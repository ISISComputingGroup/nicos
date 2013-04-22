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

"""TACO power supply classes."""

from time import sleep

import DEVERRORS
import TACOStates
from PowerSupply import CurrentControl, VoltageControl

from nicos.core import status, Moveable, HasOffset, HasLimits, Param, \
     MoveError, NicosError, waitForStatus
from nicos.devices.taco.core import TacoDevice


class Supply(HasOffset, HasLimits, TacoDevice, Moveable):
    """Base class for TACO power supplies.

    This is a common base class, please use either `CurrentSupply` or
    `VoltageSupply` for concrete devices.
    """

    parameters = {
        'ramp': Param('Ramp for the supply; can be zero to deactivate ramping',
                      type=float, unit='main/min', default=0, settable=True),
        'variance': Param('Variance of the read value to the write value; can '
                          'be zero to deactivate variance check',
                          type=float, unit='%', default=0),
    }

    def doReadRamp(self):
        try:
            return self._taco_guard(self._dev.ramp)
        except NicosError, err:
            if err.tacoerr == DEVERRORS.DevErr_CommandNotImplemented:
                return 0
            raise

    def doWriteRamp(self, value):
        self._taco_guard(self._dev.setRamp, value)

    def doRead(self, maxage=0):
        return self._taco_multitry('read', 2, self._dev.read) - self.offset

    def doStart(self, value, fromvarcheck=False):
        self._taco_multitry('write', 2, self._dev.write, value + self.offset)
        sleep(0.5)  # wait until server goes into "moving" status
        if self.variance > 0:
            newvalue = self.wait()
            maxdelta = value * (self.variance/100.) + 0.1
            if abs(newvalue - value) > maxdelta:
                if not fromvarcheck:
                    self.log.warning('value %s instead of %s exceeds variance'
                                     % (newvalue, value))
                    self.doStart(value, fromvarcheck=True)
                else:
                    raise MoveError(self,
                                    'power supply failed to set correct value')

    def doStop(self):
        self._taco_guard(self._dev.stop)

    def doStatus(self, maxage=0):
        # XXX put voltage in status information?
        state = self._taco_guard(self._dev.deviceState)
        if state == TACOStates.DEVICE_NORMAL:
            return status.OK, 'device normal'
        elif state in (TACOStates.MOVING, TACOStates.RAMP):
            return status.BUSY, 'ramping'
        elif state == TACOStates.STOPPING:
            return status.BUSY, 'stopping'
        else:
            return status.ERROR, TACOStates.stateDescription(state)

    def doWait(self):
        # XXX add a timeout?
        waitForStatus(self, 0.5)


class CurrentSupply(Supply):
    """Concrete device for TACO current supplies."""
    taco_class = CurrentControl


class VoltageSupply(Supply):
    """Concrete device for TACO voltage supplies."""
    taco_class = VoltageControl
