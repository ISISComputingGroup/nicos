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

"""Web interface for NICOS."""

from __future__ import with_statement

__version__ = "$Revision$"

import os
import sys
try:
    import json
except ImportError:
    import simplejson as json
import logging
import threading
from cgi import escape
from time import sleep
from hashlib import md5
from SocketServer import ThreadingMixIn
from wsgiref.simple_server import WSGIServer

from nicos import session
from nicos.utils.loggers import NicosConsoleFormatter, DATEFMT

QUIT_MESSAGE = 'Just close the browser window to quit the session.'

CONSOLE_PAGE = r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <script type="text/javascript">
@@jquery@@
    </script>
    <script type="text/javascript">
@@support@@
    </script>
    <style type="text/css">
        html {
            height: 100%;
        }
        body {
            height: 100%;
            margin: 0 auto;
            border-left: 1px solid #ccc;
            border-right: 1px solid #ccc;
            font-family: 'Luxi Sans', sans-serif;
            background: #eee;
        }
        #page {
            padding: 10px 20px;
        }
        #console {
            width: 100%;
            background: #fff;
            color: #111;
            border: 1px solid #888;
            font-family: 'Consolas', monospace;
        }
        #cursor {
            color: #111;
        }
        tt {
            font-family: 'Consolas', monospace;
        }
        #input {
            width: 100%;
            font-size: 100%;
            border: 1px solid #888;
            font-family: 'Consolas', monospace;
        }
        #execute {
            border: 1px solid #888;
            background-color: #eee;
            font-family: 'Consolas', monospace;
        }
        .prompt1 {
            color: olive;
        }
        .prompt2 {
            color: #888;
        }
        .output {
            color: navy;
        }
        .error {
            color: #cc0000;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div id="page">
        <pre id="console"><span style="color: #aaa">Welcome to the NICOS web console!
Enter commands in the input field below.</span>
<span id="cursor">&nbsp;</span></pre>
        <input type="text" id="input" />
    </div>
    <script type="text/javascript">init();</script>
</body>
</html>
"""

try:
    CONSOLE_PAGE = CONSOLE_PAGE.replace('@@jquery@@',
        open(os.path.join(os.path.dirname(__file__), 'jquery.js')).read())
    CONSOLE_PAGE = CONSOLE_PAGE.replace('@@support@@',
        open(os.path.join(os.path.dirname(__file__), 'support.js')).read())
except Exception:
    CONSOLE_PAGE = ''

class FakeInput(object):
    def read(self):
        return ''

    def readline(self):
        return '\n'

    def readlines(self):
        return []


class WebHandler(logging.Handler):
    """Log handler for transmitting log messages to the client."""

    def __init__(self, buf, lock):
        logging.Handler.__init__(self)
        self.setFormatter(NicosConsoleFormatter(datefmt=DATEFMT))
        self.buffer = buf
        self.lock = lock

    def emit(self, record):
        with self.lock:
            self.buffer.append(self.format(record))


class MTWSGIServer(ThreadingMixIn, WSGIServer):
    """A multi-threaded WSGI server."""


class NicosApp(object):
    """The nicos-web WSGI application."""

    def __init__(self):
        self._output_buffer = []
        self._buffer_lock = threading.RLock()
        self.session_number = 0
        self.current_sid = None

    def create_loghandler(self):
        return WebHandler(self._output_buffer, self._buffer_lock)

    def __call__(self, environ, start_response):
        status = '200 OK'
        try:
            path = environ['PATH_INFO'].strip('/')
            if not path:
                ctype = 'text/html'
                response = CONSOLE_PAGE
            else:
                ctype = 'text/javascript'
                response = self.rpc(environ)
        except Exception, err:
            ctype = 'text/plain'
            status = '500 Internal Server Error'
            response = 'Error: ' + escape(str(err))
        headers = [('Content-type', ctype)]
        start_response(status, headers)
        return [response]

    json_exports = {
        'start_session': '_start_session',
        'exec': '_exec',
        'output': '_output',
    }

    def rpc(self, env):
        try:
            length = int(env['CONTENT_LENGTH'])
            request = json.loads(env['wsgi.input'].read(length))
        except Exception:
            raise RuntimeError('bad request.')
        try:
            if request['method'] not in self.json_exports:
                raise RuntimeError('method not found.')
            handler = getattr(self, self.json_exports[request['method']])
            response = handler(*request['params'])
            return json.dumps({'result': response, 'error': None})
        except Exception, err:
            try:
                errmsg = '%s: %s' % (err.__class__.__name__, err)
            except Exception:
                errmsg = 'unknown error'
            return json.dumps({'result' : None, 'error': errmsg})

    def _start_session(self):
        self.session_number += 1
        self.current_sid = md5(str(self.session_number)).hexdigest()
        return self.current_sid

    def _output(self, sid):
        while not self._output_buffer:
            sleep(0.3)
        if sid != self.current_sid:
            raise RuntimeError('session taken over by another client.')
        with self._buffer_lock:
            entries = self._output_buffer[:]
            self._output_buffer[:] = []
        return ''.join(entries)

    def _exec(self, sid, code):
        if sid != self.current_sid:
            raise RuntimeError('session taken over by another client.')
        try:
            code = compile(code, '<stdin>', 'single', 0, 1)
            exec code in session.namespace, session.local_namespace
        except SystemExit:
            print QUIT_MESSAGE
        except:
            session.logUnhandledException(sys.exc_info())
        return None
