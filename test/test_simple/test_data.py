#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2019 by the NICOS contributors (see AUTHORS)
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
#   Georg Brandl <g.brandl@fz-juelich.de>
#
# *****************************************************************************

"""NICOS data manager test suite."""

from __future__ import absolute_import, division, print_function

from contextlib import contextmanager

from nicos.commands.measure import count

session_setup = 'data'


def test_cleanup(session):
    # check that data manager cleans up unsuitable datasets still open
    session.data.beginPoint()
    session.data.beginPoint()
    assert len(session.data._stack) == 1
    session.data.finishPoint()


@contextmanager
def dataset_scope(session, settype, **kwds):
    getattr(session.data, 'begin' + settype.capitalize())(**kwds)
    yield session.data._current
    getattr(session.data, 'finish' + settype.capitalize())()


def test_dataset_stack(session, log):
    session.experiment.new(0, user='user')
    # create some datasets on the stack, check nesting
    with dataset_scope(session, 'block') as blockset:
        with log.assert_warns('no scan to finish'):
            session.data.finishScan()
        with log.assert_warns('no data point to finish'):
            session.data.finishPoint()

        with dataset_scope(session, 'scan') as scanset:
            with log.assert_warns('no block to finish'):
                session.data.finishBlock()
            assert session.data._current.number == 1

            with dataset_scope(session, 'point') as pointset:
                assert list(session.data.iterParents(pointset)) == \
                    [scanset, blockset]

                with dataset_scope(session, 'scan', subscan=True):
                    with dataset_scope(session, 'point'):
                        assert len(session.data._stack) == 5
                        assert [s.settype for s in session.data._stack] == \
                            ['block', 'scan', 'point', 'subscan', 'point']

                        assert session.data._current.number == 1

                    with dataset_scope(session, 'point'):
                        assert session.data._current.number == 2


def test_empty_manager(session):
    # check for empty data stack
    assert session.data._stack == []
    assert session.data._current is None
    # check for empty scan cache
    session.data.reset_all()
    assert session.data._last_scans == []


def test_temp_point(session):
    session.data.beginTemporaryPoint()
    assert session.data._current.handlers == []
    session.data.finishPoint()


def test_point_dataset(session):
    assert len(session.data._stack) == 0  # pylint: disable=len-as-condition
    with dataset_scope(session, 'point'):
        ds = session.data._current

        # only assigned if a parent dataset is open
        assert ds.number == 0

        # fresh dataset, nothing in there
        assert not ds.results
        assert not ds.values
        assert not ds._valuestats
        assert not ds.metainfo

        # now fill it with some device values
        for (ts, value) in [(0, 5.), (2, 7.), (3, 5.), (4, 4.)]:
            session.data.putValues({'dev': (ts, value)})
        session.data.putValues({'dev2': (2, 5.)})

        # check value stats for devices with multiple values
        mean, stdev, mini, maxi = ds.valuestats['dev']
        assert mini == 4.
        assert maxi == 7.
        assert mean == 5.5
        assert 0.866 < stdev < 0.867  # sqrt(3)/2

        # check value stats for devices with only one value
        mean, stdev, mini, maxi = ds.valuestats['dev2']
        assert mini == maxi == mean == 5.
        assert stdev == float('inf')


def test_force_scandata(session):
    session.experiment._setROParam('forcescandata', True)
    try:
        count(1)
        # ensure that a scan dataset was produced
        ds = session.data._last_scans[-1]
        assert ds.npoints == 1
        assert session.experiment.lastscan == ds.counter
    finally:
        session.experiment._setROParam('forcescandata', False)
