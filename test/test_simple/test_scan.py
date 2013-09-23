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

"""NICOS tests for nicos.commands.scan and nicos.core.scan modules."""

from nicos import session
from nicos.core import UsageError, PositionError, CommunicationError, \
     NicosError, ModeError
from nicos.core.scan import ContinuousScan

from nicos.commands.measure import count, avg, minmax
from nicos.commands.scan import scan, cscan, timescan, twodscan, contscan, \
     manualscan, sweep, appendscan
from nicos.commands.analyze import checkoffset
from nicos.commands.tas import checkalign

from test.utils import raises


def setup_module():
    session.loadSetup('scanning')
    session.setMode('master')

def teardown_module():
    session.unloadSetup()


def test_scan():
    m = session.getDevice('motor')
    m2 = session.getDevice('motor2')
    c = session.getDevice('coder')
    ctr = session.getDevice('ctr1')
    mm = session.getDevice('manual')
    mm.move(0)

    # check that scans are impossible in slave mode
    session.setMode('slave')
    assert raises(ModeError, scan, m, [0, 1, 2, 10])
    session.setMode('master')

    session.experiment.setDetectors([session.getDevice('det')])
    session.experiment.setEnvironment([avg(mm), minmax(mm)])

    try:
        # plain scan, with some extras: infostring, firstmove
        scan(m, 0, 1, 5, 0., 'test scan', manual=1)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xnames == ['motor', 'manual:avg', 'manual:min', 'manual:max']
        assert dataset.xunits == ['mm'] * 4
        assert dataset.xresults == [[float(i), 1, 1, 1] for i in range(5)]
        assert dataset.ynames == ['timer', 'mon1', 'ctr1', 'ctr2']
        assert dataset.yunits == ['s', 'cts', 'cts', 'cts']
        assert dataset.scaninfo.startswith('test scan')
        assert len(dataset.yresults) == 5
        assert mm.read() == 1

        session.experiment.setEnvironment([])

        # scan with second basic syntax
        scan(m, [0, 4, 5], 0.)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[float(i)] for i in [0, 4, 5]]

        # scan with multiple devices
        scan([m, m2], [0, 0], [1, 2], 3, t=0.)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[float(i), float(i*2)] for i in [0, 1, 2]]

        # scan with multiple devices and second basic syntax
        scan([m, m2], [[0, 0, 1], [4, 2, 1]], t=0.)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[0., 4.], [0., 2.], [1., 1.]]

        # scan with different detectors
        scan(m, [0, 1], ctr)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[0.], [1.]]
        assert len(dataset.yresults) == 2 and len(dataset.yresults[0]) == 1
        assert dataset.ynames == ['ctr1']

        # scan with different environment
        scan(m, [0, 1], c)
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[0., 0.], [1., 1.]]
        assert dataset.xnames == ['motor', 'coder']
        assert dataset.xunits == ['mm', 'mm']

        # scan with multistep
        scan(m, [0, 1], ctr, manual=[3, 4])
        dataset = session.experiment._last_datasets[-1]
        assert dataset.xresults == [[0.], [1.]]
        assert dataset.ynames == ['ctr1_manual_3', 'ctr1_manual_4']
    finally:
        session.experiment.envlist = []
        session.experiment.detlist = []

def test_scan_usageerrors():
    m = session.getDevice('motor')
    m2 = session.getDevice('motor2')
    # not enough arguments
    assert raises(UsageError, scan, m)
    assert raises(UsageError, scan, m, 0, 1)
    assert raises(UsageError, scan, [m, m2], [0, 1])
    assert raises(UsageError, scan, [m, m2], [0, 1], [0.1, 0.2])
    # start/step must be lists for multidevice
    assert raises(UsageError, scan, [m, m2], 0)
    assert raises(UsageError, scan, [m, m2], [0, 1], 0.1, 1)
    # start/step must be of equal length
    assert raises(UsageError, scan, [m, m2], [0, 1], [0.1, 0.2, 0.3], 1)
    # as must individual value lists
    assert raises(UsageError, scan, [m, m2], [[0, 1], [0.1, 0.2, 0.3]])
    # as must multistep lists
    assert raises(UsageError, scan, m, 0, 1, 1, motor=[1,2], motor2=[3,4,5])
    # unsupported scan argument
    assert raises(UsageError, scan, m, 0, 1, 1, {})

def test_scan_invalidpreset():
    m = session.getDevice('motor')
    # invalid preset
    assert session.testhandler.warns(scan, m, 0, 1, 1, preset=5)

