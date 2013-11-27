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

"""Scan classes for NICOS."""

from time import sleep, time as currenttime

from nicos import session
from nicos.core import status, Readable, Value, NicosError, LimitError, \
     ModeError, InvalidValueError, PositionError, CommunicationError, \
     TimeoutError, ComputationError, MoveError, INFO_CATEGORIES
from nicos.utils import Repeater
from nicos.commands.output import printwarning
from nicos.commands.measure import _count
from nicos.core import SIMULATION, SLAVE
from nicos.devices.abstract import ImageStorage


class SkipPoint(Exception):
    """Custom exception class to skip a scan point."""

class StopScan(Exception):
    """Custom exception class to stop the rest of the scan."""


class Scan(object):
    """
    Represents a general scan over some devices with a specified detector.
    """

    shortdesc = None

    def __init__(self, devices, positions, firstmoves=None, multistep=None,
                 detlist=None, envlist=None, preset=None, scaninfo=None,
                 scantype=None):
        if session.mode == SLAVE:
            raise ModeError('cannot scan in slave mode')
        self.dataset = session.experiment.createDataset(scantype)
        if not detlist:
            detlist = session.experiment.detectors
        if not detlist:
            printwarning('scanning without detector, use SetDetectors() '
                         'to select which detector(s) you want to use')
        elif preset:
            names = set(preset)
            for det in detlist:
                names.difference_update(det.presetInfo())
            if names:
                printwarning('these preset keys were not recognized by any of '
                             'the detectors: %s -- detectors are %s' %
                             (', '.join(names), ', '.join(map(str, detlist))))
        if envlist == []:
            # special value [] to suppress all envlist devices
            allenvlist = []
        else:
            allenvlist = session.experiment.sampleenv
            if envlist is not None:
                allenvlist.extend(dev for dev in envlist if dev not in allenvlist)
        session.experiment.advanceScanCounter()
        self._firstmoves = firstmoves
        self._multistep = self.dataset.multistep = multistep
        if self._multistep:
            self._mscount = len(multistep[0][1])
            self._mswhere = [[(mse[0], mse[1][i]) for mse in multistep]
                             for i in range(self._mscount)]
        self._devices = self.dataset.devices = devices
        self._positions = self.dataset.positions = positions
        self._detlist = self.dataset.detlist = detlist
        self._envlist = self.dataset.envlist = allenvlist
        self._preset = self.dataset.preset = preset
        self.dataset.scaninfo = scaninfo
        self._sinks = self.dataset.sinks
        self.dataset.sinkinfo = {}
        try:
            self._npoints = len(positions)  # can be zero if not known
        except TypeError:
            self._npoints = 0

    def prepareScan(self, positions):
        session.beginActionScope('%s (moving to start)' % self.shortDesc())
        try:
            # the move-before devices
            if self._firstmoves:
                self.moveDevices(self._firstmoves)
            # the scanned-over devices
            self.moveTo(positions)
        finally:
            session.endActionScope()

    def beginScan(self):
        dataset = self.dataset
        session.experiment._last_datasets.append(dataset)
        dataset.xresults = []
        dataset.yresults = []
        devinfo = sum((dev.valueInfo() for dev in self._devices), ())
        envinfo = sum((dev.valueInfo() for dev in self._envlist), ())
        dataset.xvalueinfo = devinfo + envinfo
        dataset.envvalues = len(envinfo)
        dataset.yvalueinfo = sum((det.valueInfo()
                                  for det in dataset.detlist), ())
        if self._multistep:
            dataset.yvalueinfo = dataset.yvalueinfo * self._mscount
        for sink in self._sinks:
            sink.prepareDataset(dataset)
        for sink in self._sinks:
            sink.beginDataset(dataset)
        bycategory = {}
        for _, device in sorted(session.devices.iteritems()):
            if device.lowlevel:
                continue
            for category, key, value in device.info():
                bycategory.setdefault(category, []).append((device, key, value))
        for catname, catinfo in INFO_CATEGORIES:
            if catname not in bycategory:
                continue
            for sink in self._sinks:
                sink.addInfo(dataset, catinfo, bycategory[catname])
            for imageinfo in dataset.imageinfos:
                imageinfo.header[catinfo] = bycategory[catname]
        session.elog_event('scanbegin', dataset)
        session.beginActionScope(self.shortDesc())

    def preparePoint(self, num, xvalues):
        if self._npoints == 0:
            session.beginActionScope('Point %d' % num)
        else:
            session.beginActionScope('Point %d/%d' % (num, self._npoints))
        # update dataset values
        self.dataset.curpoint = num
        self.dataset.updateHeaderInfo(dict(zip(self._devices, xvalues)))
        # propagate to the relevant objects
        for det in self._detlist:
            if isinstance(det, ImageStorage):
                for catinfo, bycategory in self.dataset.headerinfo.iteritems():
                    det.addHeader(catinfo, bycategory)
                det.addHeader('scan', [(self, 'pointnum', '%d' % num)])

    def addPoint(self, xvalues, yvalues):
        self.dataset.xresults.append(xvalues)
        self.dataset.yresults.append(yvalues)
        for sink in self._sinks:
            sink.addPoint(self.dataset, xvalues, yvalues)

    def finishPoint(self):
        session.endActionScope()
        session.breakpoint(2)

    def endScan(self):
        session.endActionScope()
        for sink in self._sinks:
            sink.endDataset(self.dataset)
        session.elog_event('scanend', self.dataset)
        session.breakpoint(1)

    def handleError(self, what, dev, val, err):
        """Handle an error occurring during positioning or readout for a point.

        This method can do several things:

        - re-raise the current exception to abort everything
        - raise `StopScan` to end the current scan with an error, but not
          raise an exception in the script
        - raise `SkipPoint` to skip current point and continue with next point
        - return: to ignore error and continue with current point
        """
        if isinstance(err, (PositionError, MoveError, TimeoutError)):
            # continue counting anyway
            if what == 'read':
                printwarning('Readout problem', exc=1)
            else:
                printwarning('Positioning problem, continuing', exc=1)
            return
        elif isinstance(err, (InvalidValueError, LimitError,
                              CommunicationError, ComputationError)):
            if what == 'read':
                printwarning('Readout problem', exc=1)
            else:
                printwarning('Skipping data point', exc=1)
                raise SkipPoint
        # would also be possible:
        # elif ...:
        #     raise StopScan
        else:
            # consider all other errors to be fatal
            raise

    def moveTo(self, position):
        """Move scan devices to *position*, a list of positions."""
        return self.moveDevices(zip(self._devices, position))

    def moveDevices(self, where, wait=True):
        """Move to *where*, which is a list of (dev, position) tuples.
        On errors, call handleError, which decides when the scan may continue.
        """
        waitdevs = []
        for dev, val in where:
            try:
                dev.start(val)
            except NicosError, err:
                # handleError can reraise for fatal error, return False
                # to skip this point and True to measure anyway
                self.handleError('move', dev, val, err)
            else:
                waitdevs.append((dev, val))
        if not wait:
            return
        for dev, val in waitdevs:
            try:
                dev.wait()
            except NicosError, err:
                self.handleError('wait', dev, val, err)

    def readPosition(self):
        # using read() assumes all devices have updated cached value on wait()
        ret = []
        for dev in self._devices:
            try:
                val = dev.read()
            except NicosError, err:
                self.handleError('read', dev, None, err)
                val = [None] * len(dev.valueInfo())
            if isinstance(val, list):
                ret.extend(val)
            else:
                ret.append(val)
        return ret

    def readEnvironment(self, start, finished):
        ret = []
        for dev in self._envlist:
            try:
                if isinstance(dev, DevStatistics):
                    val = dev.read(start, finished)
                else:
                    val = dev.read(0)
            except NicosError, err:
                self.handleError('read', dev, None, err)
                val = [None] * len(dev.valueInfo())
            if isinstance(val, list):
                ret.extend(val)
            else:
                ret.append(val)
        return ret

    def shortDesc(self):
        if 'number' in self.dataset.sinkinfo:
            return 'Scan %s #%s' % (','.join(map(str, self._devices)),
                                    self.dataset.sinkinfo['number'])
        return 'Scan %s' % ','.join(map(str, self._devices))

    def run(self):
        if getattr(session, '_currentscan', None):
            raise NicosError('cannot start scan while another scan is running')
        session._currentscan = self
        try:
            self._inner_run()
        finally:
            session._currentscan = None

    def _inner_run(self):
        # move all devices to starting position before starting scan
        try:
            self.prepareScan(self._positions[0])
        except StopScan:
            return
        except SkipPoint:
            can_measure = False
        else:
            can_measure = True
        self.beginScan()
        try:
            for i, position in enumerate(self._positions):
                self.preparePoint(i+1, position)
                try:
                    if position:
                        if i != 0:
                            self.moveTo(position)
                        elif not can_measure:
                            continue
                    started = currenttime()
                    actualpos = self.readPosition()
                    try:
                        result = []
                        if self._multistep:
                            for i in range(self._mscount):
                                self.moveDevices(self._mswhere[i])
                                _count(self._detlist, self._preset, result,  dataset=self.dataset)
                        else:
                            _count(self._detlist, self._preset, result,  dataset=self.dataset)
                    finally:
                        actualpos += self.readEnvironment(started, currenttime())
                        self.addPoint(actualpos, result)
                except SkipPoint:
                    pass
                finally:
                    self.finishPoint()
        except StopScan:
            pass
        finally:
            self.endScan()


