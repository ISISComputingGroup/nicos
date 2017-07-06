#  -*- coding: utf-8 -*-

description = 'Monochromator'

group = 'lowlevel'

includes = ['system', 'motorbus1', 'motorbus4', 'motorbus7', 'motorbus8',
            'motorbus9', 'motorbus14']


devices = dict(
    st_mtt = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus4',
                    addr = 52,
                    slope = -1200,
                    unit = 'deg',
                    abslimits = (-110.1, -14.1),
                    startdelay = 1,
                    stopdelay = 2,
                    zerosteps = 500000,
                    lowlevel = True,
                    confbyte = 56,
                   ),

    st_mth = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus7',
                    addr = 70,
                    slope = -400,
                    unit = 'deg',
                    abslimits = (5, 175),
                    zerosteps = 500000,
                    lowlevel = True,
                    confbyte = 44,
                   ),

    # co_mtt = device('devices.vendor.ipc.Coder',
    co_mtt = device('devices.vendor.ipc.Resolver',
                   #bus = 'motorbus8',
                    bus = 'motorbus14',
                    addr = 120,
                    slope = -182.044,
                    zerosteps = 61180,
                    unit = 'deg',
                    circular = -360,
                    confbyte = 32,
                    lowlevel = True,
                   ),

    # co_mth = device('devices.vendor.ipc.Coder',
    co_mth = device('devices.vendor.ipc.Resolver',
                   #bus = 'motorbus8',
                    bus = 'motorbus14',
                    addr = 121,
                    slope = -181.638,
                    zerosteps = 32823,
                    unit = 'deg',
                    lowlevel = True,
                   ),

    io_flag = device('devices.vendor.ipc.Input',
                    bus = 'motorbus9',
                    addr = 102,
                    first = 9,
                    last = 9,
                    unit = '',
                    lowlevel = True,
                   ),

    polyswitch = device('devices.vendor.ipc.Output',
                        bus = 'motorbus9',
                        addr = 115,
                        first = 0,
                        last = 0,
                        unit = '',
                        lowlevel = True,
                       ),

    mtt    = device('puma.mtt.MttAxis',
                    description  = 'Monochromator Two Theta',
                    motor = 'st_mtt',
                    coder = 'co_mtt',
                    io_flag = 'io_flag',
                    polyswitch = 'polyswitch',
                    obs = [],
                    precision = 0.005,
                    offset = -0.151, # -0.549 / 05.2017 GE
                    maxtries = 10,
                    jitter = 0.2,
                    dragerror = 1,
                   ),

    mth    = device('devices.generic.Axis',
                    description = 'Monochromator Theta',
                    motor = 'st_mth',
                    coder = 'co_mth',
                    obs = [],
                    precision = 0.011,
                    offset = -0.236, # 0.065 / 05.2017 GE
                    maxtries = 10,
                   ),

    # st_mfhpg = device('devices.vendor.ipc.Motor',
    #                   bus = 'motorbus7',
    #                   addr = 74,
    #                   slope = -41.5,
    #                   unit = 'deg',
    #                   abslimits = (-20, 55),
    #                   zerosteps = 27100,
    #                   lowlevel = True,
    #                   confbyte = 44,
    #                  ),

    # co_mfhpg = device('devices.vendor.ipc.Coder',
    #                   bus = 'motorbus1',
    #                   addr = 152,
    #                   slope = -28.9,
    #                   zerosteps = 2445.5,
    #                   unit = 'deg',
    #                   lowlevel = True,
    #                  ),

