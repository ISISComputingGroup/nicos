description = "neutronguide, radialcollimator"

group = 'lowlevel'

includes = ['nok_ref', 'nokbus1']
global_values = configdata('global.GLOBAL_Values')

nethost = 'refsanssrv.refsans.frm2'
tango_host = 'tango://refsanshw:10000/test/'

devices = dict(
    nok3 = device('nicos_mlz.refsans.devices.nok_support.DoubleMotorNOK',
        description = 'NOK3',
        fmtstr = '%.2f, %.2f',
        nok_start = 680.0,
        nok_length = 600.0,
        nok_end = 1280.0,
        nok_gap = 1.0,
        inclinationlimits = (-100, 100),   # MP 04.12.2017 12:56:11 from ALT
        motor_r = 'nok3r_axis',
        motor_s = 'nok3s_axis',
        nok_motor = [831.0, 1131.0],
        backlash = -2,   # is this configured somewhere?
        precision = 0.5,
        masks = {
            'ng': global_values['ng'],
            'rc': global_values['rc'],
            'vc': global_values['ng'],
            'fc': global_values['ng'],
        },
    ),
    nok3_mode = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'nok3 mode',
        device = 'nok3',
        parameter = 'mode',
    ),

    nok3r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK3, reactor side',
        motor = 'nok3r_motor',
        coder = 'nok3r_motor',
        # obs = ['nok3r_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok3_srref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srref of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srref' % nethost,
        lowlevel = True,
    ),

    nok3_srrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srrel of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srrel' % nethost,
        lowlevel = True,
    ),

    nok3_srsll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srsll of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srsll' % nethost,
        lowlevel = True,
    ),

    nok3_srshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srshl of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srshl' % nethost,
        lowlevel = True,
    ),

    nok3_srll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srll of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srll' % nethost,
        lowlevel = True,
    ),

    nok3_srhl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/srhl of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/srhl' % nethost,
        lowlevel = True,
    ),

    nok3r_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK3, reactor side',
        abslimits = (-21.967, 47.783),
        bus = 'nokbus1',     # from ipcsms_*.res
        addr = 0x34,     # from resources.inf
        slope = 2000.0,  # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 20.6225,    # from ipcsms_*.res
        zerosteps = int(229.467 * 2000),     # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok3r_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok3r_motor',
         analog = 'nok3r_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    nok3r_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK3, reactor side',
        reference = 'nok_refa1',
        measure = 'nok3r_poti',
        poly = [21.830175, 997.962 / 3.846],     # off, mul * 1000 / sensitivity, higher orders...
        serial = 6507,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    nok3r_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK3, reactor side',
        tangodevice = tango_host + 'wb_a/1_3',
        scale = 1,   # mounted from bottom
        lowlevel = True,
    ),

    nok3s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK3, sample side',
        motor = 'nok3s_motor',
        coder = 'nok3s_motor',
        # obs = ['nok3s_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok3_ssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/ssll of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/ssll' % nethost,
        lowlevel = True,
    ),

    nok3_sshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/sshl of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/sshl' % nethost,
        lowlevel = True,
    ),

    nok3_ssref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/ssref of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/ssref' % nethost,
        lowlevel = True,
    ),

    nok3_ssrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/ssrel of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/ssrel' % nethost,
        lowlevel = True,
    ),

    nok3_sssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/sssll of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/sssll' % nethost,
        lowlevel = True,
    ),

    nok3_ssshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok3/ssshl of Server ipcsmsserver nok3',
        tacodevice = '//%s/test/nok3/ssshl' % nethost,
        lowlevel = True,
    ),

    nok3s_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK3, sample side',
        abslimits = (-20.9435, 40.8065),
        bus = 'nokbus1',     # from ipcsms_*.res
        addr = 0x35,     # from resources.inf
        slope = 2000.0,  # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 9.444,  # from ipcsms_*.res
        zerosteps = int(240.694 * 2000),     # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok3s_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok3s_motor',
         analog = 'nok3s_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    nok3s_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK3, sample side',
        reference = 'nok_refa1',
        measure = 'nok3s_poti',
        poly = [10.409698, 1003.196 / 3.854],    # off, mul * 1000 / sensitivity, higher orders...
        serial = 6506,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    nok3s_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK3, sample side',
        tangodevice = tango_host + 'wb_a/1_4',
        scale = 1,   # mounted from bottom
        lowlevel = True,
    ),
)
