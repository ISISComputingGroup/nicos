#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
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
#   Alexander Lenz <alexander.lenz@frm2.tum.de>
#
# *****************************************************************************

"""
This module contains the NICOS - TANGO integration.

All NICOS - TANGO devices only support devices which fulfill the official
FRM-II/JCNS TANGO interface for the respective device classes.
"""

import PyTango

from nicos.core import Param, Override, status, Readable, Moveable, Measurable,\
    HasLimits, Device, tangodev, HasCommunication, oneofdict, dictof, intrange, \
    nonemptylistof, NicosError, CommunicationError, ConfigurationError
from nicos.devices.abstract import Coder, Motor as NicosMotor, CanReference
from nicos.utils import HardwareStub
from nicos.core import SIMULATION

# Only export Nicos devices for 'from nicos.device.tango import *'
__all__ = [
    'AnalogInput', 'Sensor', 'AnalogOutput', 'Actuator', 'Motor',
    'TemperatureController', 'DigitalInput', 'DigitalOutput', 'StringIO'
]

DEFAULT_STATUS_MAPPING = {
    PyTango.DevState.ON:     status.OK,
    PyTango.DevState.ALARM:  status.WARN,
    PyTango.DevState.OFF:    status.ERROR,
    PyTango.DevState.FAULT:  status.ERROR,
    PyTango.DevState.MOVING: status.BUSY,
}

EXC_MAPPING = {
    PyTango.CommunicationFailed: CommunicationError,
    PyTango.WrongNameSyntax: ConfigurationError,
    PyTango.DevFailed: NicosError,
    # when a DeviceProxy is created with the device not exported,
    # access to the named commands/attributes will raise AttributeError
    AttributeError: CommunicationError,
}


