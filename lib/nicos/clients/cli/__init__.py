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

"""Command-line client for the NICOS daemon."""

from __future__ import with_statement

__version__ = "$Revision$"

import os
import sys
import glob
import time
import errno
import Queue
import random
import select
import signal
import getpass
import readline
import tempfile
import subprocess
import ConfigParser
import ctypes, ctypes.util
from os import path
from time import strftime, localtime
from logging import DEBUG, INFO, WARNING, ERROR, FATAL
from threading import Thread

from nicos.clients.base import NicosClient
from nicos.utils import colorize, which, formatDuration, formatEndtime, \
    terminalSize, parseConnectionString
from nicos.utils.loggers import ACTION, OUTPUT, INPUT
from nicos.utils.graceplot import grace_available, GracePlotter
from nicos.protocols.daemon import DEFAULT_PORT, STATUS_INBREAK, \
     STATUS_IDLE, STATUS_IDLEEXC

levels = {DEBUG: 'DEBUG', INFO: 'INFO', WARNING: 'WARNING',
          ERROR: 'ERROR', FATAL: 'FATAL'}

# introduce the readline C library to our program (we will use Python's
# binding module where possible, but otherwise call the readline functions
# directly via ctypes)
librl = ctypes.cdll[ctypes.util.find_library('readline')]
rl_vcpfunc_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

# some useful default readline keybindings
DEFAULT_BINDINGS = '''\
tab: complete
"\\e[5~": history-search-backward
"\\e[6~": history-search-forward
"\\e[1;3D": backward-word
"\\e[1;3C": forward-word
'''

# yay, global state!
readline_result = Ellipsis

def readline_finish_callback(result):
    """A callback for readline() below that records the final line
    in a global variable.  (For some reason making this a method
    of NicosCmdClient fails.)
    """
    global readline_result
    librl.rl_callback_handler_remove()
    # NULL pointer gives None, which means EOF
    readline_result = result

c_readline_finish_callback = rl_vcpfunc_t(readline_finish_callback)

class StateChange(Exception):
    """Raised by readline when changing to/from debugger state."""


class NicosCmdClient(NicosClient):

    def __init__(self, conndata, plot_on=False):
        NicosClient.__init__(self)
        # connection data as a dictionary
        self.conndata = conndata
        # whether to suppress printing history and other info on connection
        self.quiet_connect = False
        # various state variables
        self.in_question = False
        self.in_editing = False
        self.tip_shown = False
        # current script, line within it and filename of script
        self.current_script = ['']
        self.current_line = -1
        self.current_filename = ''
        # pending requests (i.e. scripts) in the daemon
        self.pending_requests = {}
        # filename of last edited script
        self.edit_filename = ''
        # instrument name from NICOS, pre-filled with server name
        self.instrument = conndata['host'].split('.')[0]
        # script directory from NICOS
        self.scriptdir = '.'
        # execution mode of the NICOS session
        self.current_mode = 'master'
        # messages queueing up while the editor is running
        self.message_queue = []
        # plotting support
        self.grace = GracePlotter(None) if grace_available else None
        self.grace_on = plot_on
        self.last_dataset = None
        # whether we have initiated a simulation lately
        self.simulating = False
        # whether a stop is pending
        self.stop_pending = False
        # whether we are in debugging mode
        self.debug_mode = False
        # detected text-mode browser for help display
        self.browser = None
        # used for determining how much history to print by default
        self.tsize = terminalSize()
        # output stream to print to
        self.out = sys.stdout

        # set up readline
        for line in DEFAULT_BINDINGS.splitlines():
            readline.parse_and_bind(line)
        readline.set_completer(self.completer)
        readline.set_history_length(10000)
        self.histfile = path.expanduser('~/.nicoshistory')
        if path.isfile(self.histfile):
            readline.read_history_file(self.histfile)
        self.completions = []

        # set up "wakeup" pipe to notify readline of ourput and changed prompt
        self.wakeup_pipe_r, self.wakeup_pipe_w = os.pipe()

        # set up clientexec (plotting) thread
        self.clientexec_queue = Queue.Queue()
        self.clientexec_thread = Thread(target=self.clientexec_thread_entry)
        self.clientexec_thread.setDaemon(True)
        self.clientexec_thread.start()

        # pre-set prompt to sane default
        self.set_status('disconnected')

    # -- low-level terminal input/output routines

    def readline(self, prompt, add_history=True):
        """Read a line from the user.

        This function basically reimplements the readline module's
        readline_until_enter_or_signal C function, with the addition
        that we set new prompts and update the display periodically.

        Thanks to ctypes this is possible without a custom C module.
        """
        global readline_result
        librl.rl_callback_handler_install(prompt, c_readline_finish_callback)
        readline_result = Ellipsis
        while readline_result is Ellipsis:
            try:
                res = select.select([sys.stdin, self.wakeup_pipe_r], [], [], 1)[0]
            except select.error, e:
                if e.args[0] == errno.EINTR:
                    continue
                librl.rl_callback_handler_remove()
                raise
            except:
                librl.rl_callback_handler_remove()
                raise
            if sys.stdin in res:
                librl.rl_callback_read_char()
            if self.wakeup_pipe_r in res:
                os.read(self.wakeup_pipe_r, 1)
                if not self.in_question:
                    # question has an alternate prompt that never changes
                    librl.rl_set_prompt(self.prompt)
                librl.rl_forced_update_display()
        if readline_result:
            # add to history, but only if requested and not the same as the
            # previous history entry
            if add_history and readline.get_history_item(
                readline.get_current_history_length() - 1) != readline_result:
                librl.add_history(readline_result)
        elif readline_result is None:
            raise EOFError
        elif readline_result is False:
            raise StateChange
        return readline_result

    def put(self, string):
        """Put a line of output, preserving the prompt afterwards."""
        self.out.write('\r\x1b[K%s\n' % string)
        self.out.flush()
        os.write(self.wakeup_pipe_w, ' ')

    def put_error(self, string):
        """Put a client error message."""
        self.put(colorize('red', '# ERROR: ' + string))

    def put_client(self, string):
        """Put a client info message."""
        self.put(colorize('bold', '# ' + string))

    def ask_passwd(self, question):
        """Prompt user for a password."""
        return getpass.getpass(colorize('bold', '# %s ' % question))

    def ask_question(self, question, chars='', default='', on_intr=''):
        """Prompt user for input to a question."""
        # add hints of what can be entered
        if chars:
            question += ' (%s)' % ('/'.join(chars.upper()))
        if default:
            question += ' [%s]' % default
        self.in_question = True
        try:
            try:
                # see set_status() for an explanation of the special chars here
                ans = self.readline('\x01\r\x1b[K' + colorize('bold',
                                    '\x02# ' + question + ' \x01') + '\x02',
                                    add_history=False)
            except (KeyboardInterrupt, EOFError):
                return on_intr
            if chars:
                # we accept any string; if it's beginning with one of the chars,
                # that is the result, otherwise it's the default value
                ans = ans.lower()
                for char in chars:
                    if ans.startswith(char):
                        return char
                return default
            if not ans:
                ans = default
            return ans
        finally:
            self.in_question = False

    # -- event (signal) handlers

    def initial_update(self):
        """Called after connection is established."""
        # request current full status
        state = self.ask('getstatus')
        if state is None:
            return
        status, script, output, watch, setups, reqqueue = state[:6]
        if not self.quiet_connect:
            self.put_client(
                'Connected to %s:%s as %s. '
                'Replaying output (enter "/log" to see more)...' %
                (self.host, self.port, self.conndata['login']))
            for msg in output[-self.tsize[1]:]:
                self.put_message(msg)
            if not self.tip_shown:
                self.put_client('Loaded setups: %s. Enter "/help" for help '
                                'with the client commands.' %
                                (', '.join(setups) or '(none)'))
                self.tip_shown = True
            else:
                self.put_client('Loaded setups: %s.' %
                                (', '.join(setups) or '(none)'))
        else:
            self.put_client('Connected to %s:%s as %s. ' %
                            (self.host, self.port, self.conndata['login']))
        self.signal('processing', {'script': script, 'reqno': 0})
        self.signal('status', status)
        self.scriptdir = self.eval('session.experiment.scriptdir', '.')
        self.instrument = self.eval('session.instrument.instrument',
                                    self.instrument)
        self.current_mode = self.eval('session.mode', 'master')
        for req in reqqueue:
            self.pending_requests[req['reqno']] = req
        self.set_status(self.status)

    stcolmap = {'idle': 'blue',
                'running': 'fuchsia',
                'interrupted': 'red',
                'disconnected': 'darkgray'}
    modemap =  {'master': '',
                'slave':  'slave,',
                'simulation': 'simmode,',
                'maintenance': 'maintenance,'}

    def set_status(self, status):
        """Update the current execution status, and set a new prompt."""
        self.status = status
        if self.stop_pending:
            pending = ' (stop pending)'
        elif self.pending_requests:
            pending = ' (%d pending)' % len(self.pending_requests)
        else:
            pending = ''
        # \x01/\x02 are markers recognized by readline as "here come"
        # zero-width control characters; ESC[K means "clear whole line"
        self.prompt = '\x01' + colorize(self.stcolmap[status],
            '\r\x1b[K\x02# ' + self.instrument + '[%s%s]%s >> \x01' %
            (self.modemap[self.current_mode], status, pending)) + '\x02'
        os.write(self.wakeup_pipe_w, ' ')

    def clientexec(self, what):
        """Handles the "clientexec" signal."""
        plot_func_path = what[0]
        try:
            modname, funcname = plot_func_path.rsplit('.', 1)
            func = getattr(__import__(modname, None, None, [funcname]),
                           funcname)
            self.clientexec_queue.put((func, what[1:]))
        except Exception, err:
            self.put_error('During "clientexec": %s.' % err)

    def showhelp(self, html):
        """Handles the "showhelp" signal.

        As we already get HTML, we try to get hold of a text-mode browser
        and let it dump the HTML as text.  Then we print that to the user.
        """
        # write HTML to a temporary file
        fd, fn = tempfile.mkstemp('.html')
        os.write(fd, html)
        os.close(fd)
        # check for a text browser to convert to text only
        if self.browser is None:
            if which('links'):
                self.browser = 'links'
            elif which('w3m'):
                self.browser = 'w3m'
            else:
                self.put_error('No text browser available. '
                               'Install links or w3m.')
                return
        # run HTML through text browser
        width = str(self.tsize[0])
        self.out.write('\r\x1b[K\n')
        if self.browser == 'links':
            subprocess.Popen(['links', '-dump', '-width', width, fn]).wait()
        else:
            subprocess.Popen(['w3m', '-dump', '-cols', width, fn]).wait()
        # remove tempfile
        try:
            os.unlink(fn)
        except Exception:
            pass

    def put_message(self, msg):
        """Handles the "message" signal."""
        if msg[5] == '(sim) ' and not self.simulating:
            return
        if msg[0] == 'nicos':
            namefmt = ''
        else:
            namefmt = '%-10s: ' % msg[0]
        timefmt = strftime('[%Y-%m-%d %H:%M:%S]', localtime(msg[1]))
        levelno = msg[2]
        if levelno == ACTION:
            action = namefmt + msg[3].rstrip()
            self.out.write('\033]0;NICOS%s\007' %
                           (action and ' (%s)' % action or ''))
            return
        else:
            if levelno <= DEBUG:
                newtext = colorize('darkgray', namefmt + msg[3].rstrip())
            if levelno <= OUTPUT:
                newtext = namefmt + msg[3].rstrip()
            elif levelno == INPUT:
                newtext = colorize('darkgreen', msg[3].rstrip())
                #return
            elif levelno <= WARNING:
                newtext = colorize('purple', timefmt + ' ' + namefmt +
                                   levels[levelno] + ': ' + msg[3].rstrip())
            else:
                newtext = colorize('red', timefmt + ' ' + namefmt +
                                   levels[levelno] + ': ' + msg[3].rstrip())
        self.put(msg[5] + newtext)

    def signal(self, type, data=None, exc=None):
        """Handles any kind of signal/event sent by the daemon."""
        try:
            # try to order the elifs by frequency
            if type == 'message':
                if self.in_editing:
                    self.message_queue.append(data)
                else:
                    self.put_message(data)
            elif type == 'status':
                status, line = data
                if status == STATUS_IDLE or status == STATUS_IDLEEXC:
                    new_status = 'idle'
                    self.stop_pending = False
                elif status != STATUS_INBREAK:
                    new_status = 'running'
                else:
                    new_status = 'interrupted'
                if status != self.status:
                    self.set_status(new_status)
                if line != self.current_line:
                    self.current_line = line
            elif type == 'cache':
                if data[1].endswith('/scriptdir'):
                    self.scriptdir = self.eval(
                        'session.experiment.scriptdir', '.')
            elif type == 'processing':
                script = data.get('script')
                if script is None:
                    return
                self.current_filename = data.get('name', '')
                script = script.splitlines() or ['']
                if script != self.current_script:
                    self.current_script = script
                self.pending_requests.pop(data['reqno'], None)
                self.set_status(self.status)
            elif type == 'request':
                if 'script' in data:
                    self.pending_requests[data['reqno']] = data
                self.set_status(self.status)
            elif type == 'blocked':
                removed = filter(None,
                    (self.pending_requests.pop(reqno, None) for reqno in data))
                if removed:
                    self.put_client('%d script(s) or command(s) removed from '
                                    'queue.' % len(removed))
                    self.show_pending()
                self.set_status(self.status)
            elif type == 'dataset':
                self.last_dataset = data
                if self.grace_on:
                    self.grace.beginDataset(data)
            elif type == 'datapoint':
                if self.last_dataset:
                    self.last_dataset.xresults.append(data[0])
                    self.last_dataset.yresults.append(data[1])
                    if self.grace_on:
                        self.grace.addPoint(self.last_dataset, *data)
            elif type == 'connected':
                self.initial_update()
            elif type == 'disconnected':
                self.put_client('Disconnected from server.')
                self.current_mode = 'master'
                self.debug_mode = False
                self.pending_requests.clear()
                self.set_status('disconnected')
            elif type == 'clientexec':
                self.clientexec(data)
            elif type == 'showhelp':
                self.showhelp(data[1])
            elif type == 'simresult':
                if self.simulating:
                    timing, devinfo = data
                    self.put_client('Simulated minimum runtime: %s '
                        '(finishes approximately %s). Device ranges:' %
                        (formatDuration(timing), formatEndtime(timing)))
                    dnwidth = max(map(len, devinfo))
                    for devname, (_, dmin, dmax) in sorted(devinfo.iteritems()):
                        self.put('#   %-*s: %10s  <->  %-10s' %
                                 (dnwidth, devname, dmin, dmax))
                self.simulating = False
            elif type == 'mode':
                self.current_mode = data
                self.set_status(self.status)
            elif type == 'debugging':
                self.debug_mode = data
                readline_finish_callback(False)
            elif type in ('error', 'failed', 'broken'):
                self.put_error(data)
            # and we ignore all other signals
        except Exception, e:
            self.put_error('In event handler: %s.' % e)

    # -- clientexec (plotting) thread

    def clientexec_thread_entry(self, empty=Queue.Empty):
        """This thread executes "clientexec" (i.e. plotting) requests and runs
        the matplotlib event loop in the meantime.
        """
        # do a blocking get for the first item -- if we don't do any plotting,
        # we don't need to import pylab and run the event loop at all
        item = self.clientexec_queue.get()
        # run the plotting function
        item[0](*item[1])
        # now it's safe to import pylab here
        import pylab
        # from now on, we do non-blocking gets, so that the mpl event loop can
        # run while waiting for a new item to appear on the queue
        while 1:
            try:
                item = self.clientexec_queue.get(False)
            except empty:
                pylab.pause(0.1)  # runs the GUI event loop for 0.1 sec
            else:
                item[0](*item[1])

    # -- command handlers

    def ask_connect(self, ask_all=True):
        hostport = '%s:%s' % (self.conndata['host'],
                              self.conndata['port'])
        if hostport in (':', ':1301') or ask_all:
            default = '' if hostport in (':', ':1301') else hostport
            server = self.ask_question('Server host:port?', default=default)
            if not server:
                return
            try:
                host, port = server.split(':', 1)
                port = int(port)
            except ValueError:
                host = server
                port = DEFAULT_PORT
            self.conndata['host'] = host
            self.conndata['port'] = port
        if not self.conndata['login'] or ask_all:
            user = self.ask_question('User name?',
                                     default=self.conndata['login'])
            self.conndata['login'] = user
        if not self.conndata['passwd'] or ask_all:
            passwd = self.ask_passwd('Password?')
            self.conndata['passwd'] = passwd
        self.instrument = self.conndata['host'].split('.')[0]
        # disable sending events with potentially large data we don't handle
        self.connect(self.conndata,
                     eventmask=('liveparams', 'livedata', 'watch'))

    def help(self, arg):
        """Implements the "/help" command."""
        if not arg:
            arg = 'main'
        if arg not in HELP:
            arg = 'main'
        helptext = HELP[arg]
        for line in helptext.splitlines():
            self.put('# ' + line)

    def edit_file(self, arg):
        """Implements the "/edit" command."""
        if not arg:
            if path.isfile(self.current_filename):
                arg = self.current_filename
        if not arg:
            self.put_error('Need a file name as argument.')
            return
        fpath = path.join(self.scriptdir, arg)
        if not os.getenv('EDITOR'):
            os.putenv('EDITOR', 'vi')
        self.in_editing = True
        try:
            ret = os.system('$EDITOR "' + fpath + '"')
        finally:
            self.in_editing = False
            for msg in self.message_queue:
                self.put_message(msg)
            self.message_queue = []
        if ret != 0 or not path.isfile(fpath):
            return
        # if the editor exited successfully (and the file exists) we try to be
        # smart about offering the user a choice of running, simulating or
        # updating the current script
        self.edit_filename = fpath
        if self.status == 'running':
            if fpath == self.current_filename:
                # current script edited: most likely we want to update it
                if self.ask_question('Update running script?', chars='yn',
                                     default='n') == 'y':
                    return self.command('update', fpath)
            else:
                # another script edited: updating will likely fail
                reply = self.ask_question('Queue or simulate file?',
                                          chars='qsn')
                if reply == 'q':
                    # this will automatically queue
                    return self.command('run!', fpath)
                elif reply == 's':
                    return self.command('sim', fpath)
        else:
            # no script is running at the moment: offer to run it
            reply = self.ask_question('Run or simulate file?', chars='rsn')
            if reply == 'r':
                return self.command('run', fpath)
            elif reply == 's':
                return self.command('sim', fpath)

    def print_where(self):
        """Implements the "/where" command."""
        if self.status in ('running', 'interrupted'):
            self.put_client('Printing current script.')
            for i, line in enumerate(self.current_script):
                if i+1 == self.current_line:
                    self.put(colorize('darkgreen', '---> ' + line))
                else:
                    self.put('     ' + line)
            self.put_client('End of script.')
        else:
            self.put_client('No script is running.')

    def show_pending(self):
        if not self.pending_requests:
            self.put_client('No scripts or commands are pending.')
            return
        self.put_client('Showing pending scripts or commands. '
                        'Use "/cancel number" to remove.')
        for reqno, script in sorted(self.pending_requests.iteritems()):
            if 'name' in script and script['name']:
                short = script['name']
            else:
                lines = script['script'].splitlines()
                if len(lines) == 1:
                    short = lines[0]
                else:
                    short = lines[0] + ' ...'
            self.put('# %s  %s' % (colorize('blue', '%4d' % reqno), short))
        self.put_client('End of pending list.')

    def switch_plot(self, arg):
        if not arg:
            if self.grace_on:
                if self.grace.activecounter:
                    self.put_client('Plotting is switched on (only '
                                    'counter %s).' %
                                    self.grace.activecounter)
                else:
                    self.put_client('Plotting is switched on.')
            elif self.grace:
                self.put_client('Plotting is switched off.')
            else:
                self.put_client('Plotting is unavailable.')
        elif arg == 'on':
            if not self.grace:
                self.put_error('Plotting is unavailable.')
                return
            self.grace_on = True
            self.grace.activecounter = None
            if self.last_dataset:
                self.grace.openPlot(self.last_dataset)
            self.put_client('Plotting now switched on.')
        elif arg == 'off':
            self.grace_on = False
            self.put_client('Plotting now switched off.')
        else:
            if not self.grace:
                self.put_error('Plotting is unavailable.')
                return
            self.grace_on = True
            self.grace.activecounter = arg
            if self.last_dataset:
                self.grace.openPlot(self.last_dataset)
            self.put_client('Plotting now switched on (for counter %s).'
                            % arg)

    def debug_repl(self):
        """Called to handle remote debugging via Rpdb."""
        self.in_question = True  # suppress prompt changes
        try:
            while self.debug_mode:
                try:
                    cmd = self.readline('\x01\r\x1b[K' + colorize('darkred',
                                        '\x02# (Rpdb) \x01') + '\x02') + '\n'
                except (EOFError, KeyboardInterrupt):
                    cmd = ''
                except StateChange:
                    if not self.debug_mode:
                        return
                self.tell('debuginput', cmd)
        finally:
            self.in_question = False

    def stop_query(self, how):
        """Called on Ctrl-C (if running) or when "/stop" is entered."""
        self.put_client('== %s ==' % how)
        self.put('# Please enter how to proceed:')
        self.put('# <I> ignore this interrupt')
        self.put('# <H> stop after current step')
        self.put('# <L> stop after current scan')
        self.put('# <S> immediate stop')
        res = self.ask_question('Your choice?', chars='ihls').upper()
        if res == 'I':
            return
        elif res == 'H':
            # Stoplevel 2 is "everywhere possible"
            self.tell('stop', '2')
            self.stop_pending = True
            self.set_status(self.status)
        elif res == 'L':
            # Stoplevel 1 is "everywhere in script, or after a scan"
            self.tell('stop', '1')
            self.stop_pending = True
            self.set_status(self.status)
        else:
            self.tell('emergency')

    def command(self, cmd, arg):
        """Called when a "/foo" command is entered at the prompt."""
        # try to order elif cases by frequency
        if cmd == 'cmd':
            # this is not usually entered as "/cmd foo", but only "foo"
            if self.status in ('running', 'interrupted'):
                reply = self.ask_question('A script is already running, '
                    'queue or execute anyway?', chars='qxn')
                if reply == 'x':
                    self.tell('exec', arg)
                elif reply == 'q':
                    self.tell('queue', '', arg)
                    self.put_client('Command queued.')
            else:
                self.tell('queue', '', arg)
        elif cmd in ('r', 'run', 'run!'):
            if not arg:
                # since we remember the last edited file, we can offer
                # running it here
                if self.edit_filename:
                    reply = self.ask_question('Run last edited file %r?' %
                                path.basename(self.edit_filename),
                                chars='yn', default='y')
                    if reply == 'y':
                        self.command('run', self.edit_filename)
                        return
                self.put_error('Need a file name as argument.')
                return
            fpath = path.join(self.scriptdir, arg)
            try:
                code = open(fpath).read()
            except Exception, e:
                self.put_error('Unable to open file: %s.' % e)
                return
            if self.status in ('running', 'interrupted') and cmd != 'run!':
                if self.ask_question('A script is already running, '
                    'queue script?', chars='yn', default='y') == 'y':
                    self.tell('queue', fpath, code)
            else:
                self.tell('queue', fpath, code)
        elif cmd == 'update':
            if not arg:
                # always take the current filename, if it still exists
                if path.isfile(self.current_filename):
                    arg = self.current_filename
            if not arg:
                self.put_error('Need a file name as argument.')
                return
            fpath = path.join(self.scriptdir, arg)
            try:
                code = open(fpath).read()
            except Exception, e:
                self.put_error('Unable to open file: %s.' % e)
                return
            self.tell('update', code)
        elif cmd in ('sim', 'simulate'):
            if not arg:
                self.put_error('Need a file name or code as argument.')
                return
            fpath = path.join(self.scriptdir, arg)
            # detect whether we have a filename or potential Python code
            if path.isfile(fpath) or fpath.endswith('.py'):
                try:
                    code = open(fpath).read()
                except Exception, e:
                    self.put_error('Unable to open file: %s.' % e)
                    return
                self.simulating = True
                self.tell('simulate', fpath, code)
            else:
                self.simulating = True
                self.tell('simulate', '', arg)
        elif cmd in ('e', 'edit'):
            self.edit_file(arg)
        elif cmd == 'break':
            self.tell('break')
        elif cmd in ('cont', 'continue'):
            self.tell('continue')
        elif cmd in ('s', 'stop'):
            if self.status == 'running':
                self.stop_query('Stop request')
            else:
                self.tell('emergency')
        elif cmd == 'pending':
            self.show_pending()
        elif cmd == 'cancel':
            if arg != '*':
                # this catches an empty arg as well
                try:
                    arg = int(arg)
                    self.pending_requests[arg]
                except (ValueError, KeyError):
                    self.put_error('Need a pending request number '
                                   '(see "/pending") or "*" to clear all.')
                    return
            self.tell('unqueue', str(arg))
        elif cmd == 'plot':
            self.switch_plot(arg)
        elif cmd == 'disconnect':
            if self.connected:
                self.disconnect()
        elif cmd == 'connect':
            if self.connected:
                self.put_error('Already connected. Use /disconnect first.')
            else:
                self.ask_connect()
        elif cmd == 'reconnect':
            self.ask_connect(ask_all=False)
        elif cmd in ('q', 'quit'):
            if self.connected:
                self.disconnect()
            return 0   # i.e. exit with success
        elif cmd in ('h', 'help', '?'):
            self.help(arg)
        elif cmd == 'log':
            if arg:
                n = -int(arg)
            else:
                n = None  # as a slice index, this means "unlimited"
            # this can take a while to transfer, but we don't want to cache
            # messages in this client just for this command
            state = self.ask('getstatus')
            if state is None:
                return
            self.put_client('Printing %s previous messages.' %
                            (-n if n else 'all'))
            for msg in state[2][n:]:
                self.put_message(msg)
            self.put_client('End of messages.')
        elif cmd in ('w', 'where'):
            self.print_where()
        elif cmd == 'wait':
            # this command is mainly meant for testing and scripting purposes
            time.sleep(0.2)
            while self.status != 'idle':
                time.sleep(0.2)
        elif cmd == 'trace':
            trace = self.ask('gettrace')
            if trace is None:
                return
            self.put_client('Current stacktrace of script execution:')
            for line in trace.splitlines():
                if line:
                    self.put('# ' + line)
            self.put_client('End of stacktrace.')
        elif cmd == 'debugclient':
            import pdb
            pdb.set_trace()
        elif cmd == 'debug':
            self.tell('debug', arg)
        elif cmd == 'eval':
            self.put('-> %r' % (self.eval(arg),))
        else:
            self.put_error('Unknown command %r.' % cmd)

    # -- command-line completion support

    def complete_filename(self, fn, word):
        """Try to complete a script filename."""
        # script filenames are relative to the current scriptdir; nevertheless
        # the user can override this by giving an absolute path to the script
        initpath = path.join(self.scriptdir, fn)
        candidates = []
        # omit the part already on the line, but not what readline considers the
        # current "word"
        omit = len(initpath) - len(word)
        # complete directories and .py script files
        for f in glob.glob(initpath + '*'):
            if path.isdir(f):
                candidates.append(f[omit:] + '/')
            elif path.isfile(f) and f.endswith('.py'):
                candidates.append(f[omit:])
        return candidates

    commands = ['run', 'simulate', 'edit', 'update', 'break', 'continue',
                'stop', 'where', 'disconnect', 'connect', 'reconnect',
                'quit', 'help', 'log', 'pending', 'cancel', 'plot']

    def completer(self, text, state):
        """Try to complete the command line.  Called by readline."""
        if state == 0:
            # we got a a new bit of text to complete...
            line = readline.get_line_buffer()
            if line.startswith('/'):
                # client command: complete either command or filename
                parts = line[1:].split()
                if len(parts) < 2 and not line.endswith(' '):
                    self.completions = [cmd for cmd in self.commands
                                        if cmd.startswith(text)]
                else:
                    if parts[0] in ('r', 'run', 'e', 'edit',
                                    'update', 'sim', 'simulate'):
                        try:
                            fn = parts[1]
                        except IndexError:
                            fn = ''
                        self.completions = self.complete_filename(fn, text)
                    else:
                        self.completions = []
            else:
                # server command: ask daemon to complete for us
                try:
                    self.completions = self.ask('complete', text, line) or []
                except Exception:
                    self.completions = []
        try:
            return self.completions[state]
        except IndexError:
            return None

    # -- main loop

    def handle(self, cmd):
        """Handle a command line."""
        # dispatch either as a client command...
        if cmd.startswith('/'):
            args = cmd[1:].split(None, 1) + ['','']
            return self.command(args[0], args[1])
        elif cmd:
            # or as "normal" Python code to execute
            return self.command('cmd', cmd)
        # an empty line is ignored

    def main(self):
        """Connect and then run the main read-send-print loop."""
        try:
            self.command('reconnect', '')
            while 1:
                try:
                    cmd = self.readline(self.prompt)
                except KeyboardInterrupt:
                    # offer the user a choice of ways of stopping
                    if self.status == 'running':
                        self.stop_query('Keyboard interrupt')
                    continue
                except EOFError:
                    self.command('quit', '')
                    return 0
                except StateChange:
                    if self.debug_mode:
                        self.debug_repl()
                    continue
                ret = self.handle(cmd)
                if ret is not None:
                    return ret
        finally:
            readline.write_history_file(self.histfile)

    def main_with_command(self, command):
        self.quiet_connect = True
        self.command('reconnect', '')
        self.handle(command)
        self.command('quit', '')
        return 0