# test motors for focus
    st_mfh = device('puma.ipc_puma.Motor',
                    description = 'Test motor for mfh',
                    bus = 'motorbus7',
                    addr = 74,
                    slope = 1,
                    unit = 'deg',
                    abslimits = (0, 1000000),
                    zerosteps = 0,
                    lowlevel = False,
                    confbyte = 44,
                   ),

    co_mfh = device('devices.vendor.ipc.Coder',
                    description = 'Coder for test motor for mfh',
                    bus = 'motorbus1',
                    addr = 152,
                    slope = 1,
                    zerosteps = 0,
                    unit = 'deg',
                    lowlevel = False,
                   ),

    st_mfv = device('puma.ipc_puma.Motor',
                    description = 'Test motor for mfv',
                    bus = 'motorbus7',
                    addr = 75,
                    slope = 1,
                    unit = 'deg',
                    abslimits = (0, 1000000),
                    zerosteps = 0,
                    lowlevel = False,
                    confbyte = 44,
                   ),

    co_mfv = device('devices.vendor.ipc.Coder',
                    description = 'Coder for test motor for mfv',
                    bus = 'motorbus1',
                    addr = 153,
                    slope = 1,
                    zerosteps = 0,
                    unit = 'deg',
                    lowlevel = False,
                   ),

    # mfhpg  = device('puma.focus.FocusAxis',
    #                 description = 'Horizontal focus of PG-Monochromator',
    #                 motor = 'st_mfhpg',
    #                 coder = 'co_mfhpg',
    #                 obs = [],
    #                 uplimit = 70,
    #                 lowlimit = -12.0,
    #                 flatpos = 4.668,
    #                 startpos = -7.874,
    #                 precision = 0.8,
    #                 maxtries = 15,
    #                 loopdelay = 2,
    #                ),

    # st_mfvpg = device('devices.vendor.ipc.Motor',
    #                   bus = 'motorbus7',
    #                   addr = 75,
    #                   slope = 142.1,
    #                   unit = 'deg',
    #                   abslimits = (-20, 55),
    #                   zerosteps = 21603,
    #                   lowlevel = True,
    #                   confbyte = 44,
    #                   ),

    # co_mfvpg = device('devices.vendor.ipc.Coder',
    #                   bus = 'motorbus1',
    #                   addr = 153,
    #                   slope = 75.7,
    #                   zerosteps = -554.4,
    #                   unit = 'deg',
    #                   lowlevel = True,
    #                  ),

    # mfvpg  = device('puma.focus.FocusAxis',
    #                 description = 'Vertical focus of PG-Monochromator',
    #                 motor = 'st_mfvpg',
    #                 coder = 'co_mfvpg',
    #                 obs = [],
    #                 uplimit = 38,
    #                 lowlimit = 16.0,
    #                 flatpos = 37,
    #                 startpos = 38,
    #                 precision = 0.8,
    #                 maxtries = 15,
    #                 loopdelay = 2,
    #                ),

# GE311 Focusing
    st_mfhge = device('devices.vendor.ipc.Motor',
                      bus = 'motorbus7',
                      addr = 74,
                      slope = -105.5,
                      unit = 'deg',
                      abslimits = (0, 999999),
                      zerosteps = 21858,
                      lowlevel = True,
                      confbyte = 44,
                     ),

    co_mfhge = device('devices.vendor.ipc.Coder',
                      bus = 'motorbus1',
                      addr = 152,
                      slope = -20.5,
                      zerosteps = 2432,
                      unit = 'deg',
                      lowlevel = True,
                     ),

    mfhge   = device('puma.focus.FocusAxis',
                     description = 'horizontal focus of Ge311-Monochromator',
                     motor = 'st_mfhge',
                     coder = 'co_mfhge',
                     obs = [],
                     uplimit = 45,
                     lowlimit = 5,
                     flatpos = 5,
                     startpos = 5.,
                     precision = 0.8,
                     maxtries = 25,
                     loopdelay = 2,
                    ),

    st_mfvge = device('devices.vendor.ipc.Motor',
                      bus = 'motorbus7',
                      addr = 75,
                      slope = 216.6,
                      unit = 'deg',
                      abslimits = (0, 999999),
                      zerosteps = 17772.9,
                      lowlevel = True,
                      confbyte = 44,
                     ),

    co_mfvge = device('devices.vendor.ipc.Coder',
                      bus = 'motorbus1',
                      addr = 153,
                      slope = 46.0,
                      zerosteps = -260,
                      unit = 'deg',
                      lowlevel = True,
                     ),

    mfvge   = device('puma.focus.FocusAxis',
                     description = 'orizontal focus of Ge311-Monochromator',
                     motor = 'st_mfvge',
                     coder = 'co_mfvge',
                     obs = [],
                     uplimit = 45,
                     lowlimit = 10,
                     flatpos = 74,
                     startpos = 74.,
                     precision = 0.8,
                     maxtries = 25,
                     loopdelay = 2,
                    ),

# CU220 FOcusing
    st_mfhcu = device('devices.vendor.ipc.Motor',
                      bus = 'motorbus7',
                      addr = 74,
                      slope = -253.3,
                      unit = 'deg',
                      abslimits = (-30, 100),
                      zerosteps = 21242,
                      lowlevel = True,
                      confbyte = 44,
                     ),

    co_mfhcu = device('devices.vendor.ipc.Coder',
                      bus = 'motorbus1',
                      addr = 152,
                      slope = -33.8,
                      zerosteps = 2144.7,
                      unit = 'deg',
                      lowlevel = True,
                     ),

    mfhcu   = device('puma.focus.FocusAxis',
                     description = 'Horizontal focus of Cu220-Monochromator',
                     motor = 'st_mfhcu',
                     coder = 'co_mfhcu',
                     obs = [],
                     uplimit = 45,
                     lowlimit = -13.5,
                     flatpos = -13.5,
                     startpos = -15.,
                     precision = 0.8,
                     maxtries = 25,
                     loopdelay = 2,
                    ),

    st_mfvcu = device('devices.vendor.ipc.Motor',
                      bus = 'motorbus7',
                      addr = 75,
                      slope = 259.6,
                      unit = 'deg',
                      abslimits = (-25, 60),
                      userlimits = (-25, 60),
                      zerosteps = 12426.9,
                      lowlevel = True,
                      confbyte = 44,
                     ),

    co_mfvcu = device('devices.vendor.ipc.Coder',
                      bus = 'motorbus1',
                      addr = 153,
                      slope = 43.3,
                      zerosteps = -185.2,
                      unit = 'deg',
                      lowlevel = True,
                     ),

    mfvcu   = device('puma.focus.FocusAxis',
                     description = 'Vertical focus of Cu220-Monochromator',
                     motor = 'st_mfvcu',
                     coder = 'co_mfvcu',
                     obs = [],
                     uplimit = 54,
                     lowlimit = 7,
                     flatpos = 54,
                     startpos = 56,
                     precision = 0.8,
                     maxtries = 25,
                     loopdelay = 2,
                    ),