class PyTangoDevice(HasCommunication):
    """
    Basic PyTango device.

    The PyTangoDevice uses an internal PyTango.DeviceProxy but wraps command
    execution and attribute operations with logging and exception mapping.
    """

    parameters = {
        'tangodevice': Param('Tango device name', type=tangodev,
                             mandatory=True, preinit=True),
    }

    def doPreinit(self, mode):
        # Wrap PyTango client creation (so even for the ctor, logging and
        # exception mapping is enabled).
        self._createPyTangoDevice = self._applyGuardToFunc(
            self._createPyTangoDevice, 'constructor')

        self._dev = None

        # Don't create PyTango device in simulation mode
        if mode != SIMULATION:
            self._dev = self._createPyTangoDevice(self.tangodevice)

    def doStatus(self, maxage=0, mapping=DEFAULT_STATUS_MAPPING):  # pylint: disable=W0102
        # Query status code and string
        tangoState = self._dev.State()
        tangoStatus = self._dev.Status()

        # Map status
        nicosState = mapping.get(tangoState, status.UNKNOWN)

        return (nicosState, tangoStatus)

    def doVersion(self):
        return [(self.tangodevice, self._dev.version)]

    def doReset(self):
        self._dev.Reset()
        # XXX do we need to "if isOff(): On()" dance?

    def _setMode(self, mode):
        super(PyTangoDevice, self)._setMode(mode)
        # remove the Tango device on entering simulation mode, to prevent
        # accidental access to the hardware
        if mode == SIMULATION:
            self._dev = HardwareStub(self)

    def _getProperty(self, name, dev=None):
        """
        Utility function for getting a property by name easily.
        """
        if dev is None:
            dev = self._dev
        return dev.GetProperties((name, 'device'))[2]

    def _createPyTangoDevice(self, address):  # pylint: disable=E0202
        """
        Creates the PyTango DeviceProxy and wraps command execution and
        attribute operations with logging and exception mapping.
        """
        device = PyTango.DeviceProxy(address)
        return self._applyGuardsToPyTangoDevice(device)

    def _applyGuardsToPyTangoDevice(self, dev):
        """
        Wraps command execution and attribute operations of the given
        device with logging and exception mapping.
        """
        dev.command_inout = self._applyGuardToFunc(dev.command_inout)
        dev.write_attribute = self._applyGuardToFunc(dev.write_attribute,
                                                     'attr_write')
        dev.read_attribute = self._applyGuardToFunc(dev.read_attribute,
                                                    'attr_read')
        dev.attribute_query = self._applyGuardToFunc(dev.attribute_query,
                                                     'attr_query')
        return dev

    def _applyGuardToFunc(self, func, category='cmd'):
        """
        Wrap given function with logging and exception mapping.
        """
        def wrap(*args, **kwds):
            # handle different types for better debug output
            if category == 'cmd':
                self.log.debug('[PyTango] command: %s%r' % (args[0], args[1:]))
            elif category == 'attr_read':
                self.log.debug('[PyTango] read attribute: %s' % args[0])
            elif category == 'attr_write':
                self.log.debug('[PyTango] write attribute: %s => %r'
                               % (args[0], args[1:]))
            elif category == 'attr_query':
                self.log.debug('[PyTango] query attribute properties: %s' %
                               args[0])
            elif category == 'constructor':
                self.log.debug('[PyTango] device creation: %s' % args[0])
            elif category == 'internal':
                self.log.debug('[PyTango integration] internal: %s%r'
                               % (func.__name__, args))
            else:
                self.log.debug('[PyTango] call: %s%r'
                               % (func.__name__, args))

            return self._com_retry(args[0] if args else None,
                                   func, *args, **kwds)

        # hide the wrapping
        wrap.__name__ = func.__name__

        return wrap

    def _com_return(self, result, info):
        if isinstance(result, PyTango.DeviceAttribute):
            self.log.debug('\t=> %s' % repr(result.value)[:300])
        else:
            # This line explicitly logs '=> None' for commands which
            # does not return a value. This indicates that the command
            # execution ended.
            self.log.debug('\t=> %s' % repr(result)[:300])
        return result

    def _tango_exc_desc(self, err):
        exc = str(err)
        if err.args:
            exc = err.args[0]  # Can be str or DevError
            if isinstance(exc, PyTango.DevError):
                # reduce Python tracebacks
                if '\n' in exc.origin and 'File ' in exc.origin:
                    origin = exc.origin.splitlines()[-2].strip()
                else:
                    origin = exc.origin.strip()
                exc = '%s: %s in %s' % (exc.reason.strip(),
                                        exc.desc.strip(),
                                        origin)
        return exc

    def _tango_exc_reason(self, err):
        if err.args:
            exc = err.args[0]
            if isinstance(exc, PyTango.DevError):
                return exc.reason.strip()
        return ''

    def _com_warn(self, retries, name, err, info):
        if self._tango_exc_reason(err) in ['Entangle_ConfigurationError',
                                           'Entangle_UnrecognizedHardware',
                                           'Entangle_WrongAPICall',
                                           'Entangle_InvalidValue',
                                           'Entangle_NotSupported',
                                           'Entangle_ProgrammingError',
                                           'DB_DeviceNotDefined',
                                           'API_DeviceNotDefined',
                                           'API_CantConnectToDatabase',
                                           'API_TangoHostNotSet',
                                           'API_ServerNotRunning',
                                           'API_DeviceNotExported',
                                           ]:
            self._com_raise(err, info)
        if retries == self.comtries - 1:
            self.log.warning('%s failed, retrying up to %d times: %s' %
                             (info, retries, self._tango_exc_desc(err)))

    def _com_raise(self, err, info):
        exc = self._tango_exc_desc(err)
        self.log.debug('PyTango error: %s' % exc)
        raise EXC_MAPPING.get(type(err), NicosError)(self, exc)


class AnalogInput(PyTangoDevice, Readable):
    """
    Represents the client to a TANGO AnalogInput device.
    """

    valuetype = float
    parameter_overrides = {
        'unit': Override(mandatory=False),
    }

    def doReadUnit(self):
        attrInfo = self._dev.attribute_query('value')
        return attrInfo.unit

    def doRead(self, maxage=0):
        return self._dev.value


class Sensor(AnalogInput, Coder):
    """
    Represents the client to a TANGO Sensor device.
    """

    def doSetPosition(self, value):
        self._dev.Adjust(value)


