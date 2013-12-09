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

description = 'system setup'

sysconfig = dict(
    cache = 'sans1ctrl.sans1.frm2',
    instrument = 'Instrument',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = [],
)

modules = ['nicos.commands.standard', 'sans1.commands']

# SYSTEM NEVER INCLUDES OTHER SETUPS !!!

devices = dict(
    #~ Sample   = device('devices.experiment.Sample'),
    Sample   = device('sans1.sans1_sample.Sans1Sample'),

    Instrument = device('devices.instrument.Instrument',
                        responsible = 'Dr. habil. Ralph Gilles',
                       ),

    Exp      = device('devices.experiment.Experiment',
                      dataroot = '/data/nicos',
                      sample = 'Sample'),

    filesink = device('devices.datasinks.AsciiDatafileSink',
                     ),

    conssink = device('devices.datasinks.ConsoleSink'),

    daemonsink = device('devices.datasinks.DaemonSink'),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      # only specify if differing from Exp.dataroot
                      #path = '/data/nicos',
                      minfree = 0.5,
                     ),
)
