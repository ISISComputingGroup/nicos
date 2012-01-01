#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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
#   Tobias Weber <tobias.weber@frm2.tum.de>
#
# *****************************************************************************

name = 'test switcher'

includes = ['system']

devices = dict(

    motor_1 = device(
        'nicos.generic.VirtualMotor',
        unit = 'mm',
        initval = 0,
        abslimits = (0, 100),
    ),

    switcher_1 = device('nicos.generic.Switcher',
                        description = 'switcher',
                        states = ['0', '10', '20', '30', '1000', '-10'],
                        values = [0, 10, 20, 30, 1000, -10],
                        precision = 0,
                        moveable='motor_1'),

    broken_switcher = device('nicos.generic.Switcher',
                              description = 'broker switcher',
                              states = ['0', '10', '20'],
                              values = [0, 10],
                              precision = 0,
                              moveable='motor_1'),

)