# CU111 FOcusing
    st_mfhcu1 = device('devices.vendor.ipc.Motor',
                       bus = 'motorbus7',
                       addr = 74,
                       slope = -152.7,
                       unit = 'deg',
                       abslimits = (-100, 600), #abslimits = (-20, 60),
                       userlimits = (-20,60),
                       zerosteps = 22453.6,
                       lowlevel = True,
                       confbyte = 44,
                      ),

    co_mfhcu1 = device('devices.vendor.ipc.Coder',
                       bus = 'motorbus1',
                       addr = 152,
                       slope = -33.6,
                       zerosteps = 2970.1,
                       unit = 'deg',
                       lowlevel = True,
                      ),

    mfhcu1  = device('puma.focus.FocusAxis',
                     description = 'Horizontal focus of Cu220-Monochromator',
                     motor = 'st_mfhcu1',
                     coder = 'co_mfhcu1',
                     obs = [],
                     uplimit = 40,
                     lowlimit = -3.5,
                     flatpos = -3.5,
                     startpos = -4.,
                     precision = 0.8,
                     maxtries = 25,
                     loopdelay = 2,
                    ),

    st_mfvcu1 = device('devices.vendor.ipc.Motor',
                       bus = 'motorbus7',
                       addr = 75,
                       slope = 380.5,
                       unit = 'deg',
                       abslimits = (-20, 60),
                       zerosteps = 12130.6,
                       lowlevel = True,
                       confbyte = 44,
                      ),

    co_mfvcu1 = device('devices.vendor.ipc.Coder',
                       bus = 'motorbus1',
                       addr = 153,
                       slope = 42.1,
                       zerosteps = 97.9,
                       unit = 'deg',
                       lowlevel = True,
                      ),

    mfvcu1 = device('puma.focus.FocusAxis',
                    description = 'Vertical focus of Cu220-Monochromator',
                    motor = 'st_mfvcu1',
                    coder = 'co_mfvcu1',
                    obs = [],
                    uplimit = 52,
                    lowlimit = 15,
                    flatpos = 52,
                    startpos = 54,
                    precision = 0.8,
                    maxtries = 25,
                    loopdelay = 2,
                   ),
# Tilt and Translation

    st_mty = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus7',
                    addr = 71,
                    slope = 200,
                    unit = 'mm',
                    abslimits = (0, 90),
                    zerosteps = 500000,
                    lowlevel = True,
                    confbyte = 44,
                   ),

    co_mty = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 151,
                    slope = 36.37,
                    zerosteps = 17,
                    unit = 'mm',
                    lowlevel = True,
                   ),

    mty    = device('devices.generic.Axis',
                    description = 'Translation of Monochromator (corrects '
                                  'depth of crystals',
                    motor = 'st_mty',
                    coder = 'st_mty',
                    obs = [],
                    precision = 0.3,
                    offset = 0,
                    maxtries = 10,
                    loopdelay = 1,
                   ),

    st_mgx = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus7',
                    addr = 73,
                    slope = 400,
                    unit = 'deg.',
                    abslimits = (-3.6, 3.6),
                    zerosteps = 500000,
                    lowlevel = True,
                    confbyte = 44,
                   ),

    mgx   = device('devices.generic.Axis',
                   description = 'tilt of monochromator (up/down)',
                   motor = 'st_mgx',
                   coder = 'st_mgx',
                   obs = [],
                   precision = 0.1,
                   offset = 0,
                   maxtries = 10,
                   backlash = 0.25,
                  ),

    st_mgy = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus7',
                    addr = 72,
                    slope = -400,
                    unit = 'deg.',
                    abslimits = (-3.6, 3.6),
                    zerosteps = 500000,
                    lowlevel = True,
                    confbyte = 44,
                   ),

    mgy   = device('devices.generic.Axis',
                   description = 'tilt of monochromator',
                   motor = 'st_mgy',
                   coder = 'st_mgy',
                   obs = [],
                   precision = 0.1,
                   offset = 0,
                   maxtries = 10,
                   backlash = 0.25,
                  ),
)
