# -*- coding: utf-8 -*-
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
#   Christian Felder <c.felder@fz-juelich.de>
#
# *****************************************************************************

# standard library
import time
# third party
import numpy
from PyTango import DevState, CommunicationFailed
# local library
import nicos.core.status as status
from nicos.core.device import Moveable
from nicos.devices.tango import PyTangoDevice, \
DEFAULT_STATUS_MAPPING as DEFAULT_MAP_TANGO_STATUS
from nicos.core.params import Param, Override, oneof, tupleof
from nicos.core.errors import NicosError, CommunicationError
from nicos.devices.generic.sequence import MeasureSequencer, SeqDev, SeqSleep
from nicos.core.image import ImageProducer, ImageType


__author__ = "Christian Felder <c.felder@fz-juelich.de>"
__date__ = "2014-06-06"
__version__ = "0.2.0"


class ShutterStates(object):
    """Shutter constants for opening and closing shutters."""

    OPEN = "open"
    CLOSED = "closed"


class ImagePlateBase(PyTangoDevice):
    """Basic Tango Device for MAATEL Image Plate Detectors."""

    DEFAULT_URL_FMT = "tango://%s/EMBL/Microdiff/General#dbase=no"
    MAP_STATUS = dict(DEFAULT_MAP_TANGO_STATUS)
    MAP_STATUS[DevState.STANDBY] = status.OK
    MAP_STATUS[DevState.ALARM] = status.ERROR

    def doStatus(self, maxage=0, mapping=MAP_STATUS): # pylint: disable=W0102
        return PyTangoDevice.doStatus(self, maxage, mapping)


