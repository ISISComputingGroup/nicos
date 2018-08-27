#  -*- coding: utf-8 -*-

description = 'setup for the velocity selector'
group = 'lowlevel'

tango_base = 'tango://resedahw2.reseda.frm2:10000/reseda/selector'

devices = dict(
    selector_speed_fake = device('nicos.devices.generic.virtual.VirtualMotor',
        description = 'Selector fake speed for testing',
        abslimits = (0, 28500),
        precision = 10,
        unit = 'rpm',
    ),
   # selector_tilt_fake = device('nicos.devices.generic.virtual.VirtualMotor',
   #     description = 'Selector fake tilt for testing',
   #     abslimits = (-10, 10),
   #     precision = 0.1,
   #     unit = 'deg',
   # ),
   # selector_speed = device('nicos.devices.tango.WindowTimeoutAO',
   #     description = 'Selector speed control',
   #     tangodevice = tango_base + '/speed',
   #     unit = 'rpm',
   #     fmtstr = '%.0f',
   #     warnlimits = (8500, 28500),
   #     abslimits = (0, 28500),
   #     precision = 10,
   # ),
    selector_lambda = device('nicos_mlz.reseda.devices.astrium.SelectorLambda',
        description = 'Selector wavelength control',
        seldev = 'selector_speed_fake',
        tiltdev = 'selcradle',
        unit = 'A',
        fmtstr = '%.2f',
        # twistangle = 19.724,
        twistangle = 48.27,
        length = 0.25,
        radius = 0.16,
        beamcenter = 0.115,
        maxspeed = 28500,
    ),
    selector_rtemp = device('nicos.devices.tango.AnalogInput',
        description = 'Temperature of the selector rotor',
        tangodevice = tango_base + '/rotortemp',
        unit = 'degC',
        fmtstr = '%.1f',
        warnlimits = (10, 45),
    ),
    selector_winlt = device('nicos.devices.tango.AnalogInput',
        description = 'Cooling water temperature at inlet',
        tangodevice = tango_base + '/waterintemp',
        unit = 'degC',
        fmtstr = '%.1f',
        warnlimits = (15, 20),
    ),
    selector_woutt = device('nicos.devices.tango.AnalogInput',
        description = 'Cooling water temperature at outlet',
        tangodevice = tango_base + '/waterouttemp',
        unit = 'degC',
        fmtstr = '%.1f',
        warnlimits = (15, 20),
    ),
    selector_wflow = device('nicos.devices.tango.AnalogInput',
        description = 'Cooling water flow rate through selector',
        tangodevice = tango_base + '/flowrate',
        unit = 'l/min',
        fmtstr = '%.1f',
        warnlimits = (1.5, 10),
    ),
    selector_vacuum = device('nicos.devices.tango.AnalogInput',
        description = 'Vacuum in the selector',
        tangodevice = tango_base + '/vacuum',
        unit = 'mbar',
        fmtstr = '%.5f',
        warnlimits = (0, 0.005),
    ),
    selector_vibrt = device('nicos.devices.tango.AnalogInput',
        description = 'Selector vibration',
        tangodevice = tango_base + '/vibration',
        unit = 'mm/s',
        fmtstr = '%.2f',
        warnlimits = (0, 1),
    ),
    selcradle_mot = device('nicos.devices.tango.Motor',
        description = 'Detector rotation (motor)',
        tangodevice = '%s/selcradle' % tango_base,
        fmtstr = '%.3f',
        unit = 'deg',
        lowlevel = True,
    ),
    selcradle_enc = device('nicos.devices.tango.Sensor',
        description = 'Detector rotation (encoder)',
        tangodevice = '%s/encoder' % tango_base,
        fmtstr = '%.3f',
        unit = 'deg',
        lowlevel = True,
    ),
    selcradle = device('nicos.devices.generic.Axis',
        description = 'Detector rotation',
        motor = 'selcradle_mot',
        coder = 'selcradle_enc',
        fmtstr = '%.3f',
        precision = 0.1,
    ),
)