# help texts

HELP = {
    'main': '''\
This is the NICOS command-line client.  You can enter all NICOS commands
at the command line; enter "help()" for an overview of NICOS commands
and devices.

This client supports "meta-commands" beginning with a slash:

  /w(here)            -- print current script and location in it
  /log (n)            -- print more past output, n lines or everything
  /break              -- pause script after next scan step or script command
  /cont(inue)         -- continue interrupted script
  /s(top)             -- stop script (you will be prompted how abruptly)

  /pending            -- show the currently pending commands
  /cancel n           -- cancel a pending command by number

  /plot on/off/ctr    -- switch live plotting on, off, or only plot the
                         given counter name

  /e(dit) <file>      -- edit a script file
  /r(un) <file>       -- run a script file
  /sim(ulate) <file>  -- simulate a script file
  /update <file>      -- update running script

  /disconnect         -- disconnect from NICOS daemon
  /connect            -- connect to a NICOS daemon
  /reconnect          -- reconnect to NICOS daemon last used
  /q(uit)             -- quit this client (NICOS will continue running)

Command parts in parenteses can be omitted.

All output prefixed with "#" comes from the client.

To learn how to pre-set your connection parameters, enter "/help connect".
To learn about debugging commands, enter "/help debug".
''',
    'connect': '''\
Connection defaults can be given on the command-line, e.g.

  nicos-client [-p] user@server:port

The -p flag switches on plotting.  A SSH tunnel can be automatically set up
for you with the following syntax:

  nicos-client user@server:port via sshuser@host

or in a ~/.nicos-client file, like this:

  [connect]
  server = localhost:1301
  user = admin
  passwd = secret
  via = root@instrumenthost
  plot = on

"Profiles" can be created in the config file with sections named other
than "connect". For example, if a section "tas" exists with entries
"server", "user" etc., these parameters can be used by calling the
command line

  nicos-client tas

or by a symlink to "nicos-client" called "tas".
''',
    'debug': '''\
There are several debugging commands built into the client:

While a script is running:

  /trace              -- show current stacktrace of script
  /debug              -- put running script into debug mode (pdb);
                         exit using the "c" (continue) command

With no script running:

  /debug code         -- execute some code under remote pdb

At any time:

  /eval expr          -- evaluate expression in script namespace and
                         print the result
  /debugclient        -- drop into a pdb shell to debug the client:
                         exit using the "c" command
'''
}


