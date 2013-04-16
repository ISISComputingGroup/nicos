#  -*- coding: utf-8 -*-

description = 'Monochanger'

group = 'optional'

includes = ['system', 'motorbus1', 'motorbus4', 'motorbus7']

devices = dict(
    st_lift = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus4',
                    addr = 51,
                    slope = -160,
                    unit = 'mm',
                    abslimits = (-144, 360),
                    zerosteps = 500000,
                    lowlevel = True,
                    ),

    co_lift = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 162,
                    slope = -7.256,
                    zerosteps = 2935.18,
                    unit = 'mm',
                    lowlevel = True,
                    ),

    mli    = device('puma.liftmotor.LIFT_Axis',
                    motor = 'st_lift',
                    coder = 'co_lift',
                    obs = [],
                    obsreadings = 100,
                    precision = 0.15,
                    offset = 0,
                    maxtries = 10,
                    loopdelay = 1,
                    ),

    lift   = device('puma.lift.Lift',
                   moveable = 'mli',
                   states = ["top2", "top1", "ref", "bott"],
                   values = [357.9, 356.1, 0, -142.6],
                   sw_values = ['low', 0, 'ref', 'high'],
                   precision = 0.15,
                   unit = '',
                    ),

# Magazin
    st_mag = device('devices.vendor.ipc.Motor',
                    bus = 'motorbus7',
                    addr = 76,
                    slope = 200,
                    unit = 'deg',
                    abslimits = (20, 340),
                    zerosteps = 500000,
                    lowlevel = True,
                    ),

    co_mag = device('devices.vendor.ipc.Coder',
                    bus = 'motorbus1',
                    addr = 123,
                    slope = 181.97,
                    zerosteps = 2681.64,
                    unit = 'deg',
                    lowlevel = True,
                    ),

    mag    = device('devices.generic.Axis',
                    motor = 'st_mag',
                    coder = 'co_mag',
                    obs = [],
                    precision = 0.05,
                    offset = 0,
                    maxtries = 10,
                    dragerror = 90,
                    loopdelay = 2,
                    ),

    io_mag = device('devices.vendor.ipc.Input',
                   bus = 'motorbus8',
                   addr = 106,
                   first = 3,
                   last = 6,
                   unit = ''),

    magazin = device('puma.magazin.Magazin',
                   moveable = 'mag',
                   io_stat = 'io_mag',
                   states = ["A", "B", "C", "D"],
                   values = [315.4, 45.46, 135.4, 225.7],
                   io_values = [8, 1, 2, 4],
                   precision = 0.2,
                   unit = '',
                    ),

# Magnetic Lock

    mlock_op = device('devices.vendor.ipc.Input',
                   bus = 'motorbus8',
                   addr = 101,
                   first = 0,
                   last = 3,
                   unit = '',
                   ),

    mlock_cl = device('devices.vendor.ipc.Input',
                   bus = 'motorbus8',
                   addr = 101,
                   first = 5,
                   last = 8,
                   unit = '',
                   ),

    mlock_set = device('devices.vendor.ipc.Output',
                   bus = 'motorbus8',
                   addr = 110,
                   first = 0,
                   last = 3,
                   unit = '',
                   ),

    mlock   = device('puma.maglock.MagLock',
                   magazin = 'magazin',
                   io_open = 'mlock_op',
                   io_closed = 'mlock_cl',
                   io_set = 'mlock_set',
                   unit = '',
                   ),

)