class AnalogOutput(PyTangoDevice, HasLimits, Moveable):
    """
    Represents the client to a TANGO AnalogOutput device.
    """

    valuetype = float
    parameter_overrides = {
        'abslimits': Override(mandatory=False),
        'unit':      Override(mandatory=False),
    }

    def doReadUnit(self):
        attrInfo = self._dev.attribute_query('value')
        return attrInfo.unit

    def doReadAbslimits(self):
        absmin = float(self._getProperty('absmin'))
        absmax = float(self._getProperty('absmax'))

        return (absmin, absmax)

    def doRead(self, maxage=0):
        return self._dev.value

    def doStart(self, value):
        self._dev.value = value

    def doStop(self):
        self._dev.Stop()


class Actuator(AnalogOutput, NicosMotor):
    """
    Represents the client to a TANGO Actuator device.
    """

    parameter_overrides = {
        'speed':  Override(volatile=True),
    }

    def doReadSpeed(self):
        return self._dev.speed

    def doWriteSpeed(self, value):
        self._dev.speed = value

    def doSetPosition(self, value):
        self._dev.Adjust(value)


class Motor(CanReference, Actuator):
    """
    Represents the client to a TANGO Motor device.
    """

    parameters = {
        'refpos': Param('Reference position', type=float, unit='main'),
        'accel':  Param('Acceleration', type=float, settable=True, volatile=True),
        'decel':  Param('Deceleration', type=float, settable=True, volatile=True),
    }

    def doReadRefpos(self):
        return float(self._getProperty('refpos'))

    def doReadAccel(self):
        return self._dev.accel

    def doWriteAccel(self, value):
        self._dev.accel = value

    def doReadDecel(self):
        return self._dev.decel

    def doWriteDecel(self, value):
        self._dev.decel = value

    def doReference(self):
        self._setROParam('target', None)  # don't check target in wait() below
        self._dev.Reference()
        self.wait()


class TemperatureController(Actuator):
    """
    Represents the client to a TANGO TemperatureController device.
    """

    parameters = {
        'p':            Param('Proportional control parameter', type=float,
                              settable=True, category='general', chatty=True,
                              volatile=True),
        'i':            Param('Integral control parameter', type=float,
                              settable=True, category='general', chatty=True,
                              volatile=True),
        'd':            Param('Derivative control parameter', type=float,
                              settable=True, category='general', chatty=True,
                              volatile=True),
        'setpoint':     Param('Current setpoint', type=float, category='general',
                              volatile=True),
        'heateroutput': Param('Heater output', type=float, category='general',
                              volatile=True),
    }

    def doReadP(self):
        return self._dev.p

    def doWriteP(self, value):
        self._dev.p = value

    def doReadI(self):
        return self._dev.i

    def doWriteI(self, value):
        self._dev.i = value

    def doReadD(self):
        return self._dev.d

    def doWriteD(self, value):
        self._dev.d = value

    def doReadSetpoint(self):
        return self._dev.setpoint

    def doReadHeateroutput(self):
        return self._dev.heaterOutput

    def doPoll(self, n, maxage):
        if self.speed:
            self._pollParam('heateroutput', 1)
        else:
            self._pollParam('heateroutput', 60)
        self._pollParam('setpoint')
        self._pollParam('p')
        self._pollParam('i')
        self._pollParam('d')


class DigitalInput(PyTangoDevice, Readable):
    """
    Represents the client to a TANGO DigitalInput device.
    """

    valuetype = int
    parameter_overrides = {
        'unit': Override(mandatory=False),
    }

    def doRead(self, maxage=0):
        return self._dev.value


class NamedDigitalInput(DigitalInput):
    """A DigitalInput with numeric values mapped to names."""

    parameters = {
        'mapping': Param('A dictionary mapping state names to integers',
                         type=dictof(str, int)),
    }

    def doInit(self, mode):
        self._reverse = dict((v, k) for (k, v) in self.mapping.items())

    def doRead(self, maxage=0):
        value = self._dev.value
        return self._reverse.get(value, value)