def main(argv):
    server = user = passwd = via = command = ''
    plot = False

    # to automatically close an SSH tunnel, we execute something on the remote
    # server that takes long enough for the client to connect to the daemon;
    # SSH then keeps the session open until the tunnel is unused, i.e. the
    # client has disconnected -- normally, "sleep" should be available as a
    # dummy remote command, but e.g. on erebos.frm2.tum.de it isn't, so we
    # allow configuring this (but only in the config file, not on the cmdline)
    viacommand = 'sleep 10'

    # a connection "profile" can be given by invoking this executable
    # under a different name (via symlink) ...
    configsection = 'connect'
    if not argv[0].endswith('nicos-client'):
        configsection = path.basename(argv[0])

    config = ConfigParser.RawConfigParser()
    config.read([path.expanduser('~/.nicos-client')])

    # check for plotting switch
    if '-p' in argv:
        plot = True
        argv.remove('-p')

    # check for "command to run" switch
    if '-c' in argv:
        n = argv.index('-c')
        if len(argv) >= n:
            command = argv[n+1]
        del argv[n:n+2]

    # ... or by "profile" on the command line (other arguments are
    # interpreted as a connection data string)
    if argv[1:]:
        if config.has_section(argv[1]):
            configsection = argv[1]
        else:
            cd = parseConnectionString(argv[1], DEFAULT_PORT)
            server = '%s:%s' % cd[2:4]
            user = cd[0]
            passwd = cd[1]
        if argv[3:] and argv[2] == 'via':
            via = argv[3]

    # check for profile name as a config section (given by argv0 or on the
    # command line); if not present, fall back to default
    if not config.has_section(configsection):
        configsection = 'connect'

    # take all connection parameters from the config file if not defined
    # on the command line
    if not server and config.has_option(configsection, 'server'):
        server = config.get(configsection, 'server')
    if not user and config.has_option(configsection, 'user'):
        user = config.get(configsection, 'user')
    if not passwd and config.has_option(configsection, 'passwd'):
        passwd = config.get(configsection, 'passwd')
    if not via and config.has_option(configsection, 'via'):
        via = config.get(configsection, 'via')
    if config.has_option(configsection, 'viacommand'):
        viacommand = config.get(configsection, 'viacommand')
    if config.has_option(configsection, 'plot'):
        plot = config.getboolean(configsection, 'plot')

    # split server in host:port components
    try:
        host, port = server.split(':', 1)
        port = int(port)
    except ValueError:
        host = server
        port = DEFAULT_PORT

    # if SSH tunneling is requested, stop here and re-exec after tunnel is
    # set up and running
    if via:
        # use a random (hopefully free) high numbered port on our side
        nport = random.randint(10000, 20000)
        os.execvp('sh', ['sh', '-c',
            'ssh -f -L "%s:%s:%s" "%s" %s && %s "%s:%s@localhost:%s"' %
            (nport, host, port, via, viacommand, argv[0], user, passwd, nport)])

    # this is the connection data format used by nicos.clients.base
    conndata = {
        'host': host,
        'port': port,
        'display': os.getenv('DISPLAY') or '',
        'login': user,
        'passwd': passwd,
    }

    # don't interrupt event thread's system calls
    signal.siginterrupt(signal.SIGINT, False)

    client = NicosCmdClient(conndata, plot)
    if command:
        return client.main_with_command(command)
    else:
        return client.main()
