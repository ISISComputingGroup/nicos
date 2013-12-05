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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#
# *****************************************************************************

"""NICOS axis test suite."""

from nicos import session
from nicos.core.sessions.utils import MASTER
from nicos.commands.basic import NewSetup


def setup_module():
    session.setMode(MASTER)


def teardown_module():
    session.unloadSetup()


def test_params():
    NewSetup('vmotor1')
    motor = session.getDevice('vmotor')
    # min/max parameters got from motor device
    assert motor.abslimits == (-100, +100)
    # usermin/usermax parameters in the config
    assert motor.userlimits == (-100, +100)

    NewSetup('vmotor2')
    motor = session.getDevice('vmotor')
    # min/max parameters got from motor device
    assert motor.abslimits == (-100, +80)
    # usermin/usermax parameters in the config
    assert motor.userlimits == (-100, +80)
