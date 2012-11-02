description = 'IPC slit after mono shielding'

includes = ['system']

devices = dict(
    ss1bus    = device('devices.vendor.ipc.IPCModBusTCP',
                       host = 'moxa-mono.panda.frm2',
                       port = 4001,
                       lowlevel = True),

    ss1_l_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss1bus',
                       addr = 0x5C,
                       side = 2,
                       slope = -78.0,
                       zerosteps = 1900,
                       resetpos = -20,
                       abslimits = (-25, 20)),
    ss1_r_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss1bus',
                       addr = 0x5C,
                       side = 3,
                       slope = 82.0,
                       zerosteps = 1800,
                       resetpos = 20,
                       abslimits = (-20, 25)),
    ss1_b_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss1bus',
                       addr = 0x5C,
                       side = 0,
                       slope = -54.0,
                       zerosteps = 1200,
                       resetpos = -45,
                       abslimits = (-50, 20)),
    ss1_t_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss1bus',
                       addr = 0x5C,
                       side = 1,
                       slope = 56.0,
                       zerosteps = 1200,
                       resetpos = 45,
                       abslimits = (-20, 50)),

    ss1_l     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss1_l_mot',
                       coder = 'ss1_l_mot',
                       obs = None),
    ss1_r     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss1_r_mot',
                       coder = 'ss1_r_mot',
                       obs = None),
    ss1_b     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss1_b_mot',
                       coder = 'ss1_b_mot',
                       obs = None),
    ss1_t     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss1_t_mot',
                       coder = 'ss1_t_mot',
                       obs = None),

    ss1       = device('devices.generic.Slit',
                       description = 'sample slit 1',
                       left = 'ss1_l',
                       right = 'ss1_r',
                       bottom = 'ss1_b',
                       top = 'ss1_t',
                       opmode = '4blades',
                       pollinterval = 5,
                       maxage = 10),

    ss2bus    = device('devices.vendor.ipc.IPCModBusTCP',
                       host = 'moxa-ana.panda.frm2',
                       port = 4002,
                       lowlevel = True),

    ss2_l_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss2bus',
                       addr = 0x5C,
                       side = 2,
                       slope = -80,
                       zerosteps = 1840,
                       resetpos = -20,
                       abslimits = (-25, 20)),
    ss2_r_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss2bus',
                       addr = 0x5C,
                       side = 3,
                       slope = 80.,
                       zerosteps = 1800,
                       resetpos = 20,
                       abslimits = (-20, 25)),
    ss2_b_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss2bus',
                       addr = 0x5C,
                       side = 0,
                       slope = -54.,
                       zerosteps = 1170,
                       resetpos = -45,
                       abslimits = (-50, 20)),
    ss2_t_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ss2bus',
                       addr = 0x5C,
                       side = 1,
                       slope = 54.,
                       zerosteps = 1250,
                       resetpos = 45,
                       abslimits = (-20, 50)),

    ss2_l     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss2_l_mot',
                       coder = 'ss2_l_mot',
                       obs = None),
    ss2_r     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss2_r_mot',
                       coder = 'ss2_r_mot',
                       obs = None),
    ss2_b     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ss2_b_mot',
                       coder = 'ss2_b_mot',
                       obs = None),
    ss2_t     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ss2_t_mot',
                       coder = 'ss2_t_mot',
                       obs = None),

    ss2       = device('devices.generic.Slit',
                       description = 'sample slit 2',
                       left = 'ss2_l',
                       right = 'ss2_r',
                       bottom = 'ss2_b',
                       top = 'ss2_t',
                       opmode = '4blades',
                       pollinterval = 5,
                       maxage = 10),
)
