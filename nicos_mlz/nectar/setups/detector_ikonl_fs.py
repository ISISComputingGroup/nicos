# -*- coding: utf-8 -*-

description = 'Andor IKON-L CCD camera'

group = 'optional'

includes = ['filesavers']
excludes = ['detector', 'detector_ikonl']

tango_base = 'tango://nectarccd01.nectar.frm2:10000/nectar/'
nethost = 'nectarsrv.nectar.frm2'  # taco

devices = dict(
    timer = device('nicos.devices.vendor.lima.LimaCCDTimer',
        description = 'The camera\'s internal timer',
        tangodevice = tango_base + 'detector/limaccd',
    ),
    det = device('nicos.devices.generic.Detector',
        description = 'The Andor Neo sCMOS camera detector',
        images = ['ccd'],
        timers = ['timer'],
    ),
    ccd = device('nicos_mlz.antares.devices.detector.AntaresIkonLCCD',
        description = 'The CCD detector',
        tangodevice = tango_base + 'detector/limaccd',
        hwdevice = tango_base + 'detector/ikonl',
        pollinterval = 5,
        maxage = 12,
        flip = (False, False),
        rotation = 0,
        shutteropentime = 0.05,
        shutterclosetime = 0.05,
        shuttermode = 'auto',
        vsspeed = 16.0,
        hsspeed = 1,
        pgain = 1,
        fastshutter = 'fastshutter',
    ),
    ccdTemp = device('nicos.devices.vendor.lima.Andor2TemperatureController',
        description = 'Temperature of the CCD detector',
        tangodevice = tango_base + 'detector/ikonl',
        pollinterval = 5,
        maxage = 12,
        abslimits = (-100, 0),
        userlimits = (-100, 0),
        unit = 'degC',
        precision = 3,
        fmtstr = '%.0f',
    ),
    fov_mot = device('nicos.devices.taco.Motor',
        description = 'Camera translation x (field of view)',
        tacodevice = '//%s/nectar/cam/fov' % nethost,
        abslimits = (0, 900),
        comtries = 3,
        # prefersetup = True,
        lowlevel = True,
    ),
    fov    = device('nicos.devices.generic.Axis',
        description = 'Camera traslation x (field of view)',
        pollinterval = 5,
        maxage = 12,
        fmtstr = '%.2f',
        userlimits = (0.0001, 900),
        precision = 0.1,
        motor = 'fov_mot',
        coder = 'fov_mot',
        obs=[],
    ),
    focus_mot = device('nicos.devices.taco.Motor',
        description = 'Camera lens roation axis (focus)',
        tacodevice = '//%s/nectar/cam/focus' % nethost,
        abslimits = (-100, 100),
        comtries = 3,
        lowlevel = True,
    ),
    focus = device('nicos.devices.generic.Axis',
        description = 'Camera lens roation axis (focus)',
        pollinterval = 5,
        maxage = 12,
        fmtstr = '%.2f',
        userlimits = (-100, 100),
        precision = 0.1,
        motor = 'focus_mot',
        coder = 'focus_mot',
        obs=[],
    ),
)

startupcode = '''
SetDetectors(det)

## override hw setting to known good values.
ccd.rotation = 0
ccd.shutteropentime = 0.05
ccd.shutterclosetime = 0.05
ccd.shuttermode = 'auto'
ccd.vsspeed = 38.55
ccd.hsspeed = 1
ccd.pgain = 1
'''