class ImagePlateDrum(ImagePlateBase, Moveable):
    """ImagePlateDrum implements erasing, moving to expo position and readout
    for MAATEL Image Plate Detectors."""

    POS_ERASE = "erase"
    POS_EXPO = "expo"
    POS_READ = "read"

    valuetype = oneof(POS_ERASE, POS_EXPO, POS_READ)

    parameters = {
                  "drumpos": Param("Drum position in degree", type=float,
                                        settable=True, volatile=True,
                                        category="general"),
                  "readheadpos": Param("Read head motor position in mm",
                                       type=float, settable=True, volatile=True,
                                       category="general"),
                  "drumexpo": Param("Drum expo position in degree",
                                    type=float, settable=True, volatile=True,
                                    category="general"),
                  "readspeed": Param("Readout velocity for the detector drum " +
                                    "in rpm", type=float, settable=True,
                                    volatile=True, category="general"),
                  "erasespeed": Param("Erase velocity for the detector drum " +
                                      "in rpm", type=float, settable=True,
                                      volatile=True, category="general"),
                  "freqlaser": Param("Frequency for the laser diode in Hz",
                                     type=float, settable=True, volatile=True,
                                     category="general"),
                  "timeerase": Param("Erasure time in seconds", type=float,
                                     settable=True, volatile=True,
                                     category="general"),
                  }

    parameter_overrides = {"unit": Override(default="", mandatory=False,
                                            settable=False)
                           }

    def doInit(self, mode):
        self._moveTo = None
        self._mapStart = {
                      ImagePlateDrum.POS_ERASE: self._dev.StartErasureProcess,
                      ImagePlateDrum.POS_EXPO: self._dev.MoveExpoPosition,
                      ImagePlateDrum.POS_READ: self._dev.StartReadProcess,
                      }
        self._mapStop = {
                      ImagePlateDrum.POS_ERASE: self._dev.AbortErasureProcess,
                      ImagePlateDrum.POS_EXPO: self._dev.AbortExposureProcess,
                      ImagePlateDrum.POS_READ: self._dev.AbortReadProcess,
                      }

    def doStart(self, pos):
        self.log.debug("doStart: pos: %s" % pos)
        self._moveTo = pos
        self._mapStart[pos]()
        if pos == ImagePlateDrum.POS_READ:
            # temporary fix because the tango status is not updated instantly
            myStatus = self.status(0)
            self.log.debug("DRUM STATUS: %d, %s" % (myStatus[0], myStatus[1]))
            self.log.debug("sleep 1 second")
            time.sleep(1)
            self.log.debug("sleeping done")
            myStatus = self.status(0)
            self.log.debug("DRUM STATUS: %d, %s" % (myStatus[0], myStatus[1]))

    def doStop(self):
        self.log.debug("doStop")
        if self._moveTo in self._mapStop:
            self._mapStop[self._moveTo]()
        else:
            myStatus = self.status(0)
            if myStatus[0] == status.OK:
                self.log.warning("Device already stopped.")
            else:
                raise NicosError(self, "Internal moveTo state unknown. " +
                                 "Check device status.")

    def doRead(self, maxage=0):
        return self.target

    def doIsAllowed(self, pos):
        self.log.debug("doIsAllowed: pos: %s" % pos)
        myStatus = self.status(0)
        if myStatus[0] == status.OK:
            return (True, None)
        else:
            return (False, "Movement not allowed during device status '%s'"
                    % (myStatus[0]))

    def doWait(self):
        Moveable.doWait(self)
        self._moveTo = None

    def doReadDrumpos(self):
        return self._dev.DrumPosition

    def doReadReadheadpos(self):
        return self._dev.ReadHeadPosition

    def doReadDrumexpo(self):
        return self._dev.DrumExpoPosition

    def doReadReadspeed(self):
        return self._dev.ReadingDrumJogSpeed

    def doReadErasespeed(self):
        return self._dev.ErasureDrumJogSpeed

    def doReadFreqlaser(self):
        return self._dev.LaserDiodeLevel

    def doReadTimeerase(self):
        return self._dev.ErasureDuration

    def doWriteDrumpos(self, value):
        self._dev.DrumPosition = value

    def doWriteReadheadpos(self, value):
        self._dev.ReadHeadPosition = value

    def doWriteDrumexpo(self, value):
        self._dev.DrumExpoPosition = value

    def doWriteReadspeed(self, value):
        self._dev.ReadingDrumJogSpeed = value

    def doWriteErasespeed(self, value):
        self._dev.ErasureDrumJogSpeed = value

    def doWriteFreqlaser(self, value):
        self._dev.LaserDiodeLevel = value

    def doWriteTimeerase(self, value):
        self._dev.ErasureDuration = value


