description = 'NOK5a using Beckhoff controllers'

group = 'lowlevel'

global_values = configdata('global.GLOBAL_Values')

devices = dict(
    nok5a_r_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK5a, reactor side',
        motor = device('nicos.devices.generic.VirtualMotor',
            unit = 'mm',
            abslimits = (-70.0,67.68),
            speed = 1.,
        ),
        offset = 0.0,
        backlash = 0,
        precision = global_values['precision'],
        maxtries = 3,
        lowlevel = True,
    ),
    nok5a_s_axis = device('nicos.devices.generic.Axis',
        description = 'Axis of NOK5a, sample side',
        motor = device('nicos.devices.generic.VirtualMotor',
            unit = 'mm',
            abslimits = (-79.0,77.85),
            speed = 1.,
        ),
        offset = 0.0,
        backlash = 0,
        precision = global_values['precision'],
        maxtries = 3,
        lowlevel = True,
    ),
    nok5a = device('nicos_mlz.refsans.devices.nok_support.DoubleMotorNOK',
        description = 'NOK5a',
        fmtstr = '%.2f, %.2f',
        nok_start = 2418.50,
        nok_length = 1719.20,
        nok_end = 4137.70,
        nok_gap = 1.0,
        nok_motor = [3108.00, 3888.00],
        offsets = (0.0, 0.0),
        inclinationlimits = (-100, 100),
        motor_r = 'nok5a_r_axis',
        motor_s = 'nok5a_s_axis',
        backlash = -2,
        masks = {
            'ng': global_values['ng'],
            'rc': global_values['ng'],
            'vc': global_values['vc'],
            'fc': global_values['fc'],
            # 'pola': global_values['pola'],
        },
    ),
)