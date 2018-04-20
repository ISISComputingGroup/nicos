description = "neutronguide sideMirror noMirror"

group = 'lowlevel'

includes = ['nok_ref', 'nokbus3']
global_values = configdata('global.GLOBAL_Values')

nethost = 'refsanssrv.refsans.frm2'

devices = dict(
    nok7 = device('nicos_mlz.refsans.devices.nok_support.DoubleMotorNOK',
        description = 'NOK7',
        fmtstr = '%.2f, %.2f',
        nok_start = 7665.5,
        nok_length = 1190.0,
        nok_end = 8855.5,
        nok_gap = 1.0,
        inclinationlimits = (-100, 100),   # MP 04.12.2017 12:57:38 from ALT
        motor_r = 'nok7r_axis',
        motor_s = 'nok7s_axis',
        nok_motor = [7915.0, 8605.0],
        backlash = -2,   # is this configured somewhere?
        precision = 0.5,
        masks = {
            'ng': global_values['ng'],
            'rc': global_values['ng'],
            'vc': global_values['vc'],
            'fc': global_values['fc'],
        },
    ),
    nok7_mode = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'nok7 mode',
        device = 'nok7',
        parameter = 'mode',
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok7r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK7, reactor side',
        motor = 'nok7r_motor',
        coder = 'nok7r_motor',
        # obs = ['nok7r_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok7_srll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srll of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srll' % nethost,
        lowlevel = True,
    ),

    nok7_srhl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srhl of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srhl' % nethost,
        lowlevel = True,
    ),

    nok7_srref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srref of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srref' % nethost,
        lowlevel = True,
    ),

    nok7_srrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srrel of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srrel' % nethost,
        lowlevel = True,
    ),

    nok7_srsll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srsll of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srsll' % nethost,
        lowlevel = True,
    ),

    nok7_srshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/srshl of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/srshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok7r_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK7, reactor side',
        abslimits = (-437.6, 116.15),
        userlimits = (-89.475, 116.1),
        bus = 'nokbus3',     # from ipcsms_*.res
        addr = 0x52,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 62.4,   # from ipcsms_*.res
        zerosteps = int(687.6 * 800),    # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok7r_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok7r_motor',
         analog = 'nok7r_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok7r_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK7, reactor side',
        reference = 'nok_refc1',
        measure = 'nok7r_poti',
        poly = [17.162881, 1001.504 / 3.843],    # off, mul * 1000 / sensitivity, higher orders...
        serial = 7540,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    # generated from global/inf/poti_tracing.inf
    nok7r_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK7, reactor side',
        tacodevice = '//%s/test/wb_c/1_0' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok7s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK7, sample side',
        motor = 'nok7s_motor',
        coder = 'nok7s_motor',
        # obs = ['nok7s_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok7_ssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/ssll of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/ssll' % nethost,
        lowlevel = True,
    ),

    nok7_sshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/sshl of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/sshl' % nethost,
        lowlevel = True,
    ),

    nok7_ssref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/ssref of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/ssref' % nethost,
        lowlevel = True,
    ),

    nok7_ssrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/ssrel of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/ssrel' % nethost,
        lowlevel = True,
    ),

    nok7_sssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/sssll of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/sssll' % nethost,
        lowlevel = True,
    ),

    nok7_ssshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok7/ssshl of Server ipcsmsserver nok7',
        tacodevice = '//%s/test/nok7/ssshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok7s_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK7, sample side',
        abslimits = (-96.94, 125.56),
        userlimits = (-96.94, 125.55),
        bus = 'nokbus3',     # from ipcsms_*.res
        addr = 0x53,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 66.84,  # from ipcsms_*.res
        zerosteps = int(683.19 * 800),   # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok7s_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok7s_motor',
         analog = 'nok7s_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok7s_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK7, sample side',
        reference = 'nok_refc1',
        measure = 'nok7s_poti',
        poly = [24.5752, 1000.564 / 3.836],  # off, mul * 1000 / sensitivity, higher orders...
        serial = 7546,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    # generated from global/inf/poti_tracing.inf
    nok7s_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK7, sample side',
        tacodevice = '//%s/test/wb_c/1_1' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),
)
