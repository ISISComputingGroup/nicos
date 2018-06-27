#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
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
#   Michael Wedel <michael.wedel@esss.se>
#
# *****************************************************************************

from nicos.core import status, Param, Override, pvname
from nicos.devices.abstract import Motor, HasOffset, CanReference
from nicos_ess.devices.epics.base import EpicsAnalogMoveableEss


class EpicsMotor(CanReference, HasOffset, EpicsAnalogMoveableEss, Motor):
    """
    This device exposes some of the functionality provided by the EPICS motor
    record. The PV-names for the fields of the record (readback, speed, etc.)
    are derived by combining the motorpv-parameter with the predefined field
    names.

    The errorbitpv and reseterrorpv can be provided optionally in case the
    controller supports reporting errors and a reset-mechanism that tries to
    recover from certain errors. If present, these are used when calling the
    reset()-method.

    Another optional PV is the errormsgpv, which contains an error message that
    may originate from the motor controller or the IOC. If it is present,
    doStatus uses it for some of the status messages.
    """
    parameters = {
        'motorpv': Param('Name of the motor record PV.',
                         type=pvname, mandatory=True, settable=False),
        'errormsgpv': Param('Optional PV with error message.',
                            type=pvname, mandatory=False, settable=False),
        'errorbitpv': Param('Optional PV with error bit.',
                            type=pvname, mandatory=False, settable=False),
        'reseterrorpv': Param('Optional PV with error reset switch.',
                              type=pvname, mandatory=False, settable=False),
    }

    parameter_overrides = {
        # readpv and writepv are determined automatically from the base-PV
        'readpv': Override(mandatory=False, userparam=False, settable=False),
        'writepv': Override(mandatory=False, userparam=False, settable=False),

        # speed, limits and offset may change from outside, can't rely on cache
        'speed': Override(volatile=True),
        'offset': Override(volatile=True),
        'abslimits': Override(volatile=True),
        'userlimits': Override(volatile=True),
    }

    # Fields of the motor record with which an interaction via Channel Access
    # is required.
    motor_record_fields = {
        'readpv': 'RBV',
        'writepv': 'VAL',
        'stop': 'STOP',

        'donemoving': 'DMOV',
        'moving': 'MOVN',
        'miss': 'MISS',

        'homeforward': 'HOMF',
        'homereverse': 'HOMR',

        'speed': 'VELO',

        'offset': 'OFF',

        'highlimit': 'HLM',
        'lowlimit': 'LLM',
        'softlimit': 'LVIO',
        'lowlimitswitch': 'LLS',
        'highlimitswitch': 'HLS'
    }

    def _get_pv_parameters(self):
        """
        Implementation of inherited method to automatically account for fields
        present in motor record.
        :return: List of PV aliases.
        """
        pvs = set(self.motor_record_fields.keys())

        if self.errormsgpv:
            pvs.add('errormsgpv')

        if self.errorbitpv:
            pvs.add('errorbitpv')

        if self.reseterrorpv:
            pvs.add('reseterrorpv')

        return pvs

    def _get_pv_name(self, pvparam):
        """
        Implementation of inherited method that translates between PV aliases
        and actual PV names. Automatically adds a prefix to the PV name
        according to the motorpv parameter.
        :param pvparam: PV alias.
        :return: Actual PV name.
        """

        motor_record_prefix = getattr(self, 'motorpv')
        motor_field = self.motor_record_fields.get(pvparam)

        if motor_field is not None:
            return '.'.join((motor_record_prefix, motor_field))

        return getattr(self, pvparam)

    def doReadSpeed(self):
        return self._get_pv('speed')

    def doWriteSpeed(self, newValue):
        speed = self._get_valid_speed(newValue)

        if speed != newValue:
            self.log.warning('Selected speed %s is outside the parameter '
                             'limits, using %s instead.', newValue, speed)

        self._put_pv('speed', speed)

    def doReadOffset(self):
        return self._get_pv('offset')

    def doWriteOffset(self, value):
        # In EPICS, the offset is defined in following way:
        # USERval = HARDval + offset

        if self.offset != value:
            # Set the offset in motor record
            self._put_pv_blocking('offset', value)

            # Read the limits, values, target again
            # Reading abslimits will do the following:
            # call doReadAbslimits() [because the parameter is volatile]
            # update the internal parameter dictionary
            # transfer the value to the NICOS cache
            self.abslimits  # pylint: disable=pointless-statement

            self.log.info('The new user limits are: ' + str(self.userlimits))

    def doAdjust(self, oldvalue, newvalue):
        diff = oldvalue - newvalue
        # For EPICS the offset sign convention differs to that of the base
        # implementation.
        self.offset -= diff

    def _get_valid_speed(self, newValue):
        min_speed = self._get_pvctrl('speed', 'lower_ctrl_limit', 0.0)
        max_speed = self._get_pvctrl('speed', 'upper_ctrl_limit', 0.0)

        valid_speed = newValue
        if min_speed != 0.0:
            valid_speed = max(min_speed, valid_speed)

        if max_speed != 0.0:
            valid_speed = min(max_speed, valid_speed)

        return valid_speed

    def doRead(self, maxage=0):
        return self._get_pv('readpv')

    def doStart(self, pos):
        self._put_pv('writepv', pos)

    def doReadTarget(self):
        return self._get_pv('writepv')

    def doStatus(self, maxage=0):
        general_epics_status, _ = self._get_mapped_epics_status()
        message = self._get_status_message()

        if general_epics_status == status.ERROR:
            return status.ERROR, message or 'Unknown problem in record'

        done_moving = self._get_pv('donemoving')
        moving = self._get_pv('moving')
        if done_moving == 0 or moving != 0:
            return status.BUSY, 'Motor is moving to target...'

        miss = self._get_pv('miss')
        if miss != 0:
            return status.NOTREACHED, message or \
                   'Did not reach target position.'

        high_limitswitch = self._get_pv('highlimitswitch')
        if high_limitswitch != 0:
            return status.WARN, message or 'At high limit switch.'

        low_limitswitch = self._get_pv('lowlimitswitch')
        if low_limitswitch != 0:
            return status.WARN, message or 'At low limit switch.'

        limit_violation = self._get_pv('softlimit')
        if limit_violation != 0:
            return status.WARN, message or 'Soft limit violation.'

        return status.OK, message or 'Ready.'

    def _get_status_message(self):
        if not self.errormsgpv:
            return None

        return self._get_pv('errormsgpv', as_string=True)

    def doStop(self):
        self._put_pv('stop', 1, False)

    def doReadUserlimits(self):
        # User limits are exactly the same at the
        # EPICS HLM and LLM motor records
        usrmin = self._get_pv('lowlimit')
        usrmax = self._get_pv('highlimit')

        return usrmin, usrmax

    def doReadAbslimits(self):
        # This should be independent of the offset, and
        # as the EPICS HLM, LLM fields change with the
        # offset, it should be corrected accordingly
        absmin = self._get_pv('lowlimit') - self.offset
        absmax = self._get_pv('highlimit') - self.offset

        return absmin, absmax

    def doReference(self):
        self._put_pv_blocking('homeforward', 1)

    def doReset(self):
        if self.errorbitpv and self.reseterrorpv:
            error_bit = self._get_pv('errorbitpv')
            if error_bit == 0:
                self.log.warning(
                    'Error bit is not set, can not reset error state.')
            else:
                self._put_pv('reseterrorpv', 1)
