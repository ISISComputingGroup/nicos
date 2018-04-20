description = "neutronguide sideMirror noMirror"

group = 'lowlevel'

includes = ['nok_ref', 'nokbus3', 'nokbus4']
global_values = configdata('global.GLOBAL_Values')

nethost = 'refsanssrv.refsans.frm2'

devices = dict(
    nok9 = device('nicos_mlz.refsans.devices.nok_support.DoubleMotorNOK',
        description = 'NOK9',
        nok_start = 9773.5,
        fmtstr = '%.2f, %.2f',
        nok_length = 840.0,
        nok_end = 10613.5,
        nok_gap = 1.0,
        inclinationlimits = (-100, 100),   # MP 04.12.2017 12:58:13 from ALT
        motor_r = 'nok9r_axis',
        motor_s = 'nok9s_axis',
        nok_motor = [10023.5, 10362.7],
        backlash = -2,   # is this configured somewhere?
        precision = 0.5,
        masks = {
            'ng': global_values['ng'],
            'rc': global_values['ng'],
            'vc': global_values['vc'],
            'fc': global_values['fc'],
        }
    ),
    nok9_mode = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'nok9 mode',
        device = 'nok9',
        parameter = 'mode',
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok9r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK9, reactor side',
        motor = 'nok9r_motor',
        coder = 'nok9r_motor',
        # obs = ['nok9r_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok9_srll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srll of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srll' % nethost,
        lowlevel = True,
    ),

    nok9_srhl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srhl of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srhl' % nethost,
        lowlevel = True,
    ),

    nok9_srref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srref of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srref' % nethost,
        lowlevel = True,
    ),

    nok9_srrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srrel of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srrel' % nethost,
        lowlevel = True,
    ),

    nok9_srsll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srsll of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srsll' % nethost,
        lowlevel = True,
    ),

    nok9_srshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/srshl of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/srshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok9r_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK9, reactor side',
        abslimits = (-647.03375, 602.965),
        userlimits = (-112.03425, 142.95925),
        bus = 'nokbus3',     # from ipcsms_*.res
        addr = 0x56,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 1,
        accel = 1,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 103.086,    # from ipcsms_*.res
        zerosteps = int(647.034 * 800),  # offset * slope
    ),
    nok9r_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok9r_motor',
         analog = 'nok9r_obs',
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok9r_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK9, reactor side',
        reference = 'nok_refc2',
        measure = 'nok9r_poti',
        poly = [-99.195992, 1000.37 / 1.922],    # off, mul * 1000 / sensitivity, higher orders...
        serial = 7779,
        length = 500.0,
        lowlevel = True,
    ),

    # generated from global/inf/poti_tracing.inf
    nok9r_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK9, reactor side',
        tacodevice = '//%s/test/wb_c/2_3' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf
    nok9s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK9, sample side',
        motor = 'nok9s_motor',
        coder = 'nok9s_motor',
        # obs = ['nok9s_obs'],
        backlash = 0,
        precision = 0.5,
        unit = 'mm',
        lowlevel = True,
    ),

    nok9_ssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/ssll of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/ssll' % nethost,
        lowlevel = True,
    ),

    nok9_sshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/sshl of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/sshl' % nethost,
        lowlevel = True,
    ),

    nok9_ssref = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/ssref of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/ssref' % nethost,
        lowlevel = True,
    ),

    nok9_ssrel = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/ssrel of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/ssrel' % nethost,
        lowlevel = True,
    ),

    nok9_sssll = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/sssll of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/sssll' % nethost,
        lowlevel = True,
    ),

    nok9_ssshl = device('nicos.devices.taco.DigitalInput',
        description = 'Device test/nok9/ssshl of Server ipcsmsserver nok9',
        tacodevice = '//%s/test/nok9/ssshl' % nethost,
        lowlevel = True,
    ),

    # generated from global/inf/resources.inf, geometrie.inf, optic.inf and taco *.res files
    nok9s_motor = device('nicos_mlz.refsans.devices.nok_support.NOKMotorIPC',
        description = 'IPC controlled Motor of NOK9, sample side',
        abslimits = (-663.60125, 586.3975),
        userlimits = (-114.51425, 142.62775),
        bus = 'nokbus4',     # from ipcsms_*.res
        addr = 0x61,     # from resources.inf
        slope = 800.0,   # FULL steps per physical unit
        speed = 1,
        accel = 1,
        confbyte = 48,
        ramptype = 2,
        microstep = 1,
        refpos = 86.749,     # from ipcsms_*.res
        zerosteps = int(663.601 * 800),  # offset * slope
        lowlevel = True,
    ),

    nok9s_acc = device('nicos_mlz.refsans.devices.nok_support.MotorEncoderDifference',
         description = 'calc error Motor and poti',
         motor = 'nok9s_motor',
         analog = 'nok9s_obs',
         unit = 'mm'
    ),

    # generated from global/inf/poti_tracing.inf
    nok9s_obs = device('nicos_mlz.refsans.devices.nok_support.NOKPosition',
        description = 'Position sensing for NOK9, sample side',
        reference = 'nok_refc2',
        measure = 'nok9s_poti',
        poly = [80.372504, 998.695 / 1.919],     # off, mul * 1000 / sensitivity, higher orders...
        serial = 7789,
        length = 500.0,
        lowlevel = True,
    ),

    # generated from global/inf/poti_tracing.inf
    nok9s_poti = device('nicos_mlz.refsans.devices.nok_support.NOKMonitoredVoltage',
        description = 'Poti for NOK9, sample side',
        tacodevice = '//%s/test/wb_c/2_4' % nethost,
        scale = -1,  # mounted from top
        lowlevel = True,
    ),
)
