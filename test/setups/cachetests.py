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
#   Björn Pedersen <bjoern.pedersen@frm2.tum.de>
#
# *****************************************************************************

name = 'setup for cache tests'

sysconfig = dict(
    cache = 'localhost:14877',
    datasinks = ['testsink'],
    loglevel = 'debug',
)

devices = dict(
    testsink = device('test.utils.TestSink',
                     ),
    reader1 = device('nicos.devices.generic.cache.CacheReader',
                      description='Test Reader',
                      maxage=30,
                      unit='',
                      loglevel='debug'
                     ),
    writer1 = device('nicos.devices.generic.cache.CacheWriter',
                      description='Test cache writer',
                      userlimits=(1, 200),
                      abslimits=(0, 311),
                      maxage=1,
                      unit='',
                      loglevel='debug'
                     ),
)
