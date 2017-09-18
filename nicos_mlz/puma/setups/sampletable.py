#  -*- coding: utf-8 -*-

description = 'Sample table'


includes = ['motorbus1', 'motorbus2', 'motorbus4', 'motorbus5', 'motorbus3']

devices = dict(
    st_phi = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus4',
                    addr = 53,
                    slope = 400,
                    unit = 'deg',
                    abslimits = (-5, 116.1),
                    userlimits = (9, 115),
                    zerosteps = 500000,
                    confbyte = 120,
                    speed = 10,
                    accel = 100,
                    microstep = 2,
                    startdelay = 1,
                    stopdelay = 3,
                    ramptype = 4,
                    lowlevel = True,
                   ),

    co_phi = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 128,
                    slope = -(2**26)/360.,
                    zerosteps = 9392594,
                    confbyte = 154,
                    unit = 'deg',
                    circular = 360, # map values to -180..0..180 degree
                    lowlevel = True,
                   ),

    phi    = device('nicos.devices.generic.Axis',
                    description = 'Sample scattering angle Two Theta',
                    motor = 'st_phi',
                    coder = 'co_phi',
                    obs = [],
                    precision = 0.005,
                    offset = 0.21, #May 2017 done by GE
                    maxtries = 10,
                    loopdelay = 1,
                    jitter = 0.2,
                    dragerror = 1,
                   ),

# Magnet phi
    # phi = device('nicos_mlz.puma.devices.comb_ax.CombAxis',
    #              description = 'Sample scattering angle Two Theta',
    #              motor = 'st_phi',
    #              coder = 'co_phi',
    #              obs = [],
    #              precision = 0.005,
    #              offset = 0.21,
    #              maxtries = 5,
    #              loopdelay = 1,
    #              fix_ax = 'psi_puma',
    #              iscomb = False,
    #             ),

    st_psi  = device('nicos.devices.vendor.ipc.Motor',
                     bus = 'motorbus2',
                     addr = 58,
                     slope = -400,
                     unit = 'deg',
                     abslimits = (-1000, 1000),
                     userlimits = (5, 355),
                     zerosteps = 602799,
                     lowlevel = True,
                     confbyte = 60,
                     speed = 50,
                     accel = 100,
                     microstep = 1,
                     startdelay = 0,
                     stopdelay = 0,
                     ramptype = 1,
                    ),

    co_psi  = device('nicos.devices.vendor.ipc.Coder',
                     bus = 'motorbus1',
                     addr = 129,
                     slope = -(2**20)/360.,
                     zerosteps = 954700,
                     unit = 'deg',
                     lowlevel = True,
                     circular = 360,
                     confbyte = 148,
                    ),

    psi_puma  = device('nicos.devices.generic.Axis',
                       description = 'Sample rocking angle Theta',
                       motor = 'st_psi',
                       coder = 'co_psi',
                       obs = [],
                       precision = 0.005,
                       offset = 0,
                       userlimits = (5, 355),
                       maxtries = 5,
                      ),

     psi    = device('nicos.devices.generic.DeviceAlias',
                     description  = 'Sample rocking angle Theta',
                     alias = 'psi_puma',
# when magnet is on :
                     # alias = 'sth_m7T5_ccr',
                     devclass = 'nicos.devices.generic.Axis',
# when magnet is on :
                     # devclass = 'nicos.devices.taco.Axis',
                    ),

