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

"""NICOS commands tests."""

import os
import __builtin__

from nicos import session
from nicos.core import UsageError, LimitError
from nicos.utils import ensureDirectory

from nicos.commands.measure import count
from nicos.commands.device import move, maw, drive, switch, wait, read, \
     status, stop, reset, get, getall, setall, fix, release, adjust, \
     version, history, info, limits, resetlimits, ListParams, ListMethods, \
     ListDevices
from nicos.commands.device import set #pylint: disable=W0622
from nicos.commands.basic import help, dir  #pylint: disable=W0622
from nicos.commands.basic import ListCommands, sleep, \
     NewSetup, AddSetup, RemoveSetup, ListSetups, \
     CreateDevice, DestroyDevice, CreateAllDevices, \
     NewExperiment, FinishExperiment, AddUser, NewSample, \
     Remark, SetMode, ClearCache, UserInfo, run, edit
from nicos.commands.output import printdebug, printinfo, printwarning, \
     printerror, printexception

from test.utils import ErrorLogged, raises, requires

def setup_module():
    session.loadSetup('axis')
    session.setMode('master')

def teardown_module():
    session.unloadSetup()


def test_output_commands():
    printdebug('a', 'b')
    printinfo('testing...')
    try:
        1/0
    except ZeroDivisionError:
        assert session.testhandler.warns(printwarning, 'warn!', exc=1)
    assert raises(ErrorLogged, printerror, 'error!')
    assert raises(ZeroDivisionError, printexception, 'exception!')

def test_basic_commands():
    dev = session.getDevice('motor')

    help(help)
    ListCommands()

    d = dir(dev)
    assert 'start' in d
    assert 'doStart' not in d
    assert '_get_from_cache' not in d
    d = dir()
    assert 'd' in d

    sleep(0.1)

    ListSetups()
    NewSetup('axis')
    AddSetup()  # should list all setups but not fail
    AddSetup('slit')
    assert 'slit' in session.configured_devices  # not autocreated
    RemoveSetup('slit')
    assert 'slit' not in session.configured_devices
    assert session.testhandler.warns(RemoveSetup, 'blah')

    assert 'motor' not in session.devices
    CreateDevice('motor')
    assert 'motor' in session.devices
    DestroyDevice('motor')
    assert raises(UsageError, DestroyDevice)
    assert 'motor' not in session.devices
    CreateAllDevices()
    assert 'motor' in session.devices
    assert 'motor' in session.explicit_devices
    assert 'coder' in session.devices
    assert 'coder' not in session.explicit_devices

    exp = session.getDevice('Exp')

    NewExperiment(1234, 'Test experiment', 'L. Contact', '1. User')
    assert exp.proposal == 'p1234'
    assert exp.title == 'Test experiment'
    AddUser('F. X. User', 'user@example.com')
    assert 'F. X. User <user@example.com>' in exp.users
    NewSample('MnSi', lattice=[4.58]*3, angles=[90]*3)
    FinishExperiment()

    Remark('hi')
    assert exp.remark == 'hi'

    SetMode('slave')
    SetMode('master')
    assert raises(UsageError, SetMode, 'blah')

    motor = session.getDevice('motor')
    ClearCache('motor', motor)

    with UserInfo('userinfo'):
        assert 'userinfo' == session._actionStack[-1]

@requires(os.name == 'posix')
def test_edit_command():
    ensureDirectory(session.experiment.scriptpath)
    old_editor = os.environ.get('EDITOR')
    old_raw_input = __builtin__.raw_input
    os.environ['EDITOR'] = 'touch'
    __builtin__.raw_input = lambda prompt: ''
    try:
        edit('test.py')
    finally:
        if old_editor:
            os.environ['EDITOR'] = old_editor
        __builtin__.raw_input = old_raw_input
    testpath = os.path.join(session.experiment.scriptpath, 'test.py')
    assert os.path.isfile(testpath)
    os.unlink(testpath)

def test_run_command():
    # create a test script in the current scriptpath
    ensureDirectory(session.experiment.scriptpath)
    with open(os.path.join(session.experiment.scriptpath, 'test.py'), 'w') as f:
        f.write('read()')
    run('test')

def test_device_commands():
    motor = session.getDevice('motor')
    coder = session.getDevice('coder')

    # check move()
    positions = (min(motor.abslimits), 0, max(motor.abslimits))
    for pos in positions:
        move(motor, pos)
        motor.wait()
        assert motor.curvalue == pos

    assert raises(LimitError, move, motor, max(motor.abslimits)+1)

    assert raises(UsageError, move)
    assert raises(UsageError, move, motor, 1, motor)

    # check maw()
    for pos in positions:
        maw(motor, pos)
        assert motor.curvalue == pos

    # check drive() and switch() aliases
    drive(motor, 0)
    assert motor.curvalue == 0
    switch(motor, 1)
    assert motor.curvalue == 1

    # check wait()
    move(motor, 10)
    wait(motor, 0.1)
    wait()

    # check read()
    read()

    # check status()
    status()

    # check stop()
    stop()
    stop(motor)

    # check reset()
    reset(motor)

    # check set() and get()
    set(motor, 'speed', 10)
    assert motor.speed == 10
    get(motor, 'speed')

    # check info()
    info()

    # check getall() and setall()
    getall('speed')
    setall('speed', 0)
    assert motor.speed == 0

    # check fix() and release()
    move(motor, 0)
    fix(motor)
    move(motor, 10)
    release(motor)
    assert motor.curvalue == 0

    # check adjust()
    move(motor, 1)
    adjust(motor, 0)
    assert motor() == 0
    assert motor.offset == 1
    adjust(motor, 0, 1)
    assert motor() == 1
    assert motor.offset == 0

    # check version()
    version(motor)

    # check history()
    history(motor)
    history(motor, 'value')
    history(motor, -24)
    history(motor, 24)
    history(motor, 'value', -24)
    for timespec in ['1 week', '30 minutes', '2012-01-01',
                     '2012-01-01 14:00', '14:00']:
        history(motor, 'value', timespec)

    # check limits()
    limits(motor, coder)
    limits()

    # check resetlimits()
    motor.userlimits = (1, 1)
    resetlimits(motor, coder)
    assert motor.userlimits == motor.abslimits

    # check ListParams(), ListMethods(), ListDevices()
    ListParams(motor)
    ListMethods(motor)
    ListDevices()

    # check count()
    assert raises(UsageError, count, motor)
    count()
