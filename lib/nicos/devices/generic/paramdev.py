#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
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

"""Generic device class for "moving" a parameter of another device."""

from nicos.core import Device, Moveable, Param, Override, status


class ParamDevice(Moveable):
    """
    A pseudo-device that sets the value of a selected parameter of another
    device on start(), and returns the value of the parameter on read().
    """

    hardware_access = False

    attached_devices = {
        'device':  (Device, 'The device to set/get the selected parameter'),
    }

    parameters = {
        'parameter': Param('The name of the parameter to set/get', type=str,
                           mandatory=True),
    }

    parameter_overrides = {
        'unit':      Override(mandatory=False),
    }

    def doInit(self, mode):
        self._vtype = self._adevs['device'].parameters[self.parameter].type

    def doRead(self, maxage=0):
        return getattr(self._adevs['device'], self.parameter)

    def doIsAllowed(self, value):
        try:
            self._vtype(value)
        except ValueError, err:
            return False, 'not allowed for %s.%s: %s' % \
                (self._adevs['device'], self.parameter, str(err))
        return True, ''

    def doStart(self, value):
        setattr(self._adevs['device'], self.parameter, value)

    def doStatus(self, maxage=0):
        return status.OK, ''

    def doReadUnit(self):
        devunit = getattr(self._adevs['device'], 'unit', '')
        parunit = self._adevs['device'].parameters[self.parameter].unit or ''
        if devunit:
            parunit = parunit.replace('main', devunit)
        return parunit
