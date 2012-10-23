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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""Module for MIRA specific commands."""

__version__ = "$Revision$"

import time

from nicos import session
from nicos.commands import usercommand
from nicos.commands.output import printinfo
from nicos.commands.device import move, read


@usercommand
def FlushCryo():
    CryoGas = session.getDevice('CryoGas')
    CryoVac = session.getDevice('CryoGas')
    Pcryo = session.getDevice('CryoGas')
    move(CryoGas, 'on')
    while Pcryo.read() < 995:
        time.sleep(1)
    time.sleep(5)
    read(Pcryo)
    move(CryoGas, 'off')
    move(CryoVac,'on')
    while Pcryo.read() > 0.15:
        time.sleep(1)
    time.sleep(5)
    read(Pcryo)
    move(CryoVac, 'off')
    printinfo('Cryo flushed!')

@usercommand
def SetCryoGas(target):
    CryoGas = session.getDevice('CryoGas')
    CryoVac = session.getDevice('CryoGas')
    Pcryo = session.getDevice('CryoGas')
    move(CryoGas,'on')
    while Pcryo.read() < target:
        time.sleep(0.01)
    move(CryoGas,'off')

@usercommand
def SetCryoVac(target):
    CryoGas = session.getDevice('CryoGas')
    CryoVac = session.getDevice('CryoGas')
    Pcryo = session.getDevice('CryoGas')
    move(CryoVac,'on')
    while Pcryo.read() > target:
        time.sleep(0.01)
    move(CryoVac,'off')