def test_scan_errorhandling():
    t = session.getDevice('tdev')
    m = session.getDevice('motor')

    # no errors, works fine
    scan(t, [0, 1, 2])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0], [1], [2]]

    # limit error: skips the data points
    scan(t, [-10, 0, 10, 3])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0], [3]]

    # communication error during move: also skips the data points
    t._value = 0
    t._start_exception = CommunicationError()
    scan(t, [0, 1, 2, 3])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0]]  # tdev.move only raises when target != 0

    # communication error during readout: ignored
    t._start_exception = None
    t._read_exception = CommunicationError()
    scan(t, [0, 1, 2, 3])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[None], [None], [None], [None]]

    # position error during move: ignored
    t._value = 0
    t._read_exception = None
    t._start_exception = PositionError()
    scan(t, [0, 1, 2, 3])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0], [0], [0], [0]]

    # position error during readout: ignored
    t._read_exception = PositionError()
    t._start_exception = None
    scan(t, [0, 1, 2, 3])
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[None], [None], [None], [None]]
    # also as an environment device
    scan(m, [0, 1], t)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[0., None], [1., None]]

    # other errors: reraised
    t._start_exception = RuntimeError()
    assert raises(RuntimeError, scan, t, [0, 1, 2, 3])

def test_cscan():
    m = session.getDevice('motor')
    cscan(m, 0, 1, 2)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults == [[-2.], [-1.], [0.], [1.], [2.]]

def test_sweeps():
    m = session.getDevice('motor')
    m.move(1)
    timescan(5, m)
    dataset = session.experiment._last_datasets[-1]
    assert len(dataset.xresults) == 5
    assert dataset.xresults[0][0] < 1
    assert dataset.xresults[0][1] == 1.0

    sweep(m, 1, 5)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults[-1][0] == 5

def test_contscan():
    m = session.getDevice('motor')
    mm = session.getDevice('manual')
    m.move(0)
    ContinuousScan.DELTA = 0.1
    session.experiment.detlist = [session.getDevice('det')]
    try:
        contscan(m, 0, 2, 2)
    finally:
        ContinuousScan.DELTA = 1.0
        session.experiment.detlist = []
    dataset = session.experiment._last_datasets[-1]
    assert dataset.xresults
    assert all(0 <= res[0] <= 2 for res in dataset.xresults)
    # no speed parameter
    assert raises(UsageError, contscan, mm, 0, 2)
    # preset and multistep not allowed
    assert raises(UsageError, contscan, m, 0, 2, 2, t=1)
    assert raises(UsageError, contscan, m, 0, 2, 2, manual=[0, 1])

def test_manualscan():
    m = session.getDevice('motor')
    c = session.getDevice('coder')
    ctr = session.getDevice('ctr1')
    # normal
    with manualscan(m):
        for i in range(3):
            m.move(i)
            m.wait()
            count()
        assert raises(NicosError, manualscan)
    # with multistep
    with manualscan(m, c, ctr, 'manscan', manual=[0, 1]):
        for i in range(3):
            m.move(i)
            m.wait()
            count()
    dataset = session.experiment._last_datasets[-1]
    assert dataset.scaninfo.startswith('manscan')
    assert dataset.xresults == [[0., 0.], [1., 1.], [2., 2.]]
    assert dataset.ynames == ['ctr1_manual_0', 'ctr1_manual_1']

def test_specialscans():
    m = session.getDevice('motor')
    ctr = session.getDevice('ctr1')
    checkoffset(m, 10, 0.05, 2, ctr)

    tas = session.getDevice('Tas')
    tas.scanmode = 'CKI'
    tas.scanconstant = 1.55
    checkalign((1, 0, 0), 0.05, 2, ctr, accuracy=0.1)

    dataset = session.experiment._last_datasets[-1]
    uid = dataset.uid

    appendscan(5)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.sinkinfo['continuation'] == str(uid)
    uid2 = dataset.uid
    appendscan(-5)
    dataset = session.experiment._last_datasets[-1]
    assert dataset.sinkinfo['continuation'] == '%s,%s' % (uid2, uid)

def test_twodscan():
    m = session.getDevice('motor')
    m2 = session.getDevice('motor2')
    twodscan(m, 0, 1, 3, m2, 0, 1, 3, '2d')
    dataset = session.experiment._last_datasets[-1]
    assert dataset.scaninfo.startswith('2d')
    assert dataset.xresults == [[0., 0.], [0., 1.], [0., 2.],
                                [1., 2.], [1., 1.], [1., 0.],
                                [2., 0.], [2., 1.], [2., 2.]]
