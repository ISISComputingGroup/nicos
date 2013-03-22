description = 'virtual SANS devices'
group = 'basic'

sysconfig = dict(
    instrument = 'sans',
)

excludes = ['tas']
includes = ['cryo']

devices = dict(
    sans     = device('devices.instrument.Instrument',
                      instrument = 'SANS-V'
                     ),

    guide_m  = device('devices.generic.VirtualMotor',
                      lowlevel = True,
                      abslimits = (0, 10),
                      speed = 0.5,
                      unit = 'mm',
                     ),
    guide    = device('devices.generic.Switcher',
                      moveable = 'guide_m',
                      states = ['guide', 'pol', 'nothing'],
                      values = [0, 5, 10],
                      precision = 0,
                     ),

    coll_m   = device('devices.generic.VirtualMotor',
                      lowlevel = True,
                      abslimits = (0, 10),
                      speed = 1,
                      unit = 'deg',
                     ),
    coll     = device('devices.generic.Switcher',
                      description = 'collimation',
                      moveable = 'coll_m',
                      states = ['10m', '15m', '20m'],
                      values = [0, 5, 10],
                      precision = 0,
                     ),

    det_pos  = device('devices.generic.VirtualMotor',
                      description = 'detector position in the tube',
                      abslimits = (1, 50),
                      speed = 0.5,
                      unit = 'm',
                      initval = 1,
                     ),

    det      = device('devices.generic.virtual.Virtual2DDetector',
                      distance = 'det_pos',
                      collimation = 'coll',
                      subdir = '2ddata',
                     ),

    det_HV   = device('devices.generic.VirtualMotor',
                      description = 'high voltage at the detector',
                      requires = {'level': 'admin'},
                      abslimits = (0, 1000),
                      unit = 'V',
                      initval = 1000,
                      speed = 10,
                     ),
)

startupcode = '''
SetMode('master')
SetDetectors(det)
printinfo("============================================================")
printinfo("Welcome to the NICOS SANS demo setup.")
printinfo("Run count(1) to collect an image.")
printinfo("============================================================")
'''
