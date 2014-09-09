#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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

"""The base class for communication with the NICOS server."""

import os
import time
import socket
import hashlib
import threading
try:
    import rsa #pylint: disable=F0401
except ImportError:
    rsa = None

import numpy as np

from nicos.protocols.daemon import serialize, unserialize, ENQ, ACK, STX, NAK, \
    LENGTH, PROTO_VERSION, COMPATIBLE_PROTO_VERSIONS, DAEMON_EVENTS, \
    command2code, code2event
from nicos.pycompat import to_utf8

BUFSIZE = 8192
TIMEOUT = 30.0


class ProtocolError(Exception):
    pass

class ErrorResponse(Exception):
    pass


class NicosClient(object):
    def __init__(self, log_func):
        self.host = ''
        self.port = 0

        # if the daemon uses an old protocol version that we still support,
        # we need to fix up some requests -- this is set to the old version
        self.compat_proto = 0

        self.log_func = log_func
        self.socket = None
        self.event_socket = None
        self.lock = threading.Lock()
        self.connected = False
        self.disconnecting = False
        self.version = None
        self.gzip = False

        unique_id = to_utf8(str(time.time()) + str(os.getpid()))
        # spurious warning due to hashlib magic # pylint: disable=E1121
        self.client_id = hashlib.md5(unique_id).digest()

    def signal(self, name, *args):
        # must be overwritten
        raise NotImplementedError

    def connect(self, conndata, password=None, eventmask=None):
        """Connect to a NICOS daemon.

        *conndata* is a dictionary with keys 'host', 'port', 'login' (user name)
        and 'display' (X display to use; deprecated).

        *password* is the password for logging in.

        *eventmask* is a tuple of event names that should not be sent to this
        client.
        """
        if self.connected:
            raise RuntimeError('client already connected')
        self.disconnecting = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIMEOUT)
        try:
            self.socket.connect((conndata['host'], conndata['port']))
        except socket.error as err:
            msg = err.args[1] if len(err.args) >= 2 else str(err)
            self.signal('failed', 'Server connection failed: %s.' % msg, err)
            return
        except Exception as err:
            self.signal('failed', 'Server connection failed: %s.' % err, err)
            return

        # write client identification: we are a new client
        self.socket.sendall(self.client_id)

        # read banner
        try:
            ret, banner = self._read()
            if ret != STX:
                raise ProtocolError('invalid response format')
            if 'daemon_version' not in banner:
                raise ProtocolError('daemon version missing from response')
            daemon_proto = banner.get('protocol_version', 0)
            if daemon_proto != PROTO_VERSION:
                if daemon_proto in COMPATIBLE_PROTO_VERSIONS:
                    self.compat_proto = daemon_proto
                else:
                    raise ProtocolError('daemon uses protocol %d, but this '
                                        'client requires protocol %d'
                                        % (daemon_proto, PROTO_VERSION))
        except Exception as err:
            self.signal('failed', 'Server (%s:%d) handshake failed: %s.'
                         % (conndata['host'], conndata['port'], err))
            return

        # log-in sequence
        if password is None:
            password = conndata['passwd']
        pw_hashing = banner.get('pw_hashing', 'sha1')

        if pw_hashing[0:4] == 'rsa,':
            if rsa is not None:
                encodedkey = banner.get('rsakey', None)
                if encodedkey is None:
                    raise ProtocolError('rsa requested, but rsakey missing in banner')
                pubkey = rsa.PublicKey.load_pkcs1(encodedkey.decode('base64'))
                password = 'RSA:' + rsa.encrypt(password, pubkey).encode('base64')
            else:
                pw_hashing = pw_hashing[4:]
        if pw_hashing == 'sha1':
            password = hashlib.sha1(to_utf8(password)).hexdigest()
        elif pw_hashing == 'md5':
            password = hashlib.md5(to_utf8(password)).hexdigest()

        auth_dict = {
            'login': conndata['login'],
            'passwd': password,
            'display': conndata['display'],
        }

        if not self.tell('authenticate', auth_dict):
            return

        if eventmask:
            self.tell('eventmask', eventmask)

        # connect to event port
        self.event_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.event_socket.connect((conndata['host'], conndata['port']))
        except socket.error as err:
            msg = err.args[1]
            self.signal('failed', 'Event connection failed: %s.' % msg, err)
            return

        # write client id to ensure we get registered as event connection
        self.event_socket.sendall(self.client_id)

        # start event handler
        self.event_thread = threading.Thread(target=self.event_handler,
                                             name='event handler thread')
        self.event_thread.daemon = True
        self.event_thread.start()

        self.connected = True
        self.host, self.port = conndata['host'], conndata['port']
        self.login = conndata['login']

        self.version = 'NICOS daemon version %s' % banner['daemon_version']
        self.signal('connected')

    def event_handler(self):
        recv = self.event_socket.recv
        recvinto = self.event_socket.recv_into
        while 1:
            try:
                # receive STX (1 byte) + eventcode (2) + length (4)
                start = recv(7)
                if len(start) != 7 or start[0:1] != STX:
                    if not self.disconnecting:
                        self.signal('broken', 'Server connection broken.')
                        self._close()
                    return
                length, = LENGTH.unpack(start[3:])
                got = 0
                # read into a pre-allocated buffer to avoid copying lots of data
                # around several times
                buf = np.zeros(length, 'c')  # replace with bytearray+memoryview
                                             # on Py3 only.
                while got < length:
                    read = recvinto(buf[got:], length - got)
                    if not read:
                        if not self.disconnecting:
                            self.signal('broken', 'Server connection broken.')
                            self._close()
                        return
                    got += read
                try:
                    event = code2event[start[1:3]]
                    # serialized or raw event data?
                    if DAEMON_EVENTS[event][0]:
                        data = unserialize(buf.tostring())
                    else:
                        data = buffer(buf)
                except Exception as err:
                    self.log_func('Garbled event (%s): %r' %
                                  (err, str(buffer(buf))[:100]))
                else:
                    self.signal(event, data)
            except EnvironmentError as err:
                if err.errno == socket.EINTR:
                    continue
                else:
                    self.log_func('Error in event handler: %s' % err)
                    if not self.disconnecting:
                        self.signal('broken', 'Server connection broken.')
                        self._close()
                return
            except Exception as err:
                self.log_func('Error in event handler: %s %s' % (type(err), err))
                if not self.disconnecting:
                    self.signal('broken', 'Server connection broken.')
                    self._close()
                return

    def disconnect(self):
        self.disconnecting = True
        self.tell('quit')
        self._close()

    def _close(self):
        try:
            self.socket._sock.close()
            self.socket.close()
        except Exception:
            pass
        self.socket = None
        self.version = None
        self.gzip = False
        if self.connected:
            self.connected = False
            self.signal('disconnected')

    def handle_error(self, err):
        if isinstance(err, ErrorResponse):
            self.signal('error', 'Error from daemon: ' + err.args[0] + '.')
        else:
            if isinstance(err, ProtocolError):
                msg = 'Communication error: %s.' % err.args[0]
            elif isinstance(err, socket.timeout):
                msg = 'Connection to server timed out.'
            elif isinstance(err, socket.error):
                msg = 'Server connection broken: %s.' % err.args[1]
            # we cannot handle this without breaking connection, since
            # it generally means that the response is not yet received;
            # and to carry on means that we receive the pending response
            # "in reply" to one of the next commands
            elif isinstance(err, KeyboardInterrupt):
                msg = 'Server communication interrupted by user.'
            else:
                msg = 'Exception occurred: %s.' % err
            self.signal('broken', msg, err)
            self._close()

    def _write(self, command, args):
        """Write a command to the server."""
        if self.compat_proto:
            args = self._compat_transform_command(command, args)
        data = serialize(args)
        self.socket.sendall(ENQ + command2code[command] +
                            LENGTH.pack(len(data)) + data)

    def _read(self):
        """Receive a response from the server."""
        # receive first byte + (possibly) length
        start = self.socket.recv(5)
        if start == ACK:
            return start, None
        if len(start) != 5:
            raise ProtocolError('connection broken')
        if start[0:1] not in (NAK, STX):
            raise ProtocolError('invalid response %r' % start)
        # it has a length...
        length, = LENGTH.unpack(start[1:])
        buf = b''
        while len(buf) < length:
            read = self.socket.recv(BUFSIZE)
            if not read:
                raise ProtocolError('connection broken')
            buf += read
        try:
            return start[0:1], unserialize(buf)
        except Exception as err:
            return start[0:1], self.handle_error(err)

    def _compat_transform_command(self, command, args):
        """Transform a command for compatibility mode with old daemons."""
        return args

    def _compat_transform_reply(self, command, reply):
        """Transform a command reply for compatibility mode with old daemons."""
        return reply

    def tell(self, command, *args):
        """Excecute a command that does not generate a response.

        The arguments are the command and its parameter(s), if necessary.
        """
        if not self.socket:
            self.signal('error', 'You are not connected to a server.')
            return
        try:
            with self.lock:
                self._write(command, args)
                ret, data = self._read()
                if ret != ACK:
                    raise ErrorResponse(data)
                return True
        except (Exception, KeyboardInterrupt) as err:
            return self.handle_error(err)

    def ask(self, command, *args, **kwds):
        """Excecute a command that generates a response, and return the response.

        The arguments are the command and its parameter(s), if necessary.

        A *quiet=True* keyword can be given if no error should be generated if
        the client is not connected.
        """
        if not self.socket:
            if not kwds.get('quiet', False):
                self.signal('error', 'You are not connected to a server.')
            return
        try:
            with self.lock:
                self._write(command, args)
                ret, data = self._read()
                if ret != STX:
                    raise ErrorResponse(data)
                if self.compat_proto:
                    return self._compat_transform_reply(command, data)
                return data
        except (Exception, KeyboardInterrupt) as err:
            return self.handle_error(err)

    def eval(self, expr, default=Ellipsis, stringify=False):
        """Evaluate a Python expression in the daemon's namespace and return the
        result.

        If the *default* is not given, an exception while evaluating is
        propagated as an error signal to the client.  If it is given, the
        default is returned instead.

        If *stringify* is true, the result is returned as a string.
        """
        result = self.ask('eval', expr, bool(stringify), quiet=True)
        if isinstance(result, Exception):
            if default is not Ellipsis:
                return default
            raise result  #pylint: disable=E0702
        return result

    # high-level functionality

    def getDeviceList(self, needs_class='nicos.core.device.Device',
                      only_explicit=True):
        """Return a list of NICOS devices.

        The *needs_class* argument can be given if the devices should be
        restricted to a certain base class, such as
        ``'nicos.core.device.Moveable'``.

        If *only_explicit* is true, only devices that are in the NICOS
        namespace will be returned (i.e. no lowlevel devices).
        """
        query = 'list(dn for (dn, d) in session.devices.items() ' \
                'if %r in d.classes' % needs_class
        if only_explicit:
            query += ' and dn in session.explicit_devices'
        query += ')'
        res = self.eval(query, [])
        if res:
            return sorted(res)
        return []

    def getDeviceValue(self, devname):
        """Return current device value."""
        return self.eval('session.getDevice(%r).read()' % devname, None)

    def getDeviceValuetype(self, devname):
        """Return device value type.

        This is what has been set as the ``dev.valuetype`` attribute.
        """
        return self.eval('session.getDevice(%r).valuetype' % devname, None)

    def getDeviceParamInfo(self, devname):
        """Return info about all parameters of the device.

        The info is a dictionary of parameter name mapping to a dictionary with
        all attributes of the `.Param` instance for the parameter.
        """
        query = 'dict((pn, pi.serialize()) for (pn, pi) in ' \
                'session.getDevice(%r).parameters.items())' % devname
        return self.eval(query, {})

    def getDeviceParams(self, devname):
        """Return values of all device parameters from cache, as a dictionary."""
        params = {}
        devkeys = self.ask('getcachekeys', devname.lower() + '/') or []
        for key, value in devkeys:
            param = key.split('/')[1]
            params[param] = value
        return params

    def getDeviceParam(self, devname, param):
        """Return value of a specific device parameter from cache."""
        key = self.ask('getcachekeys', devname.lower() + '/' + param)
        if key:
            return key[0][1]
        return None