class ElapsedTime(Readable):
    temporary = True
    def doRead(self, maxage=0):
        return 0
    def doStatus(self, maxage=0):
        return status.OK, ''


class SweepScan(Scan):
    """
    Special scan class for "sweeps" (i.e., start device(s) and scan until they
    arrive at their targets.)  The number of points, if > 0, is a maximum of
    points, after which the scan will stop.

    If no devices are given, acts as a "time scan", i.e. just counts the given
    number of points (or indefinitely) with an elapsed time counter.
    """

    def __init__(self, devices, startend, numpoints, firstmoves=None,
                 multistep=None, detlist=None, envlist=None, preset=None,
                 scaninfo=None, scantype=None):
        self._etime = ElapsedTime('etime', unit='s', fmtstr='%.1f')
        self._started = currenttime()
        self._numpoints = numpoints
        self._sweepdevices = devices
        if numpoints < 0:
            points = Repeater([])
        else:
            points = [[]] * numpoints
        # start for sweep devices are "firstmoves"
        firstmoves = []
        self._sweeptargets = []
        for dev, (start, end) in zip(devices, startend):
            if start is not None:
                firstmoves.append((dev, start))
            self._sweeptargets.append((dev, end))
        # sweep scans support a special "delay" preset
        self._delay = preset.pop('delay', 0)
        Scan.__init__(self, [], points, firstmoves, multistep,
                      detlist, envlist, preset, scaninfo, scantype)
        if not devices:
            self._envlist.insert(0, self._etime)
        else:
            for dev in devices[::-1]:
                if dev in self._envlist:
                    self._envlist.remove(dev)
                self._envlist.insert(0, dev)

    def shortDesc(self):
        if not self._sweepdevices:
            stype = 'Time scan'
        else:
            stype = 'Sweep %s' % ','.join(map(str, self._sweepdevices))
        if 'number' in self.dataset.sinkinfo:
            return '%s #%s' % (stype, self.dataset.sinkinfo['number'])
        return stype

    def readEnvironment(self, started, finished):
        ret = Scan.readEnvironment(self, started, finished)
        if not self._sweepdevices:
            ret[0] = finished - self._started
        return ret

    def endScan(self):
        self._etime.shutdown()
        Scan.endScan(self)

    def preparePoint(self, num, xvalues):
        if num == 1:
            try:
                self.moveDevices(self._sweeptargets, wait=False)
            except SkipPoint:
                raise StopScan
        elif self._delay:
            # wait between points, but only from the second point on
            session.action('Delay')
            sleep(self._delay)
        Scan.preparePoint(self, num, xvalues)
        if session.mode == SIMULATION:
            self._sim_start = session.clock.time

    def finishPoint(self):
        Scan.finishPoint(self)
        if self._sweepdevices:
            if not any(dev.status()[0] == status.BUSY
                       for dev in self._sweepdevices):
                raise StopScan
        if session.mode == SIMULATION:
            if self._numpoints > 1:
                session.log.info('skipping %d points...' % (self._numpoints - 1))
                duration = session.clock.time - self._sim_start
                session.clock.tick(duration * (self._numpoints - 1))
            elif self._numpoints < 0:
                session.log.info('would scan indefinitely, skipping...')
            raise StopScan


