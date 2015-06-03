description = 'IPC slit inside mono1 shielding'
group = 'lowlevel'

devices = dict(
    ms1bus    = device('devices.vendor.ipc.IPCModBusTango',
                       tangodevice = 'tango://mira1.mira.frm2:10000/mira/ms1/bio',
                       lowlevel = True,
                      ),

    ms1_l_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms1bus',
                       addr = 0x55,
                       side = 2,
                       slope = -80,
                       zerosteps = 1170,
                       resetpos = -20,
                       abslimits = (-32, 13),
                      ),
    ms1_r_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms1bus',
                       addr = 0x55,
                       side = 3,
                       slope = 80.,
                       zerosteps = 1800,
                       resetpos = 20,
                       abslimits = (-13, 32),
                      ),
    ms1_b_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms1bus',
                       addr = 0x55,
                       side = 0,
                       slope = -40.,
                       zerosteps = 720,
                       resetpos = -45,
                       abslimits = (-70, 17),
                      ),
    ms1_t_mot = device('devices.vendor.ipc.SlitMotor',
                       lowlevel = True,
                       bus = 'ms1bus',
                       addr = 0x55,
                       side = 1,
                       slope = 40.,
                       zerosteps = 790,
                       resetpos = 45,
                       abslimits = (-19, 70),
                      ),

    ms1_l     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ms1_l_mot',
                       coder = 'ms1_l_mot',
                       obs = None,
                      ),
    ms1_r     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ms1_r_mot',
                       coder = 'ms1_r_mot',
                       obs = None,
                      ),
    ms1_b     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = -2.,
                       motor = 'ms1_b_mot',
                       coder = 'ms1_b_mot',
                       obs = None,
                      ),
    ms1_t     = device('devices.generic.Axis',
                       lowlevel = True,
                       precision = 0.1,
                       backlash = 2.,
                       motor = 'ms1_t_mot',
                       coder = 'ms1_t_mot',
                       obs = None,
                      ),

    ms1       = device('devices.generic.Slit',
                       description = 'slit after monochromator Mira1',
                       left = 'ms1_l',
                       right = 'ms1_r',
                       bottom = 'ms1_b',
                       top = 'ms1_t',
                       opmode = 'offcentered',
                       pollinterval = 5,
                       maxage = 10,
                      ),
)
