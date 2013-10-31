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

"""NICOS device class test suite."""

import os
import time
from os import path

from nicos import session
from nicos.utils import ensureDirectory, enableDirectory
from nicos.commands.scan import scan
from nicos.commands.basic import run

from test.utils import rootdir

year = time.strftime('%Y')


def setup_module():
    session.loadSetup('asciisink')  # we want data files written
    session.setMode('master')

def teardown_module():
    # clean up "disabled" directory so that the next test run can remove it
    if path.isdir(datapath('p999')):
        enableDirectory(datapath('p999'))
    session.experiment._setROParam('managerights', None)
    session.unloadSetup()


def datapath(*parts):
    return path.join(rootdir, 'data', year, *parts)


def test_experiment():
    exp = session.experiment

    # create the needed script file
    spath = path.join(rootdir, 'data', year,
                      'service', 'scripts')
    ensureDirectory(spath)
    with open(path.join(spath, 'servicestart.py'), 'w') as fp:
        fp.write('Remark("service time")\n')

    # first, go in service mode
    exp.servicescript = 'servicestart.py'
    try:
        exp.new('service')
    finally:
        exp.servicescript = ''
    assert exp.proposal == 'service'
    assert exp.proptype == 'service'
    assert exp.remark == 'service time'

    # for this proposal, remove access rights after switching back
    exp._setROParam('managerights', dict( disableFileMode=0, disableDirMode=0))

    # then, go in proposal mode
    exp.new(999, 'etitle', 'me', 'you')
    # check that all properties have been set accordingly
    assert exp.proposal == 'p999'
    assert exp.proptype == 'user'
    assert exp.title == 'etitle'
    assert exp.localcontact == 'me'
    assert exp.users == 'you'
    assert exp.remark == ''

    # check that directories have been created
    assert path.isdir(datapath('p999'))
    assert path.isdir(datapath('p999', 'scripts'))
    assert path.isdir(datapath('p999', 'data'))

    # check that templating works
    assert path.isfile(datapath('p999', 'scripts', 'start_p999.py'))
    run('start_p999.py')
    assert exp.remark == 'proposal p999 started by you; sample is unknown'

    # try a small scan; check for data file written
    scan(session.getDevice('axis'), 0, 1, 5, 0.01)
    assert path.isfile(datapath('p999', 'data', 'filecounter'))
    assert path.isfile(datapath('p999', 'data', 'p999_00000001.dat'))

    # now, finish the experiment
    exp.finish()
    # has the zip file been created?
    assert path.isfile(datapath('p999.zip'))
    # have the access rights been revoked?
    if os.name != 'nt':
        assert not os.access(datapath('p999'), os.X_OK)

    # did we switch back to service proposal?
    assert exp.proposal == 'service'

    # switch back to proposal (should re-enable directory)
    exp.new('p999')
    assert os.access(datapath('p999'), os.X_OK)
    assert exp.users == ''

    exp.addUser('A User')
    #~ exp.users
    assert exp.users == 'A User'
    exp.addUser('Another User', 'another.user@experiment.com')
    assert exp.users == 'A User, Another User <another.user@experiment.com>'
    exp.addUser('Athird User', 'athird.user@experiment.com',
                'An Institute, Anywhere street, 12345 Anywhere')
    assert exp.users == 'A User, Another User <another.user@experiment.com>, '\
                        'Athird User <athird.user@experiment.com> ' \
                        '(An Institute, Anywhere street, 12345 Anywhere)'

    # and back to service
    exp.new('service')
