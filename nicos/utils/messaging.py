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

"""Utilies for ZeroMQ messaging."""

import sys
import time
import logging
import subprocess
from os import path
from threading import Thread

import zmq

from nicos import session, config
from nicos.protocols.daemon import serialize, unserialize
from nicos.utils.loggers import TRANSMIT_ENTRIES
from nicos.pycompat import iteritems


zmq_ctx = zmq.Context()


class SimulationSupervisor(Thread):
    """
    Thread for starting a simulation process, receiving messages from a pipe
    and displaying/sending them to the client.
    """

    def __init__(self, session, code, prefix):
        scriptname = path.join(config.nicos_root, 'bin', 'nicos-simulate')
        daemon = getattr(session, 'daemon_device', None)
        setups = session.explicit_setups
        Thread.__init__(self, target=self._target,
                        args=(daemon, scriptname, prefix, setups, code),
                        name='SimulationSupervisor')
        self.daemon = True

    def _target(self, daemon, scriptname, prefix, setups, code):
        socket = zmq_ctx.socket(zmq.PULL)
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        port = socket.bind_to_random_port('tcp://127.0.0.1')
        # start nicos-simulate process
        proc = subprocess.Popen([sys.executable, scriptname,
                                 str(port), prefix, ','.join(setups), code])
        while True:
            res = poller.poll(500)
            if not res:
                if proc.poll() is not None:
                    session.log.warning('Simulation has terminated prematurely')
                    return
                continue
            msg = unserialize(socket.recv())
            if isinstance(msg, list):
                # it's a message
                if daemon:
                    daemon.emit_event('message', msg)
                else:
                    record = logging.LogRecord(msg[0], msg[2], msg[5],
                                               0, msg[3], (), None)
                    record.message = msg[3].rstrip()
                    session.log.handle(record)
            else:
                # it's the result
                if daemon:
                    daemon.emit_event('simresult', msg)
                # In the console session, the summary is printed by the
                # sim() command.
                socket.close()
                break
        # wait for the process, but only for 5 seconds after the result
        # has arrived
        wait_start = time.time()
        try:
            # Python 3.x has a timeout argument for poll()...
            while time.time() < wait_start + 5:
                if proc.poll() is not None:
                    return
            raise Exception('did not terminate within 5 seconds')
        except Exception:
            session.log.exception('Error waiting for simulation process')


class SimLogSender(logging.Handler):
    """
    Log handler sending messages to the original daemon via a pipe.
    """

    def __init__(self, port, session):
        logging.Handler.__init__(self)
        self.socket = zmq_ctx.socket(zmq.PUSH)
        self.socket.connect('tcp://127.0.0.1:%d' % port)
        self.session = session
        self.devices = []
        self.aliases = []

    def begin_setup(self):
        self.level = logging.ERROR  # log only errors before code starts

    def begin_exec(self):
        from nicos.core import Readable
        from nicos.core.device import DeviceAlias
        # Collect information on timing and range of all devices
        self.starttime = self.session.clock.time
        for devname, dev in iteritems(self.session.devices):
            if isinstance(dev, DeviceAlias):
                self.aliases.append(devname)
            elif isinstance(dev, Readable):
                self.devices.append(devname)
                dev._sim_min = None
                dev._sim_max = None
        self.level = 0

    def emit(self, record, entries=TRANSMIT_ENTRIES):  #pylint: disable=W0221
        msg = [getattr(record, e) for e in entries]
        if not hasattr(record, 'nonl'):
            msg[3] += '\n'
        self.socket.send(serialize(msg))

    def finish(self):
        stoptime = self.session.clock.time
        devinfo = {}
        for devname in self.devices:
            dev = self.session.devices.get(devname)
            minmax = dev._sim_getMinMax()
            for _name, _value, _min, _max in minmax:
                try:
                    devinfo[_name] = (_value, _min, _max, [])
                except Exception:
                    pass
        for devname in self.aliases:
            adev = self.session.devices.get(devname)
            if adev and adev.alias:
                devname = session.devices[adev.alias].name
                if devname in devinfo:
                    devinfo[devname][3].append(adev.name)
        self.socket.send(serialize((stoptime, devinfo)))