class ImagePlateDetector(MeasureSequencer, ImagePlateBase, ImageProducer):
    """Represents the client to a MAATEL Image Plate Detector."""

    MAP_SHAPE = {
                 125: (10000, 900),
                 250: (5000, 900),
                 500: (2500, 900),
                 }

    attached_devices = {
                        "imgdrum": (Moveable, "Image Plate Detector Drum " +
                                    "control device."),
                        "gammashutter": (Moveable, "Gamma shutter"),
                        "photoshutter": (Moveable, "Photo shutter"),
                        }

    parameters = {
                  "erase": Param("Erase image plate on next start?", type=bool,
                                 settable=True, mandatory=False, default=True),
                  "ctrl_gammashutter": Param("Control gamma shutter?",
                                             type=bool, settable=True,
                                             mandatory=False, default=True),
                  "ctrl_photoshutter": Param("Control photo shutter?",
                                             type=bool, settable=True,
                                             mandatory=False, default=True),
                  "roi": Param("Region of interest",
                               type=tupleof(int, int, int, int),
                               default=(0, 0, 0, 0),
                               settable=True, volatile=True,
                               category="general"),
                  "pixelsize": Param("Pixel size in microns",
                                     type=oneof(125, 250, 500), default=500,
                                     settable=True, volatile=True,
                                     category="general"),
                  "file": Param("Image file location on maatel computer",
                                type=str, settable=True, volatile=True,
                                category="general"),
                  "readout_millis": Param("Timeout in ms for the readout.",
                                          type=int, settable=True,
                                          default=60000),
                  "exposure_time": Param("Default exposure time in seconds",
                                         type=float, settable=True, default=30.)
                  }

    @property
    def drum(self):
        return self._adevs["imgdrum"]

    @property
    def gammashutter(self):
        return self._adevs["gammashutter"]

    @property
    def photoshutter(self):
        return self._adevs["photoshutter"]

    def doInit(self, mode):
        self._t = None
        self.imagetype = ImageType(ImagePlateDetector.MAP_SHAPE[self.pixelsize],
                                   numpy.uint16)

    def _generateSequence(self, expoTime, prepare=False, *args, **kwargs):
        seq = []
        if prepare:
            # close shutter
            if self.ctrl_photoshutter:
                seq.append(SeqDev(self.photoshutter, ShutterStates.CLOSED))
            if self.ctrl_gammashutter:
                seq.append(SeqDev(self.gammashutter, ShutterStates.CLOSED))
            # erase and expo position
            if self.erase:
                seq.append(SeqDev(self.drum, ImagePlateDrum.POS_ERASE))
            seq.append(SeqDev(self.drum, ImagePlateDrum.POS_EXPO))
        if expoTime > 0:
            # open shutter
            if self.ctrl_gammashutter:
                seq.append(SeqDev(self.gammashutter, ShutterStates.OPEN))
            if self.ctrl_photoshutter:
                seq.append(SeqDev(self.photoshutter, ShutterStates.OPEN))
            # count
            seq.append(SeqSleep(expoTime, "counting for %fs" % expoTime))
            # close shutter
            if self.ctrl_photoshutter:
                seq.append(SeqDev(self.photoshutter, ShutterStates.CLOSED))
            if self.ctrl_gammashutter:
                seq.append(SeqDev(self.gammashutter, ShutterStates.CLOSED))
            # start readout
            seq.append(SeqDev(self.drum, ImagePlateDrum.POS_READ))
        return seq

    def _runFailed(self, step, action, exception):
        self.log.debug("RUNFAILED: %s" % action)
        self.log.debug("     args: %s" % action.args)
        self.log.debug("   device: %s" % action.dev)
        if action.dev == self.drum:
            self.log.warning("""%s failed.
Exception was:
%s

Retrying.""" % (action, exception))
            return 3
        else:
            raise exception

    def doSetPreset(self, **preset):
        if 't' in preset:
            self._t = preset['t']

    def doPrepare(self):
        self._startSequence(self._generateSequence(expoTime=False,
                                                   prepare=True))
        # temporary fix because the status is not updated instantly
        time.sleep(.3)

    def doStart(self):
        expoTime = self._t if self._t is not None else self.exposure_time
        self._t = None
        self._startSequence(self._generateSequence(expoTime))

    def doRead(self, maxage=0):
        return self.lastfilename

    def readFinalImage(self):
        narray = None
        timeout = self._dev.get_timeout_millis()
        self._dev.set_timeout_millis(self.readout_millis)
        try:
            narray = self._dev.Bitmap16Bit
        except CommunicationFailed: # PyTango
            raise CommunicationError(self, "Readout command timed out")
        finally:
            self._dev.set_timeout_millis(timeout)
        return narray

    def doReadRoi(self):
        return (0, self._dev.InterestZoneY, 1250, self._dev.InterestZoneH)

    def doReadPixelsize(self):
        return self._dev.PixelSize

    def doReadFile(self):
        return self._dev.ImageFile

    def doWriteRoi(self, value):
        self.log.warning("setting x offset and width are not supported " +
                         "- ignored.")
        self._dev.InterestZoneY = value[1]
        self._dev.InterestZoneH = value[3]

    def doWritePixelsize(self, value):
        self._dev.PixelSize = value
        self.imagetype = ImageType(ImagePlateDetector.MAP_SHAPE[value],
                                   numpy.uint16)

    def doWriteFile(self, value):
        self._dev.ImageFile = value
