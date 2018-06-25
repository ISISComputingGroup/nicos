#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
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
"""
The connection handler for the execution daemon, handling the protocol
commands.
"""

import os
import base64
import socket
import tempfile
import rsa


from nicos import session, nicos_version, get_custom_version, config
from nicos.core import ADMIN, ConfigurationError, SPMError, User
from nicos.core.data import ScanData
from nicos.utils import closeSocket
from nicos.utils.queues import SizedQueue
from nicos.services.daemon.auth import AuthenticationError
from nicos.services.daemon.utils import LoggerWrapper
from nicos.services.daemon.script import ScriptRequest, ScriptError, \
    RequestError
from nicos.protocols.daemon import serialize, unserialize, STATUS_IDLE, \
    STATUS_IDLEEXC, STATUS_RUNNING, STATUS_STOPPING, STATUS_INBREAK, \
    ENQ, ACK, STX, NAK, LENGTH, PROTO_VERSION, BREAK_NOW, code2command, \
    DAEMON_COMMANDS, SIM_STATES, event2code
from nicos.pycompat import queue, socketserver, string_types


READ_BUFSIZE = 4096


class CloseConnection(Exception):
    """Raised to unconditionally close the connection."""

command_wrappers = {}


def command(needcontrol=False, needscript=None, name=None):
    """
    Decorates a nicosd protocol command.  The `needcontrol` and `needscript`
    parameters can be set to avoid boilerplate in the handler functions.
    """
    def deco(func):
        nargsmax = func.__code__.co_argcount - 1
        nargsmin = nargsmax - len(func.__defaults__ or ())

        def wrapper(self, args):
            if not nargsmin <= len(args) <= nargsmax:
                self.write(NAK, 'invalid number of arguments')
                return
            if needcontrol:
                if not self.check_control():
                    self.write(NAK, 'you do not have control of the session')
                    return
            if needscript is True:
                if self.controller.status in (STATUS_IDLE, STATUS_IDLEEXC):
                    self.write(NAK, 'no script is running')
                    return
            elif needscript is False:
                if self.controller.status not in (STATUS_IDLE, STATUS_IDLEEXC):
                    self.write(NAK, 'a script is running')
                    return
            try:
                return func(self, *args)
            except CloseConnection:
                raise
            except Exception:
                self.log.exception('exception executing command %s',
                                   name or func.__name__)
                self.write(NAK, 'exception occurred executing command')
        wrapper.__name__ = func.__name__
        wrapper.orig_function = func
        command_wrappers[name or func.__name__] = wrapper
        return func
    return deco

# unique objects
stop_queue = (object(), '')
no_msg = object()


