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

"""Session class for console interface."""

__version__ = "$Revision$"

import os
import pdb
import sys
import code
import time
import signal
import readline
import traceback

from nicos import session, nicos_version
from nicos.core import AccessError
from nicos.utils import colorcode, formatExtendedStack
from nicos.utils.loggers import INPUT, OUTPUT
from nicos.core.sessions import Session
from nicos.core.sessions.utils import NicosCompleter, guessCorrectCommand


DEFAULT_BINDINGS = '''\
tab: complete
"\\e[5~": history-search-backward
"\\e[6~": history-search-forward
"\\e[1;3D": backward-word
"\\e[1;3C": forward-word
'''

class NicosInteractiveStop(BaseException):
    """
    This exception is raised when the user requests a stop.
    """


class NicosInteractiveConsole(code.InteractiveConsole):
    """
    This class provides a console similar to the standard Python interactive
    console, with the difference that input and output are logged to the
    NICOS logger and will therefore appear in the logfiles.
    """

    def __init__(self, session, global_ns, local_ns):
        self.session = session
        self.log = session.log
        code.InteractiveConsole.__init__(self, global_ns)
        self.globals = global_ns
        self.locals = local_ns
        for line in DEFAULT_BINDINGS.splitlines():
            readline.parse_and_bind(line)
        readline.set_completer(session.completefn)
        readline.set_history_length(10000)
        self.histfile = os.path.expanduser('~/.nicoshistory')
        # once compiled, the interactive console uses this flag for all
        # subsequent statements it compiles
        self.compile('from __future__ import division')
        if os.path.isfile(self.histfile):
            readline.read_history_file(self.histfile)

    def interact(self, banner=None):
        signal.signal(signal.SIGINT, self.session.signalHandler)
        signal.signal(signal.SIGTERM, self.sigtermHandler)
        code.InteractiveConsole.interact(self, banner)
        readline.write_history_file(self.histfile)

    def sigtermHandler(self, *args):
        raise SystemExit

    def runsource(self, source, filename='<input>', symbol='single'):
        """Mostly copied from code.InteractiveInterpreter, but added the
        logging call before runcode().
        """
        try:
            code = self.session.commandHandler(source,
                       lambda src: self.compile(src, filename, symbol))
        except Exception:
            self.log.exception()
            return False

        if code is None:
            return True

        self.log.log(INPUT, '>>> ' + source)
        self.my_runcode(code, source)

        return False

    def raw_input(self, prompt):
        sys.stdout.write(colorcode(self.session._pscolor))
        self.session._prompting = True
        try:
            inp = raw_input(prompt)
        except KeyboardInterrupt:
            self.session.immediateStop()
            return ''
        finally:
            sys.stdout.write(colorcode('reset'))
            self.session._prompting = False
        return inp

    def my_runcode(self, codeobj, source=None):
        """Mostly copied from code.InteractiveInterpreter, but added better
        exception handling.
        """
        # record starting time to decide whether to send notification
        start_time = time.time()
        try:
            exec codeobj in self.globals, self.locals
        except NicosInteractiveStop:
            pass
        except KeyboardInterrupt:
            # "immediate stop" chosen
            session.immediateStop()
        except Exception:
            exc_info = sys.exc_info()
            self.session.logUnhandledException(exc_info)
            # also send a notification if configured
            exception = ''.join(traceback.format_exception(*exc_info))
            self.session.notifyConditionally(time.time() - start_time,
                'Exception in script',
                'An exception occurred in the executed script:\n\n' +
                exception, 'error notification',
                short='Exception: ' + exception.splitlines()[-1])
            if exc_info[0] == NameError:
                guessCorrectCommand(source)
            if exc_info[0] == AttributeError:
                guessCorrectCommand(source, attribute=True)

            return
        if code.softspace(sys.stdout, 0):
            print
        #self.locals.clear()


