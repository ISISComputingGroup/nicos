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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#   Andreas Wilhelm <andreas.wilhelm@frm2.tum.de>
#
# *****************************************************************************

#
# Ist noch als AnNA.tel device vorhanden!!! geht noch nicht!!!
#

description = 'Selector'

includes = ['system']

group = 'lowlevel'

nethost = 'sans1srv.sans1.frm2'

devices = dict(
#   at    = device('devices.generic.Axis',
#                  motor = 'atmot',
#                  coder = 'atenc',
#                  tacodevice = nethost + 'sel/sel/z',
#                  fmtstr = '%.2f',
#                  abslimits = (0, 500), #need to check
#                 ),
    atmot = device('devices.taco.motor.Motor',
                   tacodevice ='//%s/sans1/z/motor' % (nethost, ),
                   fmtstr = '%.2f',
                   abslimits = (0, 500), #need to check
                  ),
    atenc = device('devices.taco.coder.Coder',
                   tacodevice = '//%s/sans1/z/enc' % (nethost, ),
                   fmtstr = '%.2f',
                  ),

)