class ManualScan(Scan):
    """
    Special scan class for "manual" scans.
    """

    def __init__(self, firstmoves=None, multistep=None, detlist=None,
                 envlist=None, preset=None, scaninfo=None, scantype=None):
        Scan.__init__(self, [], Repeater([]), firstmoves, multistep,
                      detlist, envlist, preset, scaninfo, scantype)
        self._curpoint = 0

    def manualBegin(self):
        session.beginActionScope('Scan')
        self.beginScan()

    def manualEnd(self):
        session.endActionScope()
        self.endScan()

    def step(self, **preset):
        preset = preset or self._preset
        self._curpoint += 1
        self.preparePoint(self._curpoint, [])
        result = actualpos = []
        started = currenttime()
        try:
            actualpos = self.readPosition()
            try:
                if self._multistep:
                    for i in range(self._mscount):
                        self.moveDevices(self._mswhere[i])
                        _count(self._detlist, preset, result,  dataset=self.dataset)
                else:
                    _count(self._detlist, preset, result,  dataset=self.dataset)
            finally:
                actualpos += self.readEnvironment(started, currenttime())
                self.addPoint(actualpos, result)
        except SkipPoint:
            pass
        finally:
            self.finishPoint()
        return result


class QScan(Scan):
    """
    Special scan class for scans with a triple axis instrument in Q/E space.
    """

    def __init__(self, positions, firstmoves=None, multistep=None,
                 detlist=None, envlist=None, preset=None, scaninfo=None,
                 scantype=None):
        from nicos.devices.tas import TAS
        inst = session.instrument
        if not isinstance(inst, TAS):
            raise NicosError('cannot do a Q scan, your instrument device '
                             'is not a triple axis device')
        Scan.__init__(self, [inst], positions,
                      firstmoves, multistep, detlist, envlist, preset,
                      scaninfo, scantype)
        self._envlist[0:0] = [inst._adevs['mono'], inst._adevs['ana'],
                              inst._adevs['psi'], inst._adevs['phi']]
        if inst in self._envlist:
            self._envlist.remove(inst)

    def shortDesc(self):
        comps = []
        if len(self._positions) > 1:
            for i in range(4):
                if self._positions[0][0][i] != self._positions[1][0][i]:
                    comps.append('HKLE'[i])
        if 'number' in self.dataset.sinkinfo:
            return 'Scan %s #%s' % (','.join(comps) or 'Q',
                                    self.dataset.sinkinfo['number'])
        return 'Scan %s' % (','.join(comps) or 'Q')

    def beginScan(self):
        if len(self._positions) > 1:
            # determine first varying index as the plotting index
            for i in range(4):
                if self._positions[0][0][i] != self._positions[1][0][i]:
                    self.dataset.xindex = i
                    self.dataset.xrange = (self._positions[0][0][i],
                                           self._positions[-1][0][i])
                    break
        Scan.beginScan(self)


