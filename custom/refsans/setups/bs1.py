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
#   Matthias Pomm <matthias.pomm@hzg.de>
#
# **************************************************************************

description = 'double slit'

group = 'optional'

nethost = 'refsanssrv.refsans.frm2'
tacodev = '//%s/test' % nethost

devices = dict(
    bs1_mr = device('devices.taco.Motor',
                    description = 'SlitMotor reactor side',
                    tacodevice = '%s/bs1/mr' % tacodev,
                    abslimits = (-178.0, -0.7),
                   ),
    bs1_ms = device('devices.taco.Motor',
                    description = 'SlitMotor sample side',
                    tacodevice = '%s/bs1/ms' % tacodev,
                    abslimits = (-177.002, 139.998),
                   ),
)