class PartialDigitalInput(NamedDigitalInput):
    """Base class for a TANGO DigitalInput with only a part of the full
    bit width accessed.
    """

    parameters = {
        'startbit': Param('Number of the first bit', type=int, default=0),
        'bitwidth': Param('Number of bits', type=int, default=1),
    }

    def doInit(self, mode):
        NamedDigitalInput.doInit(self, mode)
        self._mask = (1 << self.bitwidth) - 1

    def doRead(self, maxage=0):
        raw_value = self._dev.value
        value = (raw_value >> self.startbit) & self._mask
        return self._reverse.get(value, value)


class DigitalOutput(PyTangoDevice, Moveable):
    """
    Represents the client to a TANGO DigitalOutput device.
    """

    valuetype = int
    parameter_overrides = {
        'unit': Override(mandatory=False),
    }

    def doRead(self, maxage=0):
        return self._dev.value

    def doStart(self, value):
        self._dev.value = self.valuetype(value)


class NamedDigitalOutput(DigitalOutput):
    """A DigitalOutput with numeric values mapped to names."""

    parameters = {
        'mapping': Param('A dictionary mapping state names to integer values',
                         type=dictof(str, int), mandatory=True),
    }

    def doInit(self, mode):
        self._reverse = dict((v, k) for (k, v) in self.mapping.items())
        # oneofdict: allows both types of values (string/int), but normalizes
        # them into the string form
        self.valuetype = oneofdict(self._reverse)

    def doStart(self, target):
        value = self.mapping.get(target, target)
        self._dev.value = value

    def doRead(self, maxage=0):
        value = self._dev.value
        return self._reverse.get(value, value)


class PartialDigitalOutput(NamedDigitalOutput):
    """Base class for a TANGO DigitalOutput with only a part of the full
    bit width accessed.
    """

    parameters = {
        'startbit': Param('Number of the first bit', type=int, default=0),
        'bitwidth': Param('Number of bits', type=int, default=1),
    }

    def doInit(self, mode):
        NamedDigitalOutput.doInit(self, mode)
        self._mask = (1 << self.bitwidth) - 1
        self.valuetype = intrange(0, self._mask)

    def doRead(self, maxage=0):
        raw_value = self._dev.value
        value = (raw_value >> self.startbit) & self._mask
        return self._reverse.get(value, value)

    def doStart(self, target):
        value = self.mapping.get(target, target)
        curvalue = self._dev.value
        newvalue = (curvalue & ~(self._mask << self.startbit)) | \
                   (value << self.startbit)
        self._dev.value = self.valuetype(newvalue)

    def doIsAllowed(self, target):
        value = self.mapping.get(target, target)
        if value < 0 or value > self._mask:
            return False, '%d outside range [0,%d]' % (value, self._mask)
        return True, ''


class StringIO(PyTangoDevice, Device):
    """
    Represents the client to a TANGO StringIO device.
    """

    parameters = {
        'bustimeout':  Param('Communication timeout', type=float,
                             settable=True, unit='s'),
        'endofline':   Param('End of line', type=str, settable=True),
        'startofline': Param('Start of line', type=str, settable=True),
    }

    def doReadBustimeout(self):
        return self._dev.communicationTimeout

    def doWriteBustimeout(self, value):
        self._dev.communicationTimeout = value

    def doReadEndofline(self):
        return self._dev.endOfLine

    def doWriteEndofline(self, value):
        self._dev.endOfLine = value

    def doReadStartofline(self):
        return self._dev.startOfLine

    def doWriteStartofline(self, value):
        self._dev.startOfLine = value

    def communicate(self, value):
        return self._dev.Communicate(value)

    def flush(self):
        self._dev.Flush()

    def read(self, value):
        return self._dev.Read(value)

    def write(self, value):
        return self._dev.Write(value)

    def readLine(self):
        return self._dev.ReadLine()

    def writeLine(self, value):
        return self._dev.WriteLine(value)

    def multiCommunicate(self, value):
        return self._dev.MultiCommunicate(value)

    @property
    def availablechars(self):
        return self._dev.availableChars

    @property
    def availablelines(self):
        return self._dev.availableLines


