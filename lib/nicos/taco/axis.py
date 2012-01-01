#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS axis classes."""

__version__ = "$Revision$"

import threading
from time import sleep

from Motor import Motor as TACOMotor
import TACOStates

from nicos.core import status, tupleof, anytype, usermethod, Moveable, Param, \
    NicosError, PositionError, MoveError, ModeError, waitForStatus
from nicos.abstract import Axis as BaseAxis
from nicos.taco.core import TacoDevice


class Axis(TacoDevice, BaseAxis):
    """Interface for TACO Axis server devices."""

    taco_class = TACOMotor

    parameters = {
        'speed':     Param('Motor speed', unit='main/s', settable=True),
        'accel':     Param('Motor acceleration', unit='main/s^2',
                           settable=True),
        'refspeed':  Param('Speed driving to reference switch', unit='main/s',
                           settable=True),
        'refswitch': Param('Switch to use as reference', type=str,
                           settable=True),
        'refpos':    Param('Position of the reference switch', unit='main',
                           settable=True),
    }

    # XXX the usermin/usermax resources of the Taco device are currently not
    # used or queried at all by this class

    def doStart(self, target):
        self._taco_guard(self._dev.start, target + self.offset)

    def doWait(self):
        st = waitForStatus(self, 0.3)
        if st[0] == status.ERROR:
            raise MoveError(self, st[1])
        elif st[0] == status.NOTREACHED:
            raise PositionError(self, st[1])

    def doRead(self):
        return self._taco_guard(self._dev.read) - self.offset

    def doReset(self):
        self._taco_guard(self._dev.deviceReset)
        self._taco_guard(self._dev.deviceOn)

    def doSetPosition(self, target):
        self._taco_guard(self._dev.setpos, target)

    def doStatus(self):
        state = self._taco_guard(self._dev.deviceState)
        if state in (TACOStates.DEVICE_NORMAL, TACOStates.STOPPED):
            return status.OK, 'idle'
        elif state in (TACOStates.MOVING, TACOStates.STOP_REQUESTED):
            return status.BUSY, 'moving'
        elif state == TACOStates.INIT:
            return status.BUSY, 'referencing'
        elif state == TACOStates.ALARM:
            return status.NOTREACHED, 'position not reached'
        else:
            return status.ERROR, TACOStates.stateDescription(state)

    def doStop(self):
        self._taco_guard(self._dev.stop)

    def _getMotor(self):
        motorname = self._taco_guard(self._dev.deviceQueryResource, 'motor')
        client = TACOMotor(motorname)
        return client

    @usermethod
    def reference(self):
        """Do a reference drive of the axis (do not use with encoded axes)."""
        if self._mode == 'slave':
            raise ModeError(self, 'referencing not possible in slave mode')
        elif self._sim_active:
            self.setPosition(self.refpos)
            return
        client = self._getMotor()
        self.log.info('referencing the axis, please wait...')
        self._taco_guard(client.deviceReset)
        while self._taco_guard(client.deviceState) == TACOStates.INIT:
            sleep(0.3)
        self._taco_guard(client.deviceOn)
        self.setPosition(self.refpos)
        self.log.info('reference drive complete, position is now ' +
                      self.format(self.read(0)))

    def _reset_phytron(self):
        import IO
        motor = self._getMotor()
        iodev = self._taco_guard(motor.deviceQueryResource, 'iodev')
        addr = self._taco_guard(motor.deviceQueryResource, 'address')
        client = IO.StringIO(iodev)
        self._taco_guard(client.communicate, '\x02%sCR' % addr)
        self.log.info('Phytron reset complete')

    def doReadSpeed(self):
        return self._taco_guard(self._dev.speed)

    def doWriteSpeed(self, value):
        self._taco_guard(self._dev.setSpeed, value)

    def doReadDragerror(self):
        return float(self._taco_guard(
            self._dev.deviceQueryResource, 'dragerror'))

    def doWriteDragerror(self, value):
        self._taco_update_resource('dragerror', str(value))

    def doReadPrecision(self):
        return float(self._taco_guard(
            self._dev.deviceQueryResource, 'precision'))

    def doWritePrecision(self, value):
        self._taco_update_resource('precision', str(value))

    def doReadMaxtries(self):
        return int(self._taco_guard(
            self._dev.deviceQueryResource, 'maxtries'))

    def doWriteMaxtries(self, value):
        self._taco_update_resource('maxtries', str(value))

    def doReadLoopdelay(self):
        return float(self._taco_guard(
            self._dev.deviceQueryResource, 'loopdelay'))

    def doWriteLoopdelay(self, value):
        self._taco_update_resource('loopdelay', str(value))

    def doReadBacklash(self):
        return float(self._taco_guard(
            self._dev.deviceQueryResource, 'backlash'))

    def doWriteBacklash(self, value):
        self._taco_update_resource('backlash', str(value))

    # resources that need to be set on the motor, not the axis device

    def _readMotorParam(self, resource, conv=float):
        motorname = self._taco_guard(self._dev.deviceQueryResource, 'motor')
        client = TACOMotor(motorname)
        return conv(client.deviceQueryResource(resource))

    def _writeMotorParam(self, resource, value):
        motorname = self._taco_guard(self._dev.deviceQueryResource, 'motor')
        client = TACOMotor(motorname)
        client.deviceOff()
        try:
            client.deviceUpdateResource(resource, str(value))
        finally:
            client.deviceOn()

    def doReadAccel(self):
        return self._readMotorParam('accel')

    def doWriteAccel(self, value):
        self._writeMotorParam('accel', value)

    def doReadRefspeed(self):
        return self._readMotorParam('refspeed')

    def doWriteRefspeed(self, value):
        self._writeMotorParam('refspeed', value)

    def doReadRefswitch(self):
        return self._readMotorParam('refswitch', str)

    def doWriteRefswitch(self, value):
        self._writeMotorParam('refswitch', value)

    def doReadRefpos(self):
        return self._readMotorParam('refpos')

    def doWriteRefpos(self, value):
        self._writeMotorParam('refpos', value)