# Tilting

    st_sgx = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus3',
                    addr = 64, #67
                    slope = -1600,
                    unit = 'deg',
                    abslimits = (-15.6, 15.6),
                    zerosteps = 500000,
                    microstep = 8,
                    speed = 50,
                    lowlevel = True,
                   ),

    st_sgy = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus3',
                    addr = 65, #68
                    slope = -1600,
                    unit = 'deg',
                    abslimits = (-15.6, 15.6),
                    zerosteps = 500000,
                    microstep = 8,
                    speed = 50,
                    lowlevel = True,
                   ),

    co_sgx = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus3',
                    addr = 70,
                    slope = -8192,
                    zerosteps = 33466203,
                    circular = -4096,    # 12 bit (4096) for turns, times 2 deg per turn divided by 2 (+/-) from PANDA
                    unit = 'deg',
                    lowlevel = True,
                   ),

    co_sgy = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus3',
                    addr = 71,
                    slope = -8192,
                    zerosteps = 33553860,
                    circular = -4096,    # 12 bit (4096) for turns, times 2 deg per turn divided by 2 (+/-) from PANDA
                    unit = 'deg',
                    lowlevel = True,
                   ),

    sgx    = device('nicos.devices.generic.Axis',
                    description = 'Sample tilt around X',
                    motor = 'st_sgx',
                    # coder = 'co_sgx',
                    obs = [],
                    precision = 0.02,
                    offset = 0,
                    fmtstr = '%.3f',
                    maxtries = 5,
                   ),

    sgy    = device('nicos.devices.generic.Axis',
                    description = 'Sample tilt around Y',
                    motor = 'st_sgy',
                    # coder = 'co_sgy',
                    obs = [],
                    precision = 0.02,
                    offset = 0,
                    fmtstr = '%.3f',
                    maxtries = 5,
                   ),

# Translation

    st_stx = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus3',
                    addr = 66,
                    slope = -6030.6, #2017.07.04
                    unit = 'mm',
                    abslimits = (-18.1, 18.1),
                    zerosteps = 500000,
                    microstep = 8,
                    precision = 0.005,
                    lowlevel = True,
                   ),

    st_sty = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus3',
                    addr = 67, #65
                    slope = -6250.0, #2015.03.09,
                    unit = 'mm',
                    abslimits = (-18.1, 18.1),
                    zerosteps = 500000,
                    microstep = 8,
                    precision = 0.005,
                    lowlevel = True,
                   ),

    co_stx = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus3',
                    addr = 74,
                    slope = -194.53,    #2015.02.20
                    zerosteps = 4686,   #2017.07.04
                    unit = 'mm',
                    lowlevel = True,
                   ),

    co_sty = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus3',
                    addr = 75,
                    slope = -189,
                    zerosteps = 5138,
                    unit = 'mm',
                    lowlevel = True,
                   ),

    stx    = device('nicos.devices.generic.Axis',
                    description = 'Sample translation along X',
                    motor = 'st_stx',
                    coder = 'co_stx',
                    obs = [],
                    precision = 0.05,
                    offset = 0.0,
                    fmtstr = '%.3f',
                    maxtries = 9,
                    loopdelay = 1,
                    abslimits = (-18.1, 18.1),
                   ),

    sty    = device('nicos.devices.generic.Axis',
                    description = 'Sample translation along Y',
                    motor = 'st_sty',
                    coder = 'co_sty',
                    obs = [],
                    precision = 0.05,
                    offset = 0.0,
                    fmtstr = '%.3f',
                    maxtries = 9,
                    loopdelay = 1,
                   ),

    st_stz = device('nicos.devices.vendor.ipc.Motor',
                    bus = 'motorbus3',
                    addr = 68, #64
                    slope = -22400,
                    unit = 'mm',
                    abslimits = (-20, 20),
                    zerosteps = 500000,
                    microstep = 2,
                    lowlevel = True,
                   ),

    co_stz = device('nicos.devices.vendor.ipc.Coder',
                    bus = 'motorbus3',
                    addr = 76,
                    slope = 190,
                    zerosteps = 4968,
                    unit = 'mm',
                    lowlevel = True,
                   ),

    stz    = device('nicos.devices.generic.Axis',
                    description = 'Sample translation along Z',
                    motor = 'st_stz',
                    # coder = 'co_stz',
                    obs = [],
                    precision = 0.1,
                    offset = 0,
                    fmtstr = '%.2f',
                    maxtries = 10,
                    loopdelay = 2,
                   ),
)

alias_config = {
    'psi': {'psi_puma': 0},
}
