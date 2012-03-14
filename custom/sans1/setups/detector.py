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

description = 'detector related devices'

includes = ['system']
# excludes = ['excluded']

nethost= '//sans1srv.sans1.frm2/'

devices = dict(
    hv_interlock = device('nicos.taco.DigitalInput',
                          tacodevice = nethost + 'sans1/interlock/hv',
                          ),
    hv_discharge_mode = device('nicos.taco.DigitalInput',
                               tacodevice = nethost + 'sans1/interlock/hv',
                              ),
    hv_discharge = device('nicos.taco.DigitalOutput',
                          tacodevice = nethost + 'sans1/interlock/discharge',
                         ),
    hv = device('nicos.taco.VoltageSupply',
                tacodevice = nethost + 'sans1/iseg/hv',
                abslimits = [0, 1550],
               ),
    hv_current = device('nicos.taco.AnalogInput',
                        tacodevice = nethost + 'sans1/iseg/hv-current',
                       ),
)

