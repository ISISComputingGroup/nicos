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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

"""Support code for the CCR-Taco-Boxes"""

from nicos.core import Moveable, HasLimits, Override, Param, SIMULATION, \
     ConfigurationError, InvalidValueError, ProgrammingError, oneof, floatrange
from nicos.utils import lazy_property

class CCRControl(HasLimits, Moveable):
    """Class implementing requirements from SE-group

    requirements are:

    * no setpoint change without ramp
    * ramp is limited to 10K/min
    * above 300K, the CCR/coldhead/transfer point stays at 300K,
      while the stick regulates.

    """
    attached_devices = dict(
        stick = (Moveable, "Temperaturecontroller for the stick"),
        tube = (Moveable, "Temperaturecontroller for the outer ccr/tube"),
    )

    parameters = dict(
        regulationmode = Param('Preferred regulation point: stick or tube',
                               unit='', type=oneof('stick', 'tube', 'both'),
                               settable=True, chatty=True, category='general'),
        ramp  = Param('Temperature ramp in K/min', unit='K/min', chatty=True,
                      type=floatrange(0.0001, 10), settable=True, volatile=True),
        setpoint = Param('Current temperature setpoint', unit='main',
                         category='general'),
    )

    parameter_overrides = dict(
        unit = Override(default='K', type=oneof('K'), settable=False,
                        mandatory=False),
        abslimits = Override(mandatory=False),
    )

    @lazy_property
    def stick(self):
        return self._adevs['stick']

    @lazy_property
    def tube(self):
        return self._adevs['tube']

    def doInit(self, mode):
        if mode != SIMULATION:
            if self.stick is None or self.tube is None:
                raise ConfigurationError(self, 'Both stick and tube needs to '
                                          'be set for this device!')
            absmin = min(self.tube.absmin, self.stick.absmin)
            absmax = self.stick.absmax
            self._setROParam('abslimits', (absmin, absmax))

    def __start_tube_stick(self, tubetarget, sticktarget):
        ok, why = self.tube.isAllowed(tubetarget)
        if not ok:
            raise InvalidValueError(self, why)
        ok, why = self.stick.isAllowed(sticktarget)
        if not ok:
            raise InvalidValueError(self, why)
        self.log.debug('Moving %s to %r and %s to %r' %
                       (self.tube.name, tubetarget, self.stick, sticktarget))
        try:
            self.tube.start(tubetarget)
        finally:
            self.stick.start(sticktarget)

    def doStart(self, target):
        """Changes the intended setpoint

        Logic is as follows:
        if target is below absmax of the tube, let regulation mode decide if we
        move the stick or the tube or both. The unused one is switched off by
        moving to its absmin value or 0, whatever is bigger.

        If target is above absmax of the tube, we set tube to its absmax and
        the stick to the target. In this case, mode is ignored.

        Normally the absmax of the tube is set to 300K, which is compatible
        with requirements from the SE-group.
        """
        if target < self.tube.absmax:
            if self.regulationmode == 'stick':
                self.__start_tube_stick(max(self.tube.absmin, 0), target)
            elif self.regulationmode == 'tube':
                self.__start_tube_stick(target, max(self.stick.absmin, 0))
            elif self.regulationmode == 'both':
                self.__start_tube_stick(max(self.tube.absmin, target),
                                        max(self.stick.absmin, target))
            else:
                raise ProgrammingError(self, 'unknown mode %r, don\'t know how'
                                        ' to handle it!' % self.regulationmode)
        else:
            self.log.debug('ignoring mode, as target %r is above %s.absmax' %
                            (target, self.tube.name))
            self.__start_tube_stick(self.tube.absmax, target)

    def doRead(self, maxage=0):
        if self.stick.target is not None:
            if self.stick.target >= self.tube.absmax:
                return self.stick.read(maxage)
        if self.regulationmode in ('stick', 'both'):
            return self.stick.read(maxage)
        elif self.regulationmode == 'tube':
            return self.tube.read(maxage)
        else:
            raise ProgrammingError(self, 'unknown mode %r, don\'t know how to '
                                    'handle it!' % self.regulationmode)

    def doPoll(self, n):
        if n % 50 == 0:
            self._pollParam('setpoint', 60)

    #
    # Parameters
    #

    def __set_param(self, attrname, value):
        self.log.debug('Setting param %s to %r' % (attrname, value))
        setattr(self.tube, attrname, value)
        setattr(self.stick, attrname, value)

    def __get_param(self, attrname):
        # take first match
        tubeval = getattr(self.tube, attrname)
        stickval = getattr(self.stick, attrname)
        if tubeval == stickval:
            res = tubeval
        else:
            self.log.warning('%s.%s (%r) != %s.%s (%r), please set %s.%s to '
                             'the desired value!' %
                             (self.tube.name, attrname, tubeval,
                              self.stick.name, attrname, stickval,
                              self.name, attrname))
            # try to take the 'more important' one
            if self.stick.target is not None and \
               self.stick.target > self.tube.absmax:
                res = stickval
            else:
                if self.regulationmode == 'stick':
                    res = stickval
                elif self.regulationmode == 'tube':
                    res = tubeval
                else:
                    raise ConfigurationError(self, 'Parameters %s.%s and %s.%s'
                                              ' differ! please set them using '
                                              '%s.%s only.' % (
                                              self.tube.name, attrname,
                                              self.stick.name, attrname,
                                              self.name, attrname))

        self.log.debug('param %s is %r' % (attrname, res))
        return res

    def doReadRamp(self):
        # do not return a value the validator would reject, or device creation fails
        ramp = self.__get_param('ramp')
        # this works only for the floatrange type of the ramp parameter!
        rampmin = self.parameters['ramp'].type.fr
        rampmax = self.parameters['ramp'].type.to
        if rampmin <= ramp <= rampmax:
            return ramp
        clampramp = max(min(ramp, rampmax), rampmin)
        self.log.warning('Ramp parameter %.3g is outside of the allowed range '
                         '%.3g..%.3g, setting it to %.3g' % (
                         ramp, rampmin, rampmax, clampramp ))
        # clamp read value to allowed range and re-set it
        return self.doWriteRamp(clampramp)

    def doWriteRamp(self, value):
        self.__set_param('ramp', value)
        return self.__get_param('ramp')

    def doWriteRegulationmode(self, value):
        self.log.info('To use the new regulationmode %r, please start/move %s...' %
                       (value, self.name))

    def doReadSetpoint(self):
        if self.stick.target is not None:
            if self.stick.target >= self.tube.absmax:
                return self.stick.setpoint
        # take the more important one, closer to the sample.
        if self.regulationmode in ('stick', 'both'):
            return self.stick.setpoint
        elif self.regulationmode == 'tube':
            return self.tube.setpoint
        else:
            raise ProgrammingError(self, 'unknown mode %r, don\'t know how to '
                                   'handle it!' % self.regulationmode)