class Detector(PyTangoDevice, Measurable):
    """
    Represents the client to a TANGO detector device.
    """

    parameters = {
        'size': Param('Detector size',
                      type=nonemptylistof(int), unit='', settable=False,
                      volatile=True,
                     ),
        'roioffset': Param('ROI offset',
                           type=nonemptylistof(int), unit='', mandatory=False,
                           volatile=True,
                          ),
        'roisize': Param('ROI size',
                         type=nonemptylistof(int), unit='', mandatory=False,
                         volatile=True,
                        ),
        'binning': Param('Binning',
                         type=nonemptylistof(int), unit='', mandatory=False,
                         volatile=True,
                        ),
        'zeropoint': Param('Zero point',
                           type=nonemptylistof(int), unit='', settable=False,
                           mandatory=False, volatile=True,
                          ),
    }

    def doReadSize(self):
        return self._dev.detectorSize.tolist()

    def doReadRoioffset(self):
        return self._dev.roiOffset.tolist()

    def doWriteRoioffset(self, value):
        self._dev.roiOffset = value

    def doReadRoisize(self):
        return self._dev.roiSize.tolist()

    def doWriteRoisize(self, value):
        self._dev.roiSize = value

    def doReadBinning(self):
        return self._dev.binning.tolist()

    def doWriteBinning(self, value):
        self._dev.binning = value

    def doReadZeropoint(self):
        return self._dev.zeroPoint.tolist()

    def doRead(self, maxage=0):
        return self._dev.value.tolist()

    def presetInfo(self):
        return set(['t', 'time', 'm', 'monitor', ])

    def doSetPreset(self, **preset):
        self.doStop()
        if 't' in preset:
            self._dev.syncMode = 'time'
            self._dev.syncValue = preset['t']
        elif 'time' in preset:
            self._dev.syncMode = 'time'
            self._dev.syncValue = preset['time']
        elif 'm' in preset:
            self._dev.syncMode = 'monitor'
            self._dev.syncValue = preset['m']
        elif 'monitor' in preset:
            self._dev.syncMode = 'monitor'
            self._dev.syncValue = preset['monitor']

    def doStart(self):
        self._dev.Start()

    def doStop(self):
        self._dev.Stop()

    def doResume(self):
        self._dev.Resume()

    def doPause(self):
        self.doStop()
        return True

    def doIsCompleted(self):
        return self.doStatus()[0] not in (status.BUSY,)

    def doPrepare(self):
        self._dev.Prepare()

    def doClear(self):
        self._dev.Clear()


class TofDetector(Detector):
    """
    Represents the client to a TANGO time-of-flight detector device.
    """

    parameters = {
        'delay': Param('Delay',
                       type=int, unit='ns', default=0, volatile=True,
                      ),
        'timechannels': Param('Number of time channels',
                              type=int, default=1, volatile=True,
                             ),
        'timeinterval': Param('Time for each time channel',
                              type=int, unit='ns', default=1, volatile=True,
                             ),
    }

    def doReadTimechannels(self):
        return self._dev.timeChannels

    def doWriteTimechannels(self, value):
        self._dev.timeChannels = value

    def doReadDelay(self):
        return self._dev.delay

    def doWriteDelay(self, value):
        self._dev.delay = value

    def doReadTimeinterval(self):
        return self._dev.timeInterval

    def doWriteTimeinterval(self, value):
        self._dev.timeInterval = value

    def presetInfo(self):
        return set(['t', 'time', 'm', 'monitor', 'c', 'cycles', ])

    def doSetPreset(self, **preset):
        self.doStop()
        if 't' in preset:
            self._dev.syncMode = 'time'
            self._dev.syncValue = preset['t']
        elif 'time' in preset:
            self._dev.syncMode = 'time'
            self._dev.syncValue = preset['time']
        elif 'm' in preset:
            self._dev.syncMode = 'monitor'
            self._dev.syncValue = preset['m']
        elif 'monitor' in preset:
            self._dev.syncMode = 'monitor'
            self._dev.syncValue = preset['monitor']
        elif 'c' in preset:
            self._dev.syncMode = 'cycles'
            self._dev.syncValue = preset['c']
        elif 'cycles' in preset:
            self._dev.syncMode = 'cycles'
            self._dev.syncValue = preset['cycles']
