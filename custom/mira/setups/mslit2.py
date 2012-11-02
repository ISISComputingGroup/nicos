description = 'IPC slit after mono2 shielding'
group = 'optional'



devices = dict(
    ms2bus    = device('devices.vendor.ipc.IPCModBusTacoSerial',
                       tacodevice = 'mira/network/rs8_4',
                       lowlevel = True),

    # NOTE: this slit is mounted upside-down -- therefore the
    # left/right/top/bottom axis sides are switched

    ms2_l_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms2bus',
                       addr = 0x88,
                       side = 3,
                       slope = -80.,
                       zerosteps = 1150,
                       resetpos = -20,
                       abslimits = (-32, 13)),
    ms2_r_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms2bus',
                       addr = 0x88,
                       side = 2,
                       slope = 80.,
                       zerosteps = 1170,
                       resetpos = 20,
                       abslimits = (-13, 32)),
    ms2_b_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms2bus',
                       addr = 0x88,
                       side = 1,
                       slope = -40.,
                       zerosteps = 780,
                       resetpos = -45,
                       abslimits = (-70, 19)),
    ms2_t_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms2bus',
                       addr = 0x88,
                       side = 0,
                       slope = 40.,
                       zerosteps = 770,
                       resetpos = 45,
                       abslimits = (-17, 70)),

    ms2_l     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ms2_l_mot',
                       coder = 'ms2_l_mot',
                       obs = None),
    ms2_r     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ms2_r_mot',
                       coder = 'ms2_r_mot',
                       obs = None),
    ms2_b     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ms2_b_mot',
                       coder = 'ms2_b_mot',
                       obs = None),
    ms2_t     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ms2_t_mot',
                       coder = 'ms2_t_mot',
                       obs = None),

    ms2       = device('devices.generic.Slit',
                       description = 'slit after monochromator Mira2',
                       left = 'ms2_l',
                       right = 'ms2_r',
                       bottom = 'ms2_b',
                       top = 'ms2_t',
                       opmode = 'offcentered',
                       pollinterval = 5,
                       maxage = 10),
)
