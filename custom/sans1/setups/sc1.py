#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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
#   Andreas Wilhelm <andreas.wilhelm@frm2.tum.de>
#
# *****************************************************************************

description = 'sample table devices'

group = 'optional'

includes = ['table_top']

nethost = '//sans1srv.sans1.frm2/'

devices = dict(
    samplenameselector = device('devices.generic.ParamDevice',
                                description = 'Paramdevice used to select the right samplename',
                                lowlevel = True,
                                device = 'Sample',
                                parameter = 'activesample',
                               ),

    sc1_y    = device('devices.taco.axis.Axis',
                      description = 'Sample Changer 1 Axis',
                      lowlevel = True,
                      tacodevice = nethost + 'sans1/samplechanger/y-sc1',
                      fmtstr = '%.2f',
                      abslimits = (-0, 600),
                     ),

    sc1    = device('devices.generic.MultiSwitcher',
                       description = 'Sample Changer 1 Huber device',
                       moveables = ['sc1_y', 'z_2b', 'samplenameselector'],
                       mapping = {'1':  [594.5, -31, 1],  '2': [535.5, -31, 2],
                                  '3':  [476.5, -31, 3],  '4': [417.5, -31, 4],
                                  '5':  [358.5, -31, 5],  '6': [299.5, -31, 6],
                                  '7':  [240.5, -31, 7],  '8': [181.5, -31, 8],
                                  '9':  [122.5, -31, 9], '10': [ 63.5, -31, 10],
                                  '11': [  4.5, -31, 11],
                                  '12': [594.5,  28, 12], '13': [535.5,  28, 13],
                                  '14': [476.5,  28, 14], '15': [417.5,  28, 15],
                                  '16': [358.5,  28, 16], '17': [299.5,  28, 17],
                                  '18': [240.5,  28, 18], '19': [181.5,  28, 19],
                                  '20': [122.5,  28, 20], '21': [ 63.5,  28, 21],
                                  '22': [  4.5,  28, 22],
                                  },
                       precision = [0.05, 0.05, 100], # for use without nicos
                       #~ precision = [0.05, 0.05, 0], # for use with nicos
                       blockingmove = False,
                      ),

    SampleChanger = device('devices.generic.DeviceAlias',
                            description = 'Alias to the current active Samplechanger or to nothing',
                            alias = 'sc1',
                            )
)
