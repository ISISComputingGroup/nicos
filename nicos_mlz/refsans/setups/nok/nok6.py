description = "neutronguide sideMirror noMirror"

group = 'lowlevel'

includes = ['nok_ref', 'nokbus2', 'nokbus3']

nethost = 'refsanssrv.refsans.frm2'
global_values = configdata('global.GLOBAL_Values')

devices = dict(
    nok6 = device('nicos_mlz.refsans.devices.nok_support.DoubleMotorNOK',
        description = 'NOK6',
        fmtstr = '%.2f, %.2f',
        nok_start = 5887.5,
        nok_length = 1720.0,
        nok_end = 7607.5,
        nok_gap = 1.0,
        inclinationlimits = (-100, 100),   # MP 04.12.2017 12:57:22  from ALT
        motor_r = 'nok6r_axis',
        motor_s = 'nok6s_axis',
        nok_motor = [6137.0, 7357.0],
        backlash = -2,   # is this configured somewhere?
        precision = 0.5,
        masks = {
            'ng': global_values['ng'],
            'rc': global_values['ng'],
            'vc': global_values['vc'],
            'fc': global_values['fc'],
        },
    ),
    nok6_mode = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'nok6 mode',
        device = 'nok6',
        parameter = 'mode',
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok6r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK6, reactor side',
        motor = 'nok6r_motor',
        coder = 'nok6r_motor',
        # obs = ['nok6r_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok6_srll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srll of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srll' % nethost,
        lowlevel = True,
    ),

    nok6_srhl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srhl of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srhl' % nethost,
        lowlevel = True,
    ),

    nok6_srref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srref of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srref' % nethost,
        lowlevel = True,
    ),

    nok6_srrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srrel of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srrel' % nethost,
        lowlevel = True,
    ),

    nok6_srsll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srsll of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srsll' % nethost,
        lowlevel = True,
    ),

    nok6_srshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/srshl of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/srshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok6r_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK6, reactor side',
        abslimits = (-704.6375, 545.36125),
        userlimits = (-66.2, 96.59125),
        bus = 'nokbus2',     # from ipcsms_*.res
        addr = 0x46,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 45.51,  # from ipcsms_*.res
        zerosteps = int(704.638 * 800),  # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok6r_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok6r_motor',
         analog = 'nok6r_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok6r_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK6, reactor side',
        reference = 'nok_refb2',
        measure = 'nok6r_poti',
        poly = [3.823914, 997.832 / 3.846],  # off, mul * 1000 / sensitivity, higher orders...
        serial = 7538,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    # generated from global/inf/poti_tracing.inf
    nok6r_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK6, reactor side',
        tacodevice = '//%s/test/wb_b/2_1' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok6s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK6, sample side',
        motor = 'nok6s_motor',
        coder = 'nok6s_motor',
        # obs = ['nok6s_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok6_ssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/ssll of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/ssll' % nethost,
        lowlevel = True,
    ),

    nok6_sshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/sshl of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/sshl' % nethost,
        lowlevel = True,
    ),

    nok6_ssref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/ssref of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/ssref' % nethost,
        lowlevel = True,
    ),

    nok6_ssrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/ssrel of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/ssrel' % nethost,
        lowlevel = True,
    ),

    nok6_sssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/sssll of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/sssll' % nethost,
        lowlevel = True,
    ),

    nok6_ssshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok6/ssshl of Server ipcsmsserver nok6',
        tacodevice = '//%s/test/nok6/ssshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok6s_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK6, sample side',
        abslimits = (-703.5, 546.49875),
        userlimits = (-81.0, 110.875),
        bus = 'nokbus3',     # from ipcsms_*.res
        addr = 0x51,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 10,
        accel = 10,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 46.67,  # from ipcsms_*.res
        zerosteps = int(703.5 * 800),    # offset * slope
        lowlevel = global_values['hide_poti'],
    ),

    nok6s_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok6s_motor',
         analog = 'nok6s_obs',
         lowlevel = global_values['hide_acc'],
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok6s_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK6, sample side',
        reference = 'nok_refb2',
        measure = 'nok6s_poti',
        poly = [16.273013, 999.674 / 3.834],     # off, mul * 1000 / sensitivity, higher orders...
        serial = 7537,
        length = 250.0,
        lowlevel = global_values['hide_poti'],
    ),

    # generated from global/inf/poti_tracing.inf
    nok6s_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK6, sample side',
        tacodevice = '//%s/test/wb_b/2_2' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),
)