class ConsoleSession(Session):
    """
    Subclass of Session that configures the logging system for interactive
    interpreter usage: it adds a console handler with colored output, and
    an exception hook that reports unhandled exceptions via the logging system.
    """

    def __init__(self, appname):
        self._console = None
        Session.__init__(self, appname)
        # prompt color
        self._pscolor = 'reset'
        # showing prompt?
        self._prompting = False
        # our command completer for Python code
        self._completer = NicosCompleter(self.namespace,
                                         self.local_namespace).complete

    def _initLogging(self, prefix=None):
        Session._initLogging(self, prefix)
        sys.displayhook = self._displayhook

    def _displayhook(self, value):
        if value is not None and getattr(value, '__display__', True):
            self.log.log(OUTPUT, repr(value))

    def loadSetup(self, setupnames, allow_special=False, raise_failed=False, autocreate_devices=None):
        Session.loadSetup(self, setupnames, allow_special, raise_failed, autocreate_devices)
        self.resetPrompt()

    def setMode(self, mode):
        Session.setMode(self, mode)
        self.resetPrompt()

    def setSPMode(self, on):
        Session.setSPMode(self, on)
        self.resetPrompt()

    def resetPrompt(self):
        base = self._mode != 'master' and self._mode + ' ' or ''
        expsetups = '+'.join(self.explicit_setups)
        sys.ps1 = base + '(%s) %s ' % (expsetups,
                                       '-->' if self._spmode else '>>>')
        sys.ps2 = base + ' %s  ... ' % (' ' * len(expsetups))
        self._pscolor = dict(
            slave  = 'brown',
            master = 'darkblue',
            maintenance = 'darkred',
            simulation = 'turquoise'
        )[self._mode]

    def console(self):
        """Run an interactive console, and exit after it is finished."""
        banner = ('NICOS console ready (version %s).\nTry help() for a '
                  'list of commands, or help(command) for help on a command.'
                  % nicos_version)
        self._console = NicosInteractiveConsole(self, self.namespace,
                                               self.local_namespace)
        self._console.interact(banner)
        sys.stdout.write(colorcode('reset'))

    def completefn(self, word, index):
        if not self._spmode:
            return self._completer(word, index)
        if index == 0:
            line = readline.get_line_buffer()
            self._matches = self._spmhandler.complete(line, word)
        try:
            return self._matches[index] + ' '
        except IndexError:
            return None

    def breakpoint(self, level):
        if session._stoplevel >= level:
            old_stoplevel = session._stoplevel
            session._stoplevel = 0
            raise NicosInteractiveStop(old_stoplevel)

    def immediateStop(self):
        self.log.warning('stopping all devices for immediate stop')
        from nicos.commands.device import stop
        stop()

    def signalHandler(self, signum, frame):
        if self._in_sigint:  # ignore multiple Ctrl-C presses
            return
        if self._prompting:
            # shown while at prompt: always stop directly
            self.log.info('== Keyboard interrupt (Ctrl-C) ==')
            signal.default_int_handler(signum, frame)
        self._in_sigint = True
        try:
            self.log.info('== Keyboard interrupt (Ctrl-C) ==')
            self.log.info('Please enter how to proceed:')
            self.log.info('<I> ignore this interrupt')
            self.log.info('<H> stop after current step')
            self.log.info('<L> stop after current scan')
            self.log.info('<S> immediate stop')
            try:
                reply = raw_input('---> ')
            except RuntimeError:
                # when already in readline(), this will be raised
                reply = 'S'
            self.log.log(INPUT, reply)
            # first two choices are hidden, but useful for debugging purposes
            if reply.upper() == 'R':
                # handle further Ctrl-C presses with KeyboardInterrupt
                signal.signal(signal.SIGINT, signal.default_int_handler)
            elif reply.upper() == 'D':
                # print a stacktrace and debug
                self.log.info(formatExtendedStack(2))
                pdb.Pdb().set_trace(sys._getframe(1))
            elif reply.upper() == 'I':
                pass
            elif reply.upper() == 'H':
                self._stoplevel = 2
            elif reply.upper() == 'L':
                self._stoplevel = 1
            else:
                # this will create a KeyboardInterrupt and run stop()
                signal.default_int_handler(signum, frame)
        finally:
            self._in_sigint = False

    def forkSimulation(self, code, wait=True):
        try:
            pid = os.fork()
        except OSError:
            self.log.exception('Cannot fork into simulation mode')
            return
        if pid == 0:
            # child process
            self._manualscan = None  # allow simulating manualscans
            signal.alarm(600)        # kill forcibly after 10 minutes
            try:
                self.log.manager.globalprefix = '(sim) '
                self.setMode('simulation')
                exec code in self.namespace
            except:  # really *all* exceptions
                self.log.exception()
            finally:
                sys.exit()
            os._exit()
        # parent process
        if wait:
            try:
                os.waitpid(pid, 0)
            except OSError:
                self.log.exception('Error waiting for simulation process')

    @classmethod
    def run(cls, setup='startup', simulate=False):
        # Assign the correct class to the session singleton.
        session.__class__ = cls
        session.__init__('nicos')
        session._stoplevel = 0
        session._in_sigint = False

        # Load the initial setup and handle becoming master.
        session.handleInitialSetup(setup, simulate)

        # Fire up an interactive console.
        try:
            session.console()
        finally:
            # After the console is finished, cleanup.
            if session.mode != 'simulation':
                session.log.info('shutting down...')
            session.shutdown()

    def checkAccess(self, required):
        # for now, we have no way of knowing who the user is, so we cannot
        # respond to level= keyword
        if 'passcode' in required:
            code = required['passcode']
            if raw_input('Please enter "%s" to proceed, or press Enter to '
                         'cancel: ' % code) != code:
                raise AccessError('passcode not correct')
        return Session.checkAccess(self, required)

    def clientExec(self, func, args):
        # the client is the console itself -- just execute it
        func(*args)
