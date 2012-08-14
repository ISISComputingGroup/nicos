#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS daemon package."""

from __future__ import with_statement

__version__ = "$Revision$"

import time
import Queue
import select
import socket
import weakref
import threading
from SocketServer import TCPServer

from nicos import nicos_version
from nicos.core import listof, tupleof, oneof, Device, Param
from nicos.utils import closeSocket

from nicos.daemon.user import Authenticator
from nicos.daemon.utils import serialize
from nicos.daemon.script import ExecutionController
from nicos.daemon.handler import ConnectionHandler


DEFAULT_PORT = 1301


class Server(TCPServer):
    def __init__(self, daemon, address, handler):
        self.daemon = daemon
        self.handler_ident_lock = threading.Lock()
        self.handlers = weakref.WeakValueDictionary()
        self.handler_ident = 0
        self.pending_clients = {}
        TCPServer.__init__(self, address, handler)
        self.__is_shut_down = threading.Event()
        self.__serving = False

    # serve_forever, shutdown and _handle_request_noblock are copied
    # from 2.6 SocketServer, 2.5 doesn't support shutdown

    def serve_forever(self,timeout=1.0):
        self.__serving = True
        self.__is_shut_down.clear()
        while self.__serving:
            r = select.select([self], [], [], timeout)[0]
            if r:
                self._handle_request_noblock()
        self.__is_shut_down.set()

    def _handle_request_noblock(self):
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except Exception:
                self.handle_error(request, client_address)
                self.close_request(request)

    def shutdown(self):
        self.__serving = False
        self.__is_shut_down.wait()

    def process_request(self, request, client_address):
        """Process a "request", that is, a client connection."""
        # mostly copied from ThreadingMixIn but without the import,
        # which causes threading issues because of the import lock
        t = threading.Thread(target=self.process_request_thread,
                             args=(request, client_address),
                             name='request handler')
        t.setDaemon(True)
        t.start()

    def process_request_thread(self, request, client_address):
        """Thread to process the client connection, calls the Handler."""
        try:
            # this call instantiates the RequestHandler class
            self.finish_request(request, client_address)
            self.close_request(request)
        except Exception:
            self.handle_error(request, client_address)
            self.close_request(request)

    def verify_request(self, request, client_address):
        """Called on a new connection.  If we have a connection from that
        host that lacks an event connection, use this.
        """
        host = client_address[0]
        if host not in self.pending_clients:
            self.pending_clients[host] = None
            return True
        # this is an event connection: start event sender thread on the handler
        # wait until the handler is registered
        while self.pending_clients[host] is None:
            time.sleep(0.2)
        handler = self.pending_clients[host]
        self.daemon.log.debug('event connection from %s for handler #%d' %
                               (host, handler.ident))
        event_thread = threading.Thread(target=handler.event_sender,
                                        args=(request,),
                                        name='event_sender %d' % handler.ident)
        event_thread.setDaemon(True)
        event_thread.start()
        del self.pending_clients[host]
        # don't call the usual handler
        return False

    def server_close(self):
        """Close the server socket and all client sockets."""
        for handler in self.handlers.values():
            closeSocket(handler.sock)
        closeSocket(self.socket)

    def register_handler(self, handler, host):
        """Give each handler a unique ID."""
        with self.handler_ident_lock:
            self.pending_clients[host] = handler
            self.handler_ident += 1
            handler.ident = self.handler_ident
            self.handlers[threading._get_ident()] = handler

    def unregister_handler(self, ident):
        """Remove a handler from the handlers dictionary."""
        with self.handler_ident_lock:
            del self.handlers[threading._get_ident()]

    def handle_error(self, request, client_address):
        """Last chance exception handling."""
        self.daemon.log.exception('exception while handling request')


class NicosDaemon(Device):
    """
    This class abstracts the main daemon process.
    """

    parameters = {
        'server':         Param('Address to bind to (host or host:port)',
                                type=str, mandatory=True),
        'maxlogins':      Param('Maximum number of logins', type=int,
                                default=10),
        'reuseaddress':   Param('Whether to set SO_REUSEADDR', type=bool,
                                default=True),
        'updateinterval': Param('Update interval for watch expressions',
                                type=float, unit='s', default=0.2),
        'trustedhosts':   Param('Trusted hosts allowed to log in',
                                type=listof(str)),
        'authmethod':     Param('Authentication method',
                                type=oneof('none', 'list', 'pam')),
        'passwd':         Param('User/password list for authmethod "list"',
                                type=listof(tupleof(str, str, int)))
    }

    # key: event name
    # value: whether the event data is serialized
    daemon_events = {
        'message': True,
        'request': True,
        'processing': True,
        'blocked': True,
        'status': True,
        'watch': True,
        'cache': True,
        'dataset': True,
        'datapoint': True,
        'liveparams': True,
        'livedata': False,
        'simresult': True,
        'showhelp': True,
    }

    def doInit(self, mode):
        self._stoprequest = False
        # the controller represents the internal script execution machinery
        self._controller = ExecutionController(self.log, self.emit_event,
                                               'startup')
        # to authenticate users
        self._auth = Authenticator(self)
        # log messages emitted so far
        self._messages = []

        address = self.server
        if ':' not in address:
            host = address
            port = DEFAULT_PORT
        else:
            host, port = address.split(':')
            port = int(port)

        Server.request_queue_size = self.maxlogins * 2
        Server.allow_reuse_address = self.reuseaddress
        self._server = Server(self, (host, port), ConnectionHandler)

        self._watch_worker = threading.Thread(target=self._watch_entry,
                                              name='daemon watch monitor')
        self._watch_worker.setDaemon(True)
        self._watch_worker.start()

    def _watch_entry(self):
        """
        This thread checks for watch value changes periodically and sends out
        events on changes.
        """
        # pre-fetch attributes for speed
        ctlr, intv, emit, sleep = self._controller, self.updateinterval, \
                                  self.emit_event, time.sleep
        lastwatch = {}
        while not self._stoprequest:
            sleep(intv)
            # new watch values?
            watch = ctlr.eval_watch_expressions()
            if watch != lastwatch:
                emit('watch', watch)
                lastwatch = watch

    def emit_event(self, event, data):
        """Emit an event to all handlers."""
        if self.daemon_events[event]:
            data = serialize(data)
        for handler in self._server.handlers.values():
            try:
                handler.event_queue.put((event, data))
            except Queue.Full:
                self.log.warning('handler %s: event queue full' % handler.ident)

    def start(self):
        """Start the daemon's server."""
        self.log.info('NICOS daemon v%s started, starting server on %s' %
                       (nicos_version, self.server))
        # startup the script thread
        self._controller.start_script_thread()
        self._worker = threading.Thread(target=self._server.serve_forever,
                                        name='daemon server')
        self._worker.start()

    def wait(self):
        while not self._stoprequest:
            time.sleep(0.5)
        self._worker.join()

    def quit(self):
        self.log.info('quitting...')
        self._stoprequest = True
        self._server.shutdown()
        self._worker.join()
        self._server.server_close()

    def current_script(self):
        return self._controller.current_script
