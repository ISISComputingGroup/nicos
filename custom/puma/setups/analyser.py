#  -*- coding: utf-8 -*-

description = 'Analysator'

includes = ['system', 'motorbus2', 'motorbus6', 'motorbus1']

group = 'lowlevel'

devices = dict(
# Att and ATH
     st_att = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus2',
                    addr = 60,
                    slope = -538,
                    unit = 'deg',
                    abslimits = (-117, 1),
                    zerosteps = 500000,
                    lowlevel = True,
                    ),

    st_ath = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus6',
                    addr = 92,
                    slope = -200,
                    unit = 'deg',
                    abslimits = (0, 60),
                    zerosteps = 500000,
                    lowlevel = True,
                    ),

    co_att = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 130,
                    slope = 2912.7111,
                    zerosteps = 124422,
                    unit = 'deg',
                    circular = -360,
                    lowlevel = True,
                    ),

    co_ath = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 131,
                    slope = 2912.7111,
                    zerosteps = 476397,
                    unit = 'deg',
                    lowlevel = True,
                    ),

    att    = device('devices.generic.Axis',
                    description = 'Scattering angle two-theta of analyser',
                    motor = 'st_att',
                    coder = 'co_att',
                    obs = [],
                    precision = 0.005,
                    offset = 0.612, # focused
 #                   offset = 0.307, # with collimator
                    maxtries = 8,
                    ),

    ath    = device('devices.generic.Axis',
                    description = 'Rocking angle theta of analyser',
                    motor = 'st_ath',
                    coder = 'co_ath',
                    obs = [],
                    precision = 0.01,
#                   offset = -0.678, #with collimator
                    offset = -0.8332, #focussed
                    maxtries = 8,
                    ),

# Focusing

   st_afpg = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus6',
                    addr = 90,
                    slope = -403.226,
                    unit = 'deg',
                    abslimits = (-55, 55),
                    zerosteps = 505306.456,
                    lowlevel = True,
                    ),

   co_afpg = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 159,
                    slope = -55.743,
                    zerosteps = 3864.42,
                    unit = 'deg',
                    lowlevel = True,
                    ),
   afpg   = device('puma.focus.focus_Axis',
                   description = 'Horizontal focus of PG-analyser',
                   motor = 'st_afpg',
                   coder = 'co_afpg',
                   obs = [],
                   uplimit = 55,
                   lowlimit = -55,
                   abslimits = (-55, 55),
                   flatpos = 4.92,
                   startpos = 4,
                   precision = 0.25,
                   maxtries = 15,
                   ),

# Tilt and Translation

   st_atx = device('devices.vendor.ipc.Motor',
                   bus = 'motorbus6',
                   addr = 89,
                   slope = 5000,
                   unit = 'mm',
                   abslimits = (-10.1, 7.6),
                   zerosteps = 500000,
                   lowlevel = True,
                   ),


   co_atx = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 156,
                    slope = 76.57,
                    zerosteps = 2404,
                    unit = 'mm',
                    lowlevel = True,
                    ),

    atx    = device('devices.generic.Axis',
                    description = 'Translation of analyser',
                    motor = 'st_atx',
                    coder = 'co_atx',
                    obs = [],
                    precision = 0.1,
                    offset = 0,
                    maxtries = 10,
                    loopdelay = 1,
                    ),

   st_aty = device('devices.vendor.ipc.Motor',
                   bus = 'motorbus6',
                   addr = 88,
                   slope = -5000,
                   unit = 'mm',
                   abslimits = (-6.1, 5.1),
                   zerosteps = 500000,
                   lowlevel = True,
                   ),


   co_aty = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 157,
                    slope = 77.57,
                    zerosteps = 2392,
                    unit = 'mm',
                    lowlevel = True,
                    ),

    aty    = device('devices.generic.Axis',
                    description = 'Translation of analyser (corrects depth of pg-crystals)',
                    motor = 'st_aty',
                    coder = 'co_aty',
                    obs = [],
                    precision = 0.1,
                    offset = 0,
                    maxtries = 10,
                    loopdelay = 1,
                    ),

   st_agx = device('devices.vendor.ipc.Motor',
                   bus = 'motorbus6',
                   addr = 87,
                   slope = 5000,
                   unit = 'mm',
                   abslimits = (-5.5, 5.5),
                   zerosteps = 500000,
                   lowlevel = True,
                   ),

    agx   = device('devices.generic.Axis',
                    description = 'Tilt of analyser (up/down scattering)',
                    motor = 'st_agx',
                    coder = 'st_agx',
                    obs = [],
                    precision = 0.05,
                    offset = 0,
                    maxtries = 10,
                    backlash = 0.2,
                    ),

    st_agy = device('devices.vendor.ipc.Motor',
                   bus = 'motorbus6',
                   addr = 86,
                   slope = -5000,
                   unit = 'mm',
                   abslimits = (-5.5, 4.5),
                   zerosteps = 500000,
                   lowlevel = True,
                   ),

    agy   = device('devices.generic.Axis',
                    description = 'Tilt of analyser',
                    motor = 'st_agy',
                    coder = 'st_agy',
                    obs = [],
                    precision = 0.05,
                    offset = 0,
                    maxtries = 10,
                    backlash = 0.2,
                    ),
)
