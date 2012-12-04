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
#   Tobias Weber <tobias.weber@frm2.tum.de>
#
# *****************************************************************************

name = 'test system setup'

sysconfig = dict(
    cache = 'localhost:14877',
    experiment = 'Exp',
    instrument = 'Tas',
    datasinks = ['testsink'],
)

modules = ['nicos.commands.tas']


devices = dict(
    sample   = device('devices.tas.TASSample',
                     ),

    testsink = device('test.utils.TestSink',
                     ),

    # test that both nicos.(...) and (...) work
    Exp      = device('nicos.devices.experiment.Experiment',
                      sample = 'sample',
                      elog = False,
                      dataroot = 'test/root/data',
                      propprefix = 'p',
                      templatedir = '../../script_templates',
                      zipdata = True,
                      managerights = False,  # set to True for a single test
                      serviceexp = 'service',
                      lowlevel = False
                     ),

    t_phi    = device('devices.generic.VirtualMotor',
                      abslimits = (-180, 180),
                      initval = 0,
                      speed = 0,
                      jitter = 0.01,
                      unit = 'deg',
                     ),

    t_psi    = device('devices.generic.VirtualMotor',
                      abslimits = (0, 360),
                      initval = 0,
                      speed = 0,
                      jitter = 0.01,
                      unit = 'deg',
                     ),

    t_mono   = device('devices.tas.Monochromator',
                      unit = 'A-1',
                      theta = 't_mth',
                      twotheta = 't_mtt',
                      focush = None,
                      focusv = None,
                      abslimits = (0, 10),
                      dvalue = 3.325,
                     ),

    t_mth    = device('devices.generic.VirtualMotor',
                      curvalue = 10,
                      unit = 'deg',
                      abslimits = (-180, 180),
                      jitter = 0.02,
                     ),

    t_mtt    = device('devices.generic.VirtualMotor',
                      curvalue = 20,
                      unit = 'deg',
                      abslimits = (-180, 180),
                     ),

    t_ana    = device('devices.tas.Monochromator',
                      unit = 'A-1',
                      theta = 't_ath',
                      twotheta = 't_att',
                      focush = None,
                      focusv = None,
                      reltheta = True,
                      abslimits = (0, 10),
                      dvalue = 3.325,
                     ),

    t_ath    = device('devices.generic.VirtualMotor',
                      curvalue = 10,
                      unit = 'deg',
                      abslimits = (-180, 180),
                      jitter = 0.02,
                     ),

    t_att    = device('devices.generic.VirtualMotor',
                      curvalue = -20,
                      unit = 'deg',
                      abslimits = (-180, 180),
                     ),

    t_ki     = device('devices.tas.Wavevector',
                      unit = 'A-1',
                      base = 't_mono',
                      tas = 'Tas',
                      scanmode = 'CKI',
                     ),

    t_kf     = device('devices.tas.Wavevector',
                      unit = 'A-1',
                      base = 't_ana',
                      tas = 'Tas',
                      scanmode = 'CKF',
                     ),

    t_alpha  = device('devices.generic.VirtualMotor',
                      curvalue = 0,
                      unit = 'deg',
                      abslimits = (-360, 360),
                     ),

    Tas      = device('devices.tas.TAS',
                      cell = 'sample',
                      mono = 't_mono',
                      phi = 't_phi',
                      psi = 't_psi',
                      ana = 't_ana',
                      alpha = 't_alpha',
                      instrument = 'Tas',
                     ),
)
