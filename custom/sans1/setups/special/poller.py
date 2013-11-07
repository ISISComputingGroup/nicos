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
#   Andreas Wilhem <andreas.wilhelm@frm2.tum.de>
#
# *****************************************************************************

description = 'setup for the poller'
group = 'special'

sysconfig = dict(
    cache = 'sans1ctrl.sans1.frm2'
)

devices = dict(
   Poller = device('services.poller.Poller',
                   alwayspoll = ['tube', 'collimation', 'table_top',
                                 'table_bottom', 'magnet_sans1', 'pressure',
                                 'htf03', 'detector', 'selector', 'ccr12',
                                 'guidehall', 'reactor', 'nl4a', 'spin_flipper',
                                 'sc1', 'newport02', 'newport03', 'ccr10', 'memograph',
                                 'ccr12', 'ccr16',
                                ],
                   blacklist = [],
                  ),
)