class HoveringAxis(Axis):
    """A TACO axis that also controls air for airpads."""

    attached_devices = {
        'switch': (Moveable, 'The device used for switching air on and off'),
    }

    parameters = {
        'startdelay':   Param('Delay after switching on air', type=float,
                              mandatory=True, unit='s'),
        'stopdelay':    Param('Delay before switching off air', type=float,
                              mandatory=True, unit='s'),
        'switchvalues': Param('(off, on) values to write to switch device',
                              type=tupleof(anytype, anytype), default=(0, 1)),
    }

    def doInit(self):
        self._poll_thread = None

    def doStart(self, target):
        if self._poll_thread:
            raise NicosError(self, 'axis is already moving')
        if abs(target - self.read()) < self.precision:
            return
        self._adevs['switch'].move(self.switchvalues[1])
        sleep(self.startdelay)
        Axis.doStart(self, target)
        self._poll_thread = threading.Thread(target=self._pollthread)
        self._poll_thread.setDaemon(True)
        self._poll_thread.start()

    def _pollthread(self):
        sleep(0.1)
        waitForStatus(self, 0.2)
        sleep(self.stopdelay)
        try:
            self._adevs['switch'].move(self.switchvalues[0])
        finally:
            self._poll_thread = None

    def doWait(self):
        if self._poll_thread:
            self._poll_thread.join()

    def doStatus(self):
        state = self._taco_guard(self._dev.deviceState)
        if state in (TACOStates.DEVICE_NORMAL, TACOStates.STOPPED,
                     TACOStates.TRIPPED):
            # TRIPPED means: both limit switches or inhibit active
            # which is normal when air is switched off
            return status.OK, 'idle'
        elif state in (TACOStates.MOVING, TACOStates.STOP_REQUESTED):
            return status.BUSY, 'moving'
        elif state == TACOStates.ALARM:
            return status.NOTREACHED, 'position not reached'
        else:
            return status.ERROR, TACOStates.stateDescription(state)
