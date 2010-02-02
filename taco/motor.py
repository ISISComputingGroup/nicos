#  -*- coding: iso-8859-15 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Description:
#   NICOS TACO motor definition
#
# Author:
#   Jens Kr�ger <jens.krueger@frm2.tum.de>
#   $Author$
#
#   The basic NICOS methods for the NICOS daemon (http://nicos.sf.net)
#
#   Copyright (C) 2009 Jens Kr�ger <jens.krueger@frm2.tum.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# *****************************************************************************

"""Implementation of the class for TACO controlled motors."""

__author__ = "Jens Kr�ger <jens.krueger@frm2.tum.de>"
__date__   = "$Date$"
__version__= "$Revision$"

from Motor import Motor as TACOMotor
import TACOStates
import TACOClient

from nicm import status
from nicm.errors import ConfigurationError, NicmError
from nicm.motor import Motor as NicmMotor
from taco.base import TacoDevice
from taco.errors import taco_guard


class Motor(TacoDevice, NicmMotor):
    """TACO motor implementation class."""

    taco_class = TACOMotor

    def doVersion(self):
        """Returns the version of the module (class)."""
        return __version__

    def doStart(self, target):
        taco_guard(self._dev.start, target)

    def doSetPosition(self, target):
        taco_guard(self._dev.setpos, target)

    def doStatus(self):
        stat = taco_guard(self._dev.deviceState)
        if stat == TACOStates.DEVICE_NORMAL:
            return status.OK
        elif stat == TACOStates.MOVING:
            return status.BUSY
        else:
            return status.ERROR

    def doStop(self):
        taco_guard(self._dev.stop)

    def doGetSpeed(self):
        return taco_guard(self._dev.speed)

    def doSetSpeed(self, value):
        taco_guard(self._dev.setSpeed, value)