class ConnectionHandler(socketserver.BaseRequestHandler):
    """
    This class is the SocketServer "request handler" implementation for the
    daemon server.  One instance of this class is created for every control
    connection (not event connections) from a client.  When the event
    connection is opened, the `event_sender` method of the existing instance
    is spawned as a new thread.

    The `handle` method reads commands from the client, dispatches them to
    methods of the same name, and writes the responses back.

    Command methods must be decorated with the `@command` decorator; it
    registers the command for dispatching and avoids boilerplate: if the
    `needcontrol` argument is True, the command will need to be called in the
    controlling session.  If the `needscript` argument is True or False, the
    command can only be called if a script is running or not running,
    respectively.

    Note that the SocketServer interface is such that the request handling is
    done while the constructor runs, i.e. the `__init__` method calls `handle`.
    """

    def __init__(self, request, client_address, client_id, server):
        # limit memory usage to 100 Megs
        self.event_queue = SizedQueue(100*1024*1024)
        self.event_mask = set()
        self.event_sock = None  # set later by server
        # bind often used daemon attributes to self
        self.daemon = server.daemon
        self.controller = server.daemon._controller
        # register self as a new handler
        server.register_handler(self, client_address[0], client_id)
        self.sock = request
        self.log = LoggerWrapper(self.daemon.log,
                                 '[handler #%d] ' % self.ident)
        # read buffer
        self._buffer = ''
        try:
            # this calls self.handle()
            socketserver.BaseRequestHandler.__init__(
                self, request, client_address, server)
        except CloseConnection:
            # in case the client hasn't opened the event connection, stop
            # waiting for it
            server.pending_clients.pop((client_address[0], client_id), None)
        except Exception:
            self.log.exception('unhandled exception')
        try:
            self.event_queue.put(stop_queue, False)
        except queue.Full:
            # the event queue has already overflown because the event sender
            # was already closed; so we can ignore this
            pass
        server.unregister_handler(self.ident)
        self.log.info('handler unregistered')

    def write(self, prefix, msg=no_msg):
        """Write a message to the client."""
        try:
            if msg is no_msg:  # cannot use None, it might be a reply
                self.sock.sendall(prefix)
            else:
                ser_msg = serialize(msg)
                self.sock.sendall(prefix + LENGTH.pack(len(ser_msg)) + ser_msg)
        except socket.error as err:
            self.log.error('write: connection broken (%s)', err)
            raise CloseConnection

    def read(self):
        """Read a command and arguments from the client."""
        try:
            # receive: ENQ (1 byte) + commandcode (2) + length (4)
            start = b''
            while len(start) < 7:
                data = self.sock.recv(7 - len(start))
                if not data:
                    self.log.error('read: connection broken')
                    raise CloseConnection
                start += data
            if start[0:1] != ENQ:
                self.log.error('read: invalid command header')
                raise CloseConnection
            # it has a length...
            length, = LENGTH.unpack(start[3:])
            buf = b''
            while len(buf) < length:
                read = self.sock.recv(min(READ_BUFSIZE, length-len(buf)))
                if not read:
                    self.log.error('read: connection broken')
                    raise CloseConnection
                buf += read
            try:
                return code2command[start[1:3]], unserialize(buf)
            except Exception:
                self.log.error('read: invalid command or garbled data', exc=1)
                self.write(NAK, 'invalid command or garbled data')
                raise CloseConnection
        except socket.error as err:
            self.log.error('read: connection broken (%s)', err)
            raise CloseConnection

    def closeSockets(self):
        closeSocket(self.event_sock)
        closeSocket(self.sock)

    def check_host(self):
        """Match the connecting host against the daemon's list of
        trusted hosts.
        """
        for allowed in self.daemon.trustedhosts:
            for possible in self.clientnames:
                if allowed == possible:
                    return
        self.write(NAK, 'permission denied')
        self.log.error('login attempt from untrusted host: %s',
                       self.clientnames)
        raise CloseConnection

    def check_control(self):
        """Check if the current thread is the session's controlling thread."""
        he = self.controller.controlling_user
        me = self.user
        if self.user.level == ADMIN:
            # admin may do anything
            return True
        if he is None:
            self.controller.controlling_user = me
            return True
        if he.level > me.level:
            # user is not controlling, and currently controlling
            # user has higher priority
            return False
        # controlling user has same or lower priority (may be the same user)
        return True

    def handle(self):
        """Handle a single connection."""
        ip = self.client_address[0]
        try:
            host, aliases, addrlist = socket.gethostbyaddr(ip)
        except socket.herror:
            self.clientnames = [ip]
        else:
            self.clientnames = [host] + aliases + addrlist
        self.log.info('connection from %s', self.clientnames)

        # check trusted hosts list, if nonempty
        if self.daemon.trustedhosts:
            self.check_host()

        authenticators = self.daemon.get_authenticators()
        pubkey, privkey = rsa.newkeys(512)
        pubkeyStr = base64.encodestring(pubkey.save_pkcs1())
        bannerhashing = 'rsa,plain'

        # announce version and authentication modality
        self.write(STX, dict(
            daemon_version = nicos_version,
            custom_version = get_custom_version(),
            nicos_root = config.nicos_root,
            custom_path = config.setup_package_path,
            pw_hashing = bannerhashing,
            rsakey = pubkeyStr,
            protocol_version = PROTO_VERSION,
        ))

        # read login credentials
        cmd, (credentials,) = self.read()
        if cmd != 'authenticate' or not isinstance(credentials, dict) or \
           not all(v in credentials for v in ('login', 'passwd', 'display')):
            self.log.error('invalid login: %r, credentials=%r',
                           cmd, credentials)
            self.write(NAK, 'invalid credentials')
            raise CloseConnection

        password = credentials['passwd']
        if password[0:4] == 'RSA:':
            password = password[4:]
            password = rsa.decrypt(base64.decodestring(password.encode()),
                                   privkey)

        # check login data according to configured authentication
        login = credentials['login']
        self.log.info('auth request: login=%r display=%r', login,
                      credentials['display'])
        if authenticators:
            auth_err = None
            for auth in authenticators:
                try:
                    self.user = auth.authenticate(login, password)
                    break
                except AuthenticationError as err:
                    auth_err = err  # Py3 clears "err" after the except block
                    continue
            else:  # no "break": all authenticators failed
                self.log.error('authentication failed: %s', auth_err)
                self.write(NAK, 'credentials not accepted')
                raise CloseConnection
        else:
            self.user = User(login, ADMIN)

        # of course this only works for the client that logged in last
        os.environ['DISPLAY'] = credentials['display']

        # acknowledge the login
        self.log.info('login succeeded, access level %d', self.user.level)
        self.write(STX, dict(
            user_level = self.user.level,
        ))

        # start main command loop
        while 1:
            command, data = self.read()
            command_wrappers[command](self, data)

    # -- Event thread entry point ---------------------------------------------

    def event_sender(self, sock):
        """Take events from the handler instance's event queue and send them
        to the client using the event connection.
        """
        self.log.info('event sender started')
        queue_get = self.event_queue.get
        event_mask = self.event_mask
        # close connection after socket send queue is full for 60 seconds
        sock.settimeout(60.0)
        send = sock.sendall
        while 1:
            item = queue_get()
            if item is stop_queue:
                break
            event, data = item
            if event in event_mask:
                continue
            evtcode = event2code[event]
            try:
                # first, send length header and event name
                send(STX + evtcode + LENGTH.pack(len(data)))
                # then, send data separately (doesn't create temporary strings)
                send(data)
            except socket.timeout:
                self.log.error('send timeout in event sender')
                break
            except socket.error as err:
                self.log.warning('connection broken in event sender: %s', err)
                break
            except Exception as err:
                self.log.exception('exception in event sender; event: %s, '
                                   'data: %s', event, repr(data)[:1000])
        self.log.info('closing connections from event sender')
        self.closeSockets()

    # -- Script control commands ----------------------------------------------

    @command(needscript=False)
    def start(self, name, code):
        """Start a script within the script thread.

        Same as queue(), but will reject the command if a script is running.
        """
        self.queue(name, code)

    @command()
    def queue(self, name, code):
        """Start a script, or queue it if the script thread is busy.

        :param name: name of the script (usually the filename) or ''
        :param code: code of the script
        :returns: ok or error
        """
        if not name:
            name = None
        try:
            reqid = self.controller.new_request(
                ScriptRequest(code, name, self.user, handler=self))
        except RequestError as err:
            self.write(NAK, str(err))
            return
        # take control of the session
        self.controller.controlling_user = self.user
        self.write(STX, reqid)

    @command()
    def unqueue(self, reqid):
        """Mark the given request ID (or all, if '*') so that it is not
        executed.

        :param reqid: (str) request UUID, or '*'
        :returns: ok or error (e.g. if the given script is not in the queue)
        """
        if reqid == '*':
            self.controller.block_all_requests()
        else:
            try:
                self.controller.block_requests([reqid])
            except IndexError:
                self.write(NAK, 'script already executing')
                return
        self.write(ACK)

    @command(needcontrol=True, needscript=True)
    def update(self, newcode, reason, reqid=None):
        """Update the currently running script.

        :param newcode: new code for the current script
        :param reason: user-specified reason for the update
        :returns: ok or error (e.g. if the script differs in executing code)
        """
        try:
            self.controller.update_script(reqid, newcode, reason, self.user)
        except ScriptError as err:
            self.write(NAK, str(err))
            return
        except IndexError:
            self.write(NAK, 'script doesn\'t exist')
            return
        self.write(ACK)

    @command(needcontrol=True, needscript=True, name='break')
    def break_(self, level):
        """Pause the current script at the next breakpoint.

        :param level: (int) stop level of breakpoint, constants are defined in
           `nicos.protocols.daemon`:

           * BREAK_AFTER_LINE - pause after current scan/line in the script
           * BREAK_AFTER_STEP - pause after scanpoint/breakpoint with level "2"
           * BREAK_NOW - pause in the middle of counting
        :returns: ok or error (e.g. if script is already paused)
        """
        level = int(level)
        if self.controller.status == STATUS_STOPPING:
            self.write(NAK, 'script is already stopping')
        elif self.controller.status == STATUS_INBREAK:
            self.write(NAK, 'script is already paused')
        else:
            session.log.info('Pause requested by %s', self.user.name)
            self.controller.set_break(('break', level, self.user.name))
            if level >= BREAK_NOW:
                session.countloop_request = ('pause',
                                             'Paused by %s' % self.user.name)
            self.log.info('script pause request')
            self.write(ACK)

    @command(needcontrol=True, needscript=True, name='continue')
    def continue_(self):
        """Continue the paused script.

        :returns: ok or error (e.g. if script is not paused)
        """
        if self.controller.status == STATUS_STOPPING:
            self.write(NAK, 'could not continue script')
        elif self.controller.status == STATUS_RUNNING:
            self.write(NAK, 'script is not paused')
        else:
            self.log.info('script continue request')
            self.controller.set_continue(('continue', 0, self.user.name))
            self.write(ACK)

    @command(needcontrol=True, needscript=True)
    def stop(self, level):
        """Abort the paused script.

        :param level: (int) stop level, constants are defined in
           `nicos.protocols.daemon`:

           * BREAK_AFTER_LINE - stop after current scan/line in the script
           * BREAK_AFTER_STEP - stop after scan point/breakpoint with level "2"
           * BREAK_NOW - stop in the middle of counting (but due to the special
             way the breakpoint while counting is implemented, it will
             actually just stop there if paused before, otherwise this is
             equivalent to level '2')
        :returns: ok or error
        """
        level = int(level)
        self.log.info('script stop request')
        self.controller.script_stop(level, self.user)
        self.write(ACK)

    # note: name finish() is already defined by BaseRequestHandler
    @command(name='finish', needcontrol=True, needscript=True)
    def finish_(self):
        """Finish the currently running action early and proceed.

        Currently, the only action that can be finished early is a count().

        :returns: ok or error
        """
        self.log.info('measurement finish request')
        if self.controller.status == STATUS_STOPPING:
            self.write(NAK, 'script is stopping')
        else:
            session.log.info('Early finish requested by %s', self.user.name)
            session.countloop_request = \
                ('finish', 'Finished early by %s' % self.user.name)
        self.write(ACK)

    @command()
    def emergency(self):
        """Stop the script unconditionally and run emergency stop functions.

        This throws an exception into the thread running the script, so that
        the script is interrupted as soon as possible.  However, finalizers
        with "try-finally" are still run and can e.g. record count results.

        :returns: ok or error
        """
        if self.controller.status in (STATUS_IDLE, STATUS_IDLEEXC):
            self.log.warning('immediate stop without script running')
        else:
            self.log.warning('immediate stop request in %s',
                             self.controller.current_location(True))
        self.controller.script_immediate_stop(self.user)
        self.write(ACK)

    @command()
    def rearrange(self, ids):
        """Try to re-sort the queued scripts according to the given sequence of
        their IDs.

        :param ids: a list of request IDs that gives the new ordering

        :returns: ok or error
        """
        try:
            self.controller.rearrange_queue(ids)
        except RequestError as err:
            self.write(NAK, str(err))
        else:
            self.write(ACK)

    # -- Asynchronous script interaction --------------------------------------

    @command(needcontrol=True, name='exec')
    def exec_(self, cmd):
        """Execute a Python statement in the context of the running script.

        :param cmd: Python statement
        :returns: ok or error (it is not an error if the script itself raised
           an exception)
        """
        if self.controller.status == STATUS_STOPPING:
            self.write(NAK, 'script is stopping')
            return
        self.log.debug('executing command in script context\n%s', cmd)
        try:
            self.controller.exec_script(cmd, self.user, self)
        except Exception:
            session.logUnhandledException(cut_frames=0)
        self.write(ACK)

    @command()
    def eval(self, expr, stringify):
        """Evaluate and return an expression.

        :param expr: Python expression
        :param stringify: (bool) if True, return the `repr` of the result
        :returns: result of evaluation or an error if exception raised
        """
        self.log.debug('evaluating expression in script context\n%s', expr)
        try:
            retval = self.controller.eval_expression(expr, self, stringify)
        except Exception as err:
            self.log.exception('exception in eval command')
            self.write(NAK, 'exception raised while evaluating: %s' % err)
        else:
            self.write(STX, retval)

    @command()
    def simulate(self, name, code, uuid=None):
        """Simulate a named script by forking into simulation mode.

        :param name: name of the script (typically the filename)
        :param code: code of the script
        :param prefix: prefix string for the log output of the simulation
           process
        :returns: ok or error (e.g. if simulation is not possible)
        """
        self.log.debug('running simulation\n%s', code)
        try:
            self.controller.simulate_script(uuid, code,
                                            name or None, self.user)
        except SPMError as err:
            self.write(NAK, 'syntax error in script: %s' % err)
        except Exception as err:
            self.log.exception('exception in simulate command')
            self.write(NAK, 'exception raised running simulation: %s' % err)
        else:
            self.write(ACK)

    @command()
    def complete(self, line, lastword):
        """Get completions for the given prefix.

        :param line: the whole entered line
        :param lastword: the last word of the line
        :returns: list of matches
        """
        matches = sorted(set(self.controller.complete_line(line, lastword)))
        self.write(STX, matches)

    # -- Runtime information commands -----------------------------------------

    @command()
    def getversion(self):
        """Return the daemon's version.

        :returns: version string
        """
        self.write(STX, nicos_version)

    @command()
    def getstatus(self):
        """Return all important status info.

        :returns: dict of status info with the following entries:

           status
              tuple of (status constant, line number)
           script
              current script or ''
           watch
              dict of current watch expressions
           requests
              current request queue (list of serialized requests)
           mode
              current mode of the session as a string ('master', 'slave', ...)
           setups
              tuple of (current loaded setups, explicitly loaded setups)
           devices
              list of names of all existing devices
        """
        current_script = self.controller.current_script
        request_queue = self.controller.get_queue()
        self.write(STX, dict(
            status   = (self.controller.status, self.controller.lineno),
            script   = current_script and current_script.text or '',
            eta      = current_script and (current_script.simstate,
                                           current_script.eta)
                       or (SIM_STATES['pending'], 0),
            watch    = self.controller.eval_watch_expressions(),
            requests = request_queue,
            mode     = session.mode,
            setups   = (session.loaded_setups, session.explicit_setups),
            devices  = list(session.devices),
        ))

    @command()
    def getmessages(self, n):
        """Return the last *n* messages.

        :param n: number of messages to transfer or '*' for all messages
        :returns: list of messages (each message being a list of logging
           fields)
        """
        if n == '*':
            self.write(STX, self.daemon._messages)
        else:
            self.write(STX, self.daemon._messages[-int(n):])

    @command()
    def getscript(self):
        """Return the current script text, or an empty string.

        :returns: code of the current script
        """
        current_script = self.controller.current_script
        self.write(STX, current_script and current_script.text or '')

    @command()
    def gethistory(self, key, fromtime, totime):
        """Return history of a cache key, if available.

        :param key: cache key (without prefix) to query history
        :param fromtime: start time as Unix timestamp
        :param totime: end time as Unix timestamp
        :returns: list of (time, value) tuples
        """
        if not session.cache:
            self.write(STX, [])
        history = session.cache.history('', key, float(fromtime),
                                        float(totime))
        self.write(STX, history)

    @command()
    def getcachekeys(self, query):
        """Return a cache key query result, if available.

        XXX document this better

        :param query: input query
        :returns: list of (time, value) tuples
        """
        if not session.cache:
            self.write(STX, [])
            return
        if ',' in query:
            result = session.cache.query_db(query.split(','))
        else:
            result = session.cache.query_db(query)
        self.write(STX, result)

    @command()
    def gettrace(self):
        """Return current execution status as a stacktrace.

        :returns: stack trace as a string
        """
        self.write(STX, self.controller.current_location(True))

    # -- Watch expression commands --------------------------------------------

    @command(needcontrol=True)
    def watch(self, vallist):
        """Add watch expressions.

        :param vallist: list of expressions to add
        :returns: ack or error
        """
        if not isinstance(vallist, list):
            self.write(NAK, 'wrong argument type for add_values: %s' %
                       vallist.__class__.__name__)
            return
        for val in vallist:
            if not isinstance(val, string_types):
                self.write(NAK, 'wrong type for add_values item: %s' %
                           val.__class__.__name__)
                return
            if ':' not in val:
                val += ':default'
            self.controller.add_watch_expression(val)
        self.write(ACK)

    @command(needcontrol=True)
    def unwatch(self, vallist):
        """Delete watch expressions.

        :param vallist: list of expressions to remove, or ['*'] to remove all
        :returns: ack or error
        """
        if not isinstance(vallist, list):
            self.write(NAK, 'wrong argument type for del_values: %s' %
                       vallist.__class__.__name__)
            return
        for val in vallist:
            if not isinstance(val, string_types):
                self.write(NAK, 'wrong type for del_values item: %s' %
                           val.__class__.__name__)
                return
            if ':' not in val:
                val += ':default'
            if val.startswith('*:'):
                group = val[val.find(':'):]
                self.controller.remove_all_watch_expressions(group)
            else:
                self.controller.remove_watch_expression(val)
        self.write(ACK)

    # -- Data interface commands ----------------------------------------------

    @command()
    def getdataset(self, index):
        """Get one or more datasets.

        :param index: (int) index of the dataset or '*' for all datasets
        :returns: a list of datasets if index is '*', or a single dataset
           otherwise; or None if the dataset does not exist
        """
        if index == '*':
            try:
                self.write(STX, [ScanData(s)
                                 for s in session.data._last_scans])
            # session.experiment may be None or a stub
            except (AttributeError, ConfigurationError):
                self.write(STX, None)
        else:
            index = int(index)
            try:
                dataset = ScanData(session.data._last_scans[index])
                self.write(STX, dataset)
            except (IndexError, AttributeError, ConfigurationError):
                self.write(STX, None)

    # -- Miscellaneous commands -----------------------------------------------

    @command(needcontrol=True)
    def debug(self, code):
        """Start a pdb session in the script thread context.  Experimental!

        The daemon is put into debug mode.  Replies to pdb queries can be given
        using the "debuginput" command.  Stopping the debugging (with "q" at
        the pdb prompt or finishing the script) will exit debug mode.

        :param code: code to start in debug mode
        :returns: ack or error
        """
        if self.controller.status in (STATUS_IDLE, STATUS_IDLEEXC):
            if not code:
                self.write(NAK, 'no piece of code to debug given')
                return
            req = ScriptRequest(code, '', self.user, handler=self)
            self.controller.debug_start(req)
        else:
            if code:
                self.write(NAK, 'code to debug given, but a script is '
                           'already running')
                return
            self.controller.debug_running()
        self.write(ACK)

    @command(needcontrol=True, needscript=True)
    def debuginput(self, line):
        """Feed input lines to pdb.

        :param line: input to pdb
        :returns: ack or error
        """
        self.controller.debug_input(line)
        self.write(ACK)

    @command()
    def eventmask(self, events):
        """Disable sending of certain events to the client.

        :param events: a serialized list of event names
        :returns: ack
        """
        self.event_mask.update(events)
        self.write(ACK)

    @command()
    def eventunmask(self, events):
        """Enable sending of certain events to the client.

        :param events: a serialized list of event names
        :returns: ack
        """
        self.event_mask.difference_update(events)
        self.write(ACK)

    @command()
    def transfer(self, content):
        """Transfer a file to the server, encoded in base64.

        :param content: file content encoded with base64
        :returns: file name
        """
        fd, filename = tempfile.mkstemp(prefix='nicos')
        try:
            os.write(fd, content)
        finally:
            os.close(fd)
        self.write(STX, filename)

    @command(needcontrol=True)
    def unlock(self):
        """Give up control of the session.

        :returns: ack
        """
        self.controller.controlling_user = None
        self.write(ACK)

    @command()
    def quit(self):
        """Close the session.

        :returns: ack and closes the connection
        """
        if self.controller.controlling_user is self.user:
            self.controller.controlling_user = None
        self.log.info('disconnect')
        self.write(ACK)
        raise CloseConnection

    @command()
    def authenticate(self, data):
        """Authenticate the client.

        This command may only be used during handshake.
        """
        raise CloseConnection


# make sure we handle all protocol defined commands
for cmd in DAEMON_COMMANDS:
    if cmd not in command_wrappers:
        raise RuntimeError('Daemon command %s not handled by server!' % cmd)
