description = 'Virtual TOF instrument'

group = 'basic'

includes = ['source']

excludes = ['misc']

sysconfig = dict(
    datasinks = ['conssink', 'serialsink', 'livesink', 'dmnsink',
                 'tofsink',
                ],
)

devices = dict(
    monitor = device('nicos.devices.generic.VirtualCounter',
                     description = 'TOFTOF monitor',
                     fmtstr = '%d',
                     type = 'monitor',
                     lowlevel = True,
                    ),
    timer = device('nicos.devices.generic.VirtualTimer',
                   description = 'TOFTOF timer',
                   fmtstr = '%.2f',
                   unit = 's',
                   lowlevel = True,
                  ),
    image = device('nicos_mlz.toftof.devices.virtual.VirtualImage',
                   description = 'Image data device',
                   fmtstr = '%d',
                   pollinterval = 86400,
                   lowlevel = True,
                   datafile = 'nicos_mlz/toftof/data/test/data.npz',
                  ),
    det = device('nicos_mlz.toftof.devices.detector.Detector',
                 description = 'The TOFTOF detector device',
                 timers = ['timer'],
                 monitors = ['monitor'],
                 counters = [],
                 images = ['image'],
                 rc = 'rc',
                 chopper = 'ch',
                 chdelay = 'chdelay',
                 maxage = 3,
                 pollinterval = 0.5,
                 liveinterval = 10.0,
                 saveintervals = [30.],
                 detinfofile = 'nicos_mlz/toftof/detinfo.dat',
                 # fileformats = ['tofdatasaver'],
                 # subdir = 'toftof',
                 # numinputs = 1024,
                ),
    d1 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 1',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d2 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 2',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d3 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 3',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d4 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 4',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d5 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 5',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d6 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 6',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    d7 = device('nicos_mlz.toftof.devices.chopper.Disc',
                description = 'Chopper disc 7',
                fmtstr = '%.0f',
                speed = 100,
                jitter = 2,
                lowlevel = True,
               ),
    ch = device('nicos_mlz.toftof.devices.chopper.VirtualController',
                description = 'TOFTOF chopper control device',
                speed_accuracy = 40,
                phase_accuracy = 10,
                ch5_90deg_offset = 0,
                timeout = 600,
                pollinterval = 10,
                maxage = 12,
                unit = 'rpm',
                discs = ['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7'],
                fmtstr = "%.1f",
                # abslimits = (0., 27000),
                lowlevel = False,
               ),
    chSpeed = device('nicos_mlz.toftof.devices.chopper.Speed',
                     description = 'Setpoint of the chopper speed',
                     chopper = 'ch',
                     chdelay = 'chdelay',
                     abslimits = (0, 22000.),
                     pollinterval = 10,
                     maxage = 12,
                     fmtstr = '%.0f',
                     unit = 'rpm',
                    ),
    chDS = device('nicos_mlz.toftof.devices.chopper.SpeedReadout',
                  description = 'Speed of the disks 1 - 7',
                  chopper = 'ch',
                  fmtstr = '[%.0f, %.0f, %.0f, %.0f, %.0f, %.0f, %.0f]',
                  pollinterval = 10,
                  maxage = 12,
                  unit = 'rpm',
                 ),
    chWL = device('nicos_mlz.toftof.devices.chopper.Wavelength',
                  description = 'Neutron wavelength',
                  chopper = 'ch',
                  chdelay = 'chdelay',
                  abslimits = (0.2, 16.0),
                  pollinterval = 10,
                  maxage = 12,
                  unit = 'AA',
                 ),
    chRatio = device('nicos_mlz.toftof.devices.chopper.Ratio',
                     description = 'Frame overlap ratio',
                     chopper = 'ch',
                     chdelay = 'chdelay',
                     pollinterval = 10,
                     maxage = 12,
                    ),
    chCRC = device('nicos_mlz.toftof.devices.chopper.CRC',
                   description = 'Chopper rotation sense (CRC=1, '
                                 'parallel=0)',
                   requires = {'level': 'admin'},
                   chopper = 'ch',
                   chdelay = 'chdelay',
                   pollinterval = 10,
                   maxage = 12,
                  ),
    chST = device('nicos_mlz.toftof.devices.chopper.SlitType',
                  description = 'Chopper window; large window=0',
                  requires = {'level': 'admin'},
                  chopper = 'ch',
                  chdelay = 'chdelay',
                  pollinterval = 10,
                  maxage = 12,
                 ),
    chdelay = device('nicos.devices.generic.ManualMove',
                     description = 'Trigger time-offset',
                     requires = {'level': 'guest'},
                     abslimits = (0, 1000000),
                     unit = 'usec',
                     fmtstr = '%d',
                    ),
    gx    = device('nicos.devices.generic.VirtualMotor',
                   description = 'X translation of the sample table',
                   fmtstr = "%7.3f",
                   abslimits = (-20.0, 20.),
                   unit = 'mm',
                  ),
    gy    = device('nicos.devices.generic.VirtualMotor',
                   description = 'Y translation of the sample table',
                   fmtstr = "%7.3f",
                   abslimits = (-20.0, 20.),
                   unit = 'mm',
                  ),
    gz    = device('nicos.devices.generic.VirtualMotor',
                   description = 'Z translation of the sample table',
                   fmtstr = "%7.3f",
                   abslimits = (-14.8, 50.),
                   unit = 'mm',
                  ),
    gcx   = device('nicos.devices.generic.VirtualMotor',
                   description = 'Chi rotation of the sample goniometer',
                   fmtstr = "%7.3f",
                   abslimits = (-20.0, 20.),
                   unit = 'deg',
                  ),
    gcy   = device('nicos.devices.generic.VirtualMotor',
                   description = 'Psi rotation of the sample goniometer',
                   fmtstr = "%7.3f",
                   abslimits = (-20.0, 20.),
                   unit = 'deg',
                  ),
    gphi  = device('nicos.devices.generic.VirtualMotor',
                   description = 'Phi rotation of the sample table',
                   fmtstr = "%7.3f",
                   abslimits = (-20.0, 150.),
                   unit = 'deg',
                  ),

    SampleSlitMotVB = device('nicos.devices.generic.VirtualMotor',
                             lowlevel = True,
                             abslimits = (-200, 46.425),
                             fmtstr = "%7.3f",
                             unit = 'mm',
                            ),
    SampleSlitMotVT = device('nicos.devices.generic.VirtualMotor',
                             lowlevel = True,
                             abslimits = (-200, 46.425),
                             fmtstr = "%7.3f",
                             unit = 'mm',
                            ),
    SampleSlitMotHL = device('nicos.devices.generic.VirtualMotor',
                             lowlevel = True,
                             abslimits = (-200, 27.5),
                             fmtstr = "%7.3f",
                             unit = 'mm',
                            ),
    SampleSlitMotHR = device('nicos.devices.generic.VirtualMotor',
                             lowlevel = True,
                             abslimits = (-200, 27.5),
                             fmtstr = "%7.3f",
                             unit = 'mm',
                            ),
    slit = device('nicos.devices.generic.Slit',
                  description = 'Sample entry slit',
                  bottom = 'SampleSlitMotVB',
                  top = 'SampleSlitMotVT',
                  left = 'SampleSlitMotHL',
                  right = 'SampleSlitMotHR',
                  coordinates = 'opposite',
                  opmode = 'offcentered',
                 ),

    hv0   = device('nicos.devices.generic.VirtualMotor',
                   description = 'ISEG HV power supply 1',
                   requires = {'level': 'admin'},
                   abslimits = (0, 1600),
                   ramp = 120,
                   unit = 'V',
                  ),
    hv1   = device('nicos.devices.generic.VirtualMotor',
                   description = 'ISEG HV power supply 2',
                   requires = {'level': 'admin'},
                   abslimits = (0, 1600),
                   ramp = 120,
                   unit = 'V',
                  ),
    hv2   = device('nicos.devices.generic.VirtualMotor',
                   description = 'ISEG HV power supply 3',
                   requires = {'level': 'admin'},
                   abslimits = (0, 1600),
                   ramp = 120,
                   unit = 'V',
                  ),

    lv0   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 1',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv1   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 2',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv2   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 3',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv3   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 4',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv4   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 5',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv5   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 6',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv6   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 7',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),
    lv7   = device('nicos.devices.generic.ManualSwitch',
                   description = 'LV power supply 8',
                   requires = {'level': 'admin'},
                   pollinterval = 10,
                   maxage = 12,
                   states = ['off', 'on']
                  ),

    vac0   = device('nicos.devices.generic.ManualMove',
                    description = 'Vacuum sensor in chopper vessel 1',
                    default = 1.7e-6,
                    abslimits = (0, 1000),
                    pollinterval = 10,
                    maxage = 12,
                    unit = 'mbar',
                   ),
    vac1   = device('nicos.devices.generic.ManualMove',
                    description = 'Vacuum sensor in chopper vessel 2',
                    default = 0.00012,
                    abslimits = (0, 1000),
                    pollinterval = 10,
                    maxage = 12,
                    unit = 'mbar',
                   ),
    vac2   = device('nicos.devices.generic.ManualMove',
                    description = 'Vacuum sensor in chopper vessel 3',
                    default = 3.5e-6,
                    abslimits = (0, 1000),
                    pollinterval = 10,
                    maxage = 12,
                    unit = 'mbar',
                   ),
    vac3   = device('nicos.devices.generic.ManualMove',
                    description = 'Vacuum sensor in chopper vessel 4',
                    default = 5.0e-6,
                    abslimits = (0, 1000),
                    pollinterval = 10,
                    maxage = 12,
                    unit = 'mbar',
                   ),
    ngc_motor = device('nicos.devices.generic.VirtualMotor',
                       description = 'The motor for the neutron guide'
                                     ' changing mechnism',
                       fmtstr = "%7.2f",
                       userlimits = (-131.4, 0.),
                       abslimits = (-131.4, 0.),
                       unit = 'mm',
                       lowlevel = True,
                      ),
    ngc = device('nicos_mlz.toftof.devices.neutronguide.Switcher',
                 description = 'The neutron guide changer/collimator',
                 moveable = 'ngc_motor',
                 mapping = {'linear': -5.1, 'focus': -131.25,},
                 # requires = {'level': 'admin'},
                ),
    rc = device('nicos.devices.generic.ManualSwitch',
                description = 'Radial collimator',
                states = ['off', 'on'],
                requires = {'level': 'admin'},
                pollinterval = 10,
                maxage = 12,
               ),
    tofsink = device('nicos_mlz.toftof.devices.datasinks.TofImageSink',
                     filenametemplate = ['%(pointcounter)08d_0000.raw'],
                     lowlevel = True,
                    ),
)

startupcode = '''
SetDetectors(det)
SetEnvironment(ReactorPower)
# AddEnvironment(chDS)
'''