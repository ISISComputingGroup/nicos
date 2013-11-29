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

description = 'collimation tube'

includes = ['system']

excludes = ['collimation_config']

# included by sans1
group = 'lowlevel'

nethost = 'sans1srv.sans1.frm2'

devices = dict(
    col = device('nicos.devices.generic.LockedDevice',
                  description = 'sans1 primary collimation',
                  lock = 'at',
                  device = 'col_sw',
                  #lockvalue = None,     # go back to previous value
                  unlockvalue = 'x1000',
                  #keepfixed = False,	# dont fix attenuator after movement
                  lowlevel = False,
               ),
    col_sw = device('devices.generic.MultiSwitcher',
                  description = 'collimator switching device',
                  precision = None,
                  blockingmove = False,
                  unit = 'm',
                  fmtstr = '%.1f',
                  fallback = 'Error',
                  moveables = ['col_20a', 'col_20b', 'col_16a', 'col_16b', 'col_12a', 'col_12b',
                               'col_8a', 'col_8b', 'col_4a', 'col_4b', 'col_2a', 'col_2b'],
                  # col_2b disabled !!!
                  mapping = {
                      #~ 1:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG'],
                      1.5: ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL'],
                      2:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL'],
                      3:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL'],
                      4:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL'],
                      6:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL'],
                      8:   ['NG',  'NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      10:  ['NG',  'NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      12:  ['NG',  'NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      14:  ['NG',  'NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      16:  ['NG',  'NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      18:  ['NG',  'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                      20:  ['COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL', 'COL'],
                  },
                  lowlevel = True,
                ),

    at = device('sans1.collimotor.Sans1ColliSwitcher',
                    description = 'Attenuator',
                    mapping = dict(P1=0, P2=117, P3=234, P4=351, OPEN=0, x1000=117, x100=234, x10=351),
                    moveable = 'at_m',
                    ),
    at_m = device('sans1.collimotor.Sans1ColliMotor',
                    description = 'Attenuator motor',
                    # IP-adresse: 172.16.17.1
                    tacodevice='//%s/sans1/coll/ng-pol'% (nethost,),
                    address = 0x4020+0*10,
                    slope = 200*4, # FULL steps per turn * turns per mm
                    microsteps = 8,
                    unit = 'mm',
                    refpos = -23.0,
                    abslimits = (-400, 600),
                    lowlevel = True,
                  ),

    ng_pol = device('sans1.collimotor.Sans1ColliSwitcher',
                    description = 'Neutronguide polariser',
                    mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, POL1=117, POL2=234, LAS=354),
                    moveable = 'ng_pol_m',
                    ),
    ng_pol_m = device('sans1.collimotor.Sans1ColliMotor',
                    description = 'Neutronguide polariser motor',
                    # IP-adresse: 172.16.17.1
                    tacodevice='//%s/sans1/coll/ng-pol'% (nethost,),
                    address = 0x4020+1*10,
                    slope = 200*4, # FULL steps per turn * turns per mm
                    microsteps = 8,
                    unit = 'mm',
                    refpos = -4.5,
                    abslimits = (-400, 600),
                    lowlevel = True,
                  ),

    col_20a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 20a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_20a_m',
                      ),
    col_20a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 20a motor',
                      # IP-adresse: 172.16.17.2
                      tacodevice='//%s/sans1/coll/col-20m'% (nethost,),
                      address = 0x4020+0*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -5.39,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_20b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 20b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_20b_m',
                      ),
    col_20b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 20b',
                      # IP-adresse: 172.16.17.2
                      tacodevice='//%s/sans1/coll/col-20m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -5.28,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    bg1 = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Background slit1',
                      mapping = {'P1':0, 'P2':90, 'P3':180, 'P4':270,
                                 '50mm':0, 'OPEN':90, '20mm':180, '42mm':270 },
                      moveable = 'bg1_m',
                      ),
    bg1_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Background slit1 motor',
                      # IP-adresse: 172.16.17.3
                      tacodevice='//%s/sans1/coll/col-16m'% (nethost,),
                      address = 0x4020+0*10,
                      slope = 200*0.16, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'deg',
                      refpos = -28.85,
                      abslimits = (-40, 300),
                      lowlevel = True,
                    ),

    col_16a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 16a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_16a_m',
                      ),
    col_16a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 16a motor',
                      # IP-adresse: 172.16.17.3
                      tacodevice='//%s/sans1/coll/col-16m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -4.29,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_16b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 16b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_16b_m',
                      ),
    col_16b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 16b motor',
                      # IP-adresse: 172.16.17.3
                      tacodevice='//%s/sans1/coll/col-16m'% (nethost,),
                      address = 0x4020+2*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -2.31,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_12a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 12a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_12a_m',
                      ),
    col_12a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 12a motor',
                      # IP-adresse: 172.16.17.4
                      tacodevice='//%s/sans1/coll/col-12m'% (nethost,),
                      address = 0x4020+0*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -1.7,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_12b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 12b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_12b_m',
                      ),
    col_12b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 12b motor',
                      # IP-adresse: 172.16.17.4
                      tacodevice='//%s/sans1/coll/col-12m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -9.999, #XXX: Angabe fehlt in Doku !!!
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    bg2 = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Background slit2',
                      mapping = {'P1':0, 'P2':90, 'P3':180, 'P4':270,
                                 '28mm':0, '20mm':90, '12mm':180, 'OPEN':270 },
                      moveable = 'bg2_m',
                      ),
    bg2_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Background slit2 motor',
                      # IP-adresse: 172.16.17.5
                      tacodevice='//%s/sans1/coll/col-8m'% (nethost,),
                      address = 0x4020+0*10,
                      slope = 200*0.16, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'deg',
                      refpos = -1.5,
                      abslimits = (-40, 300),
                      lowlevel = True,
                    ),

    col_8a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 8a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_8a_m',
                      ),
    col_8a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 8a motor',
                      # IP-adresse: 172.16.17.5
                      tacodevice='//%s/sans1/coll/col-8m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -3.88,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_8b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 8b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_8b_m',
                      ),
    col_8b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 8b motor',
                      # IP-adresse: 172.16.17.5
                      tacodevice='//%s/sans1/coll/col-8m'% (nethost,),
                      address = 0x4020+2*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -4.13,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_4a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 4a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_4a_m',
                      ),
    col_4a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 4a motor',
                      # IP-adresse: 172.16.17.6
                      tacodevice='//%s/sans1/coll/col-4m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -9.37,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    col_4b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 4b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_4b_m',
                      ),
    col_4b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 4b motor',
                      # IP-adresse: 172.16.17.6
                      tacodevice='//%s/sans1/coll/col-4m'% (nethost,),
                      address = 0x4020+2*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -9.35,
                      abslimits = (-400, 600),
                      lowlevel = True,
                    ),

    sa1 = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'attenuation slits',
                      mapping = {'P1':0, 'P2':70, 'P3':140, 'P4':210,
                                 '50x50':0, '30mm':70, '20mm':140, '10mm':210 },
                      moveable = 'sa1_m',
                      ),
    sa1_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'attenuation slits motor',
                      # IP-adresse: 172.16.17.7
                      tacodevice='//%s/sans1/coll/col-2m'% (nethost,),
                      address = 0x4020+0*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -34.7,
                      abslimits = (-40, 300),
                      lowlevel = True,
                    ),

    col_2a = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 2a',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_2a_m',
                      ),
    col_2a_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 2a motor',
                      # IP-adresse: 172.16.17.7
                      tacodevice='//%s/sans1/coll/col-2m'% (nethost,),
                      address = 0x4020+1*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -8.,
                      abslimits = (-400, 600),
                      autopower = 'on',
                      autozero = 10,
                      lowlevel = True,
                    ),

    col_2b = device('sans1.collimotor.Sans1ColliSwitcher',
                      description = 'Collimotor 2b',
                      mapping = dict(P1=0, P2=117, P3=234, P4=351, NG=0, COL=117, free=234, LAS=351),
                      moveable = 'col_2b_m',
                      ),
    col_2b_m = device('sans1.collimotor.Sans1ColliMotor',
                      description = 'Collimotor 2b motor',
                      # IP-adresse: 172.16.17.7
                      tacodevice='//%s/sans1/coll/col-2m'% (nethost,),
                      address = 0x4020+2*10,
                      slope = 200*4, # FULL steps per turn * turns per mm
                      microsteps = 8,
                      unit = 'mm',
                      refpos = -9.,
                      abslimits = (-400, 600),
                      fixed = 'unreliable, do not use !',
                      fixedby = ('setupfile', 99),      # deny release!
                      lowlevel = True,
                    ),
# pump devices of 172.17.17.10 are at modbus-tacodevice //sans1srv.sans.frm2/sans1/coll/pump
)