class ContinuousScan(Scan):
    """
    Special scan class for scans with one axis moving continuously (used for
    peak search).
    """

    DELTA = 1.0

    def __init__(self, device, start, end, speed, firstmoves=None, detlist=None,
                 envlist=None, scaninfo=None):
        self._startpos = start
        self._endpos = end
        if speed is None:
            self._speed = device.speed / 5.
        else:
            self._speed = speed

        Scan.__init__(self, [device], [], firstmoves, None, detlist, envlist,
                      None, scaninfo)

    def shortDesc(self):
        if 'number' in self.dataset.sinkinfo:
            return 'Continuous scan %s #%s' % (self._devices[0],
                                               self.dataset.sinkinfo['number'])
        return 'Continuous scan %s' % self._devices[0]

    def run(self):
        device = self._devices[0]
        detlist = self._detlist
        ok, why = device.isAllowed(self._startpos)
        if not ok:
            raise LimitError('Cannot move to start value for %s: %s' %
                             (device, why))
        ok, why = device.isAllowed(self._endpos)
        if not ok:
            raise LimitError('Cannot move to end value for %s: %s' %
                             (device, why))
        try:
            self.prepareScan([self._startpos])
        except (StopScan, SkipPoint):
            return
        self.beginScan()
        original_speed = device.speed
        session.beginActionScope(self.shortDesc())
        try:
            device.speed = self._speed
            device.move(self._endpos)
            starttime = currenttime()
            preset = max(abs(self._endpos - self._startpos) /
                         (self._speed or 0.1) * 5, 3600)
            session.experiment.advanceImageCounter(detlist)
            for det in detlist:
                det.start(t=preset)
            last = sum((det.read() for det in detlist), [])
            while device.status(0)[0] == status.BUSY:
                sleep(self.DELTA)
                session.breakpoint(2)
                devpos = device.read(0)
                read = sum((det.read() for det in detlist), [])
                actualpos = [devpos] + self.readEnvironment(starttime,
                                                            currenttime())
                starttime = currenttime()
                diff = [read[i] - last[i]
                        if isinstance(read[i], (int, long, float)) else read[i]
                        for i in range(len(read))]
                self.dataset.curpoint += 1
                self.addPoint(actualpos, diff)
                last = read
                for det in detlist:
                    if isinstance(det, ImageStorage):
                        det.updateImage()
        finally:
            for det in detlist:
                try:
                    det.stop()
                except Exception:
                    session.log.warning('could not stop %s' % det, exc=1)
                if isinstance(det, ImageStorage):
                    det.saveImage()
            session.endActionScope()
            device.stop()
            device.speed = original_speed
            self.endScan()


