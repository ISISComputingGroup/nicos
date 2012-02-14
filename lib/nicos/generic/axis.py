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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS axis classes."""

__version__ = "$Revision$"

import threading
from time import sleep

from nicos.core import status, HasOffset, Override, ConfigurationError, \
     NicosError, PositionError, MoveError, waitForStatus, floatrange, Param
from nicos.abstract import Axis as BaseAxis, Motor, Coder


class Axis(BaseAxis):
    """Axis implemented in Python, with NICOS devices for motor and coders."""

    attached_devices = {
        'motor': (Motor, 'Axis motor device'),
        'coder': (Coder, 'Main axis encoder device'),
        'obs':   ([Coder], 'Auxiliary encoders used to verify position, '
                  'can be empty'),
    }

    parameter_overrides = {
        # XXX determine this from motor precision if not given
        'precision': Override(mandatory=True),
        # these are not mandatory for the axis: the motor should have them
        # defined anyway, and by default they are correct for the axis as well
        'abslimits': Override(mandatory=False),
    }

    parameters = {
        'speed':  Param('Motor speed', unit='main/s', volatile=True,
                        settable=True),
        'jitter': Param('Amount of position jitter allowed', unit='main',
                        type=floatrange(0.0, 10.0), settable=True),
    }

    def doInit(self):
        # Check that motor and unit have the same unit
        if self._adevs['coder'].unit != self._adevs['motor'].unit:
            raise ConfigurationError(self, 'different units for motor and coder'
                                     ' (%s vs %s)' % (self._adevs['motor'].unit,
                                                      self._adevs['coder'].unit))
        # Check that all observers have the same unit as the motor
        for ob in self._adevs['obs']:
            if self._adevs['motor'].unit != ob.unit:
                raise ConfigurationError(self, 'different units for motor '
                                         'and observer %s' % ob)

        self._errorstate = None
        self._posthread = None
        self._stoprequest = 0

    @property
    def motor(self):
        return self._adevs['motor']

    @property
    def coder(self):
        return self._adevs['coder']

    def doReadUnit(self):
        return self._adevs['motor'].unit

    def doReadAbslimits(self):
        # check axis limits against motor absolute limits (the motor should not
        # have user limits defined)
        if 'abslimits' in self._config:
            amin, amax = self._config['abslimits']
            mmin, mmax = self._adevs['motor'].abslimits
            if amin < mmin:
                raise ConfigurationError(self, 'absmin (%s) below the motor '
                                         'absmin (%s)' % (amin, mmin))
            if amax > mmax:
                raise ConfigurationError(self, 'absmax (%s) above the motor '
                                         'absmax (%s)' % (amax, mmax))
        else:
            mmin, mmax = self._adevs['motor'].abslimits
            amin, amax = mmin, mmax
        return amin, amax

    def doIsAllowed(self, target):
        # do limit check here already instead of in the thread
        ok, why = self._adevs['motor'].isAllowed(target + self.offset)
        if not ok:
            return ok, 'motor cannot move there: ' + why
        return True, ''

    def doStart(self, target):
        """Starts the movement of the axis to target."""
        if self._checkTargetPosition(self.read(0), target, error=False):
            return

        if self.status(0)[0] == status.BUSY:
            self.log.debug('need to stop axis first')
            self.stop()
            waitForStatus(self, errorstates=())
            #raise NicosError(self, 'axis is moving now, please issue a stop '
            #                 'command and try it again')

        if self._posthread:
            self._posthread.join()
            self._posthread = None

        self._target = target
        self._stoprequest = 0
        self._errorstate = None
        if not self._posthread:
            self._posthread = threading.Thread(None, self.__positioningThread,
                                               'Positioning thread')
            self.log.debug('start positioning thread')
            self._posthread.start()

    def doStatus(self):
        """Returns the status of the motor controller."""
        if self._errorstate:
            return (status.ERROR, str(self._errorstate))
        elif self._posthread and self._posthread.isAlive():
            return (status.BUSY, 'moving')
        else:
            return self._adevs['motor'].status(0)

    def doRead(self):
        """Returns the current position from coder controller."""
        # TODO: decide whether to re-enable this
        #if self._errorstate:
        #    errorstate = self._errorstate
        #    self._errorstate = None
        #    raise errorstate

        # XXX read() or read(0)
        return self._adevs['coder'].read() - self.offset

    def doPoll(self, i):
        devs = [self._adevs['coder'], self._adevs['motor']] + self._adevs['obs']
        for dev in devs:
            dev.poll()

    def _getReading(self):
        """Find a good value from the observers, taking into account that they
        usually have lower resolution, so we have to average of a few readings
        to get a (more) precise value.
        """
        # if coder != motor -> use coder (its more precise!)
        # if no observers, rely on coder (even if its == motor)
        if self._adevs['coder'] == self._adevs['motor'] or \
            not self._adevs['obs']:
            # read the coder
            return self._adevs['coder'].read(0)
        # XXX probably make this a parameter, could also be a par of the
        # obs-device... someone please decide!
        rounds = 100
        obs = self._adevs['obs']
        pos = sum(o.doRead() for _ in range(rounds) for o in obs)
        pos /= float(rounds * len(obs))
        return pos

    def doReset(self):
        """Resets the motor/coder controller."""
        if self.status(0)[0] != status.BUSY:
            self._errorstate = None
        self._adevs['motor'].setPosition(self._getReading())

    def doStop(self):
        """Stops the movement of the motor."""
        self._stoprequest = 1

    def doWait(self):
        """Waits until the movement of the motor has stopped and
        the target position has been reached.
        """
        # XXX add a timeout?
        waitForStatus(self, self.loopdelay, errorstates=())
        if self._errorstate:
            errorstate = self._errorstate
            self._errorstate = None
            raise errorstate

    def doWriteSpeed(self, value):
        self._adevs['motor'].speed = value

    def doReadSpeed(self):
        return self._adevs['motor'].speed

    def doWriteOffset(self, value):
        """Called on adjust(), overridden to forbid adjusting while moving."""
        if self.status(0)[0] == status.BUSY:
            raise NicosError(self, 'axis is moving now, please issue a stop '
                             'command and try it again')
        if self._errorstate:
            raise self._errorstate
        HasOffset.doWriteOffset(self, value)

    def _preMoveAction(self):
        """This method will be called before the motor will be moved.
        It should be overwritten in derived classes for special actions.

        To abort the move, raise an exception from this method.
        """

    def _postMoveAction(self):
        """This method will be called after the axis reached the position or
        will be stopped.
        It should be overwritten in derived classes for special actions.

        To signal an error, raise an exception from this method.
        """

    def _duringMoveAction(self, position):
        """This method will be called during every cycle in positioning thread.
        It should be used to do some special actions like changing shielding
        blocks, checking for air pressure etc.  It should be overwritten in
        derived classes.

        To abort the move, raise an exception from this method.
        """

    def _checkDragerror(self):
        """Check if a "drag error" occurred, i.e. the values of motor and
        coder deviate too much.  This indicates that the movement is blocked.

        This method sets the error state and returns False if a drag error
        occurs, and returns True otherwise.
        """
        diff = abs(self._adevs['motor'].read() - self._adevs['coder'].read())
        self.log.debug('motor/coder diff: %s' % diff)
        maxdiff = self.dragerror
        if maxdiff <= 0:
            return True
        if diff > maxdiff:
            self._errorstate = MoveError(
                self, 'drag error (primary coder): difference %.4g, maximum %.4g' %
                (diff, maxdiff))
            return False
        for obs in self._adevs['obs']:
            diff = abs(self._adevs['motor'].read() - obs.read())
            if diff > maxdiff:
                self._errorstate = PositionError(
                    self, 'drag error (%s): difference %.4g, maximum %.4g' %
                    (obs.name, diff, maxdiff))
                return False
        return True

    def _checkMoveToTarget(self, target, pos):
        """Check that the axis actually moves towards the target position.

        This method sets the error state and returns False if a drag error
        occurs, and returns True otherwise.
        """
        delta_last = self._lastdiff
        delta_curr = abs(pos - target)
        self.log.debug('position delta: %s, was %s' % (delta_curr, delta_last))
        # at the end of the move, the motor can slightly overshoot during
        # movement we also allow for small jitter, since airpads usually wiggle
        # a little resulting in non monotonic movement!
        ok = (delta_last >= (delta_curr - self.jitter)) or \
            delta_curr < self.precision
        # since we allow to move away a little, we want to remember the smallest
        # distance so far so that we can detect a slow crawl away from the
        # target which we would otherwise miss
        self._lastdiff = min(delta_last, delta_curr)
        if not ok:
            self._errorstate = MoveError(self,
                'not moving to target: last delta %.4g, current delta %.4g'
                % (delta_last, delta_curr))
            return False
        return True

    def _checkTargetPosition(self, target, pos, error=True):
        """Check if the axis is at the target position.

        This method returns False if not arrived at target, or True otherwise.
        """
        diff = abs(pos - target)
        prec = self.precision
        if (prec > 0 and diff >= prec) or (prec == 0 and diff):
            if error:
                self._errorstate = MoveError(self,
                    'precision error: difference %.4g, precision %.4g' %
                    (diff, self.precision))
            return False
        maxdiff = self.dragerror
        for obs in self._adevs['obs']:
            diff = abs(target - obs.read())
            if maxdiff > 0 and diff > maxdiff:
                if error:
                    self._errorstate = PositionError(self,
                        'precision error (%s): difference %.4g, maximum %.4g' %
                        (obs, diff, maxdiff))
                return False
        return True

    def _setErrorState(self, cls, text):
        self._errorstate = cls(self, text)
        self.log.error(text)
        return False

    def __positioningThread(self):
        try:
            self._preMoveAction()
        except Exception, err:
            self._setErrorState(MoveError, 'error in pre-move action: %s' % err)
        else:
            target = self._target
            self._errorstate = None
            if self.backlash:
                backlash = self.backlash
                lastpos = self.read(0)
                # make sure not to move twice if coming from the side in the
                # direction of the backlash
                if backlash > 0 and lastpos < target + backlash:
                    positions = [target + backlash, target]
                elif backlash < 0 and lastpos > target + backlash:
                    positions = [target + backlash, target]
                else:
                    positions = [target]
                for pos in positions:
                    self.__positioning(pos)
                    if self._stoprequest == 2 or self._errorstate:
                        break
            else:
                try:
                    self.__positioning(target)
                except Exception, err:
                    self._setErrorState(MoveError,
                                        'error in positioning: %s' % err)
            try:
                self._postMoveAction()
            except Exception, err:
                self._setErrorState(MoveError,
                                    'error in post-move action: %s' % err)

    def __positioning(self, target):
        moving = False
        offset = self.offset
        tries = self.maxtries
        self._adevs['motor'].start(target + offset)
        moving = True
        self._lastdiff = abs(target - self.read(0))

        while moving:
            if self._stoprequest == 1:
                self.log.debug('stopping motor')
                self._adevs['motor'].stop()
                self._stoprequest = 2
                continue
            sleep(self.loopdelay)
            # poll accurate current values and status of child devices so that
            # we can use read() and status() subsequently
            st, pos = self.poll()
            mstatus = self._adevs['motor'].status()[0]
            if mstatus != status.BUSY:
                # motor stopped; check why
                if self._stoprequest == 2:
                    self.log.debug('stop requested, leaving positioning')
                    # manual stop
                    moving = False
                elif self._checkTargetPosition(target, pos):
                    self.log.debug('target reached, leaving positioning')
                    # target reached
                    moving = False
                elif mstatus == status.ERROR:
                    # motor in error state -> try resetting
                    newstatus = self._adevs['motor'].reset()
                    # if that failed, stop immediately
                    if newstatus[0] == status.ERROR:
                        moving = False
                        self._setErrorState(MoveError,
                            'motor in error state: %s' % newstatus[1])
                elif tries > 0:
                    if tries == 1:
                        self.log.warning('last try: %s' % self._errorstate)
                    else:
                        self.log.debug('target not reached, retrying: %s' %
                                       self._errorstate)
                    self._errorstate = None
                    # target not reached, get the current position, set the
                    # motor to this position and restart it. _getReading is the
                    # 'real' value, may ask the coder again (so could slow
                    # down!)
                    self._adevs['motor'].setPosition(self._getReading())
                    self._adevs['motor'].start(target + self.offset)
                    tries -= 1
                else:
                    moving = False
                    self._setErrorState(MoveError,
                        'target not reached after %d tries: %s' %
                        (self.maxtries, self._errorstate))
            elif not self._checkMoveToTarget(target, pos):
                self.log.debug('stopping motor because not moving to target')
                self._adevs['motor'].stop()
                # should now go into next try
            elif not self._checkDragerror():
                self.log.debug('stopping motor due to drag error')
                self._adevs['motor'].stop()
                # should now go into next try
            elif self._stoprequest == 0:
                try:
                    self._duringMoveAction(pos)
                except Exception, err:
                    self._setErrorState(MoveError,
                                        'error in during-move action: %s' % err)
                    self._stoprequest = 1
