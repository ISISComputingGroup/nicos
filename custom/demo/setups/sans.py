description = 'virtual SANS devices'
group = 'basic'

sysconfig = dict(
    instrument = 'sans',
)

modules = ['sans1.commands']

excludes = ['tas']
includes = ['cryo']

devices = dict(
    Sample   = device('sans1.sans1_sample.Sans1Sample'),

    sans     = device('devices.instrument.Instrument',
                      responsible = 'R. Esponsible <r.esponsible@frm2.tum.de>',
                      instrument = 'SANS-V2'
                     ),

    guide_m1  = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 0.5,
                       unit = 'mm',
                      ),
    guide1    = device('devices.generic.Switcher',
                      lowlevel = True,
                      moveable = 'guide_m1',
                      mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                      precision = 0,
                      blockingmove = False,
                     ),
    guide_m2  = device('devices.generic.VirtualMotor',
                      lowlevel = True,
                      abslimits = (0, 10),
                      speed = 0.5,
                      unit = 'mm',
                     ),
    guide2    = device('devices.generic.Switcher',
                      lowlevel = True,
                      moveable = 'guide_m2',
                      mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                      precision = 0,
                      blockingmove = False,
                     ),
    guide_m3  = device('devices.generic.VirtualMotor',
                      lowlevel = True,
                      abslimits = (0, 10),
                      speed = 0.5,
                      unit = 'mm',
                     ),
    guide3    = device('devices.generic.Switcher',
                      lowlevel = True,
                      moveable = 'guide_m3',
                      mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                      precision = 0,
                      blockingmove = False,
                     ),
    guide_m4  = device('devices.generic.VirtualMotor',
                      lowlevel = True,
                      abslimits = (0, 10),
                      speed = 0.5,
                      unit = 'mm',
                     ),
    guide4    = device('devices.generic.Switcher',
                      lowlevel = True,
                      moveable = 'guide_m4',
                      mapping = {'off': 0, 'ng': 3, 'P3': 6, 'P4': 9},
                      precision = 0,
                      blockingmove = False,
                     ),
    guide    = device('devices.generic.MultiSwitcher',
                      moveables = ['guide1', 'guide2', 'guide3', 'guide4'],
                      mapping = {'off': ['off', 'off', 'off', 'off'],
                                 '1m':  ['off', 'off', 'off', 'ng' ],
                                 '2m':  ['off', 'off', 'ng',  'ng' ],
                                 '4m':  ['off', 'ng',  'ng',  'ng' ],
                                 '6m':  ['ng',  'ng',  'ng',  'ng' ],
                                 'P3':  ['P3',  'P3',  'P3',  'P3' ],
                                 'P4':  ['P4',  'P4',  'P4',  'P4' ],
                                 },
                      precision = [None,],
                     ),

    coll_m    = device('devices.generic.VirtualMotor',
                       lowlevel = True,
                       abslimits = (0, 10),
                       speed = 1,
                       unit = 'deg',
                      ),
    coll      = device('devices.generic.Switcher',
                       description = 'collimation',
                       moveable = 'coll_m',
                       mapping = {'off': 0,
                                  '10m': 2,
                                  '15m': 4,
                                  '20m': 8},
                       precision = 0,
                      ),

    det_pos1  = device('devices.generic.VirtualMotor',
                      description = 'detector1 position in the tube',
                      abslimits = (0, 21),
                      speed = 1,
                      unit = 'm',
                      curvalue = 1,
                     ),

    det_pos1_x  = device('devices.generic.VirtualMotor',
                      description = 'horizontal offset of detector inside tube',
                      abslimits = (-1, 5),
                      speed = 0.5,
                      unit = 'm',
                      curvalue = 0,
                     ),

    det_pos1_tilt  = device('devices.generic.VirtualMotor',
                      description = 'tilt of detector',
                      abslimits = (-40, 40),
                      speed = 0.5,
                      unit = 'deg',
                      curvalue = 0,
                     ),

    det_pos2  = device('devices.generic.VirtualMotor',
                      description = 'detector2 position in the tube',
                      abslimits = (1, 22),
                      speed = 0.5,
                      unit = 'm',
                      curvalue = 10,
                     ),

    det      = device('devices.generic.virtual.Virtual2DDetector',
                      distance = 'det_pos1',
                      collimation = 'guide',
                      subdir = '2ddata',
                     ),

    det_HV   = device('devices.generic.VirtualMotor',
                      description = 'high voltage at the detector',
                      requires = {'level': 'admin'},
                      abslimits = (0, 1000),
                      warnlimits = (990, 1010),
                      unit = 'V',
                      curvalue = 1000,
                      speed = 10,
                     ),
    SampleChanger = device('devices.generic.ManualSwitch',
                           description = 'Virtual Samplechanger with 11 positions',
                           states = range(1, 11),
                           fmtstr = '%d',
                           ),
)

startupcode = '''
SetDetectors(det)
printinfo("============================================================")
printinfo("Welcome to the NICOS SANS demo setup.")
printinfo("Run count(1) to collect an image.")
printinfo("============================================================")
'''