class TwoDimScan(Scan):
    """
    Special scan class for two-dimensional scans.
    """

    def __init__(self, dev1, start1, step1, numpoints1,
                 dev2, start2, step2, numpoints2,
                 firstmoves=None, multistep=None, detlist=None,
                 envlist=None, preset=None, scaninfo=None):
        scantype = '2D'
        devices = [dev1, dev2]
        positions = []
        for i in range(numpoints1):
            dev1value = start1 + i*step1
            # move dev2 forward in one row, then move it back in the next row
            if i % 2 == 0:
                positions.extend([dev1value, start2 + j*step2]
                                 for j in range(numpoints2))
            else:
                positions.extend([dev1value, start2 + (numpoints2-j-1)*step2]
                                 for j in range(numpoints2))
        self._pointsperrow = numpoints2
        Scan.__init__(self, devices, positions, firstmoves, multistep,
                      detlist, envlist, preset, scaninfo, scantype)

    def preparePoint(self, num, xvalues):
        if num > 1 and (num-1) % self._pointsperrow == 0:
            for sink in self._sinks:
                sink.addBreak(self.dataset)
        Scan.preparePoint(self, num, xvalues)


class DevStatistics(object):
    """Object to use in the environment list to get not only a single device
    value, but statistics such as average, minimum or maximum over the time of
    counting during a scan point.
    """

    statname = None

    def __init__(self, dev):
        self.dev = dev

    def __str__(self):
        return '%s:%s' % (self.dev, self.statname)

    def read(self, fromtime, totime):
        raise NotImplementedError('%s.read() must be implemented'
                                  % self.__class__.__name__)

    def valueInfo(self):
        raise NotImplementedError('%s.valueInfo() must be implemented'
                                  % self.__class__.__name__)


class Average(DevStatistics):
    """Collects the average of the device value."""

    statname = 'avg'

    def read(self, fromtime, totime):
        hist = self.dev.history(fromtime=fromtime, totime=totime)
        if len(hist) < 2:
            # if there is no history, read at least once
            return self.dev.read(0)
        avg = sum(v for (t, v) in hist[1:]) / (len(hist) - 1)
        return avg

    def valueInfo(self):
        return Value('%s:avg' % self.dev, unit=self.dev.unit,
                     fmtstr=self.dev.fmtstr),


class MinMax(DevStatistics):
    """Collects the minimum and maximum of the device value."""

    statname = 'minmax'

    def read(self, fromtime, totime):
        hist = self.dev.history(fromtime=fromtime, totime=totime)
        if len(hist) < 2:
            # if there is no history, read at least once
            v = self.dev.read(1.0)
            return [v, v]
        real = hist[1:]
        mini = min(v for (t, v) in real)
        maxi = max(v for (t, v) in real)
        return [mini, maxi]

    def valueInfo(self):
        return (Value('%s:min' % self.dev, unit=self.dev.unit,
                      fmtstr=self.dev.fmtstr),
                Value('%s:max' % self.dev, unit=self.dev.unit,
                      fmtstr=self.dev.fmtstr))


DevStatistics.subclasses = {
    Average.statname: Average,
    MinMax.statname:  MinMax,
}
