description = 'all values for detector positon'

group = 'lowlevel'

nethost = 'refsanssrv.refsans.frm2'
tango_base = 'tango://refsansctrl02.refsans.frm2.tum.de:10000/'

devices = dict(
    det_drift = device('nicos.devices.generic.ManualSwitch',
        description = 'depth of detector drift1=40mm drift2=65mm',
        states = ['off','drift1', 'drift2'],
    ),
    det_pivot = device('nicos_mlz.refsans.devices.pivot.PivotPoint',
        description = 'Pivot point at floor of samplechamber',
        states = list(range(1, 14)),
        fmtstr = 'Point %d',
        unit = '',
    ),
    det_yoke_m = device('nicos.devices.tango.Motor',
        description = 'yoke Motor',
        tangodevice = tango_base + 'test/tube/servostar',
        abslimits = (-120, 1000),
        lowlevel = True,
    ),
    det_yoke = device('nicos.devices.generic.Axis',
        description = 'yoke height',
        motor = 'det_yoke_m',
        obs = [],
        precision = 0.05,
        dragerror = 10.,
    ),
    table_z_motor = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffMotorDetector',
        description = 'table inside scatteringtube',
        tangodevice = tango_base + 'det_table/io/modbus',
        address = 0x3020 + 0 * 10,  # word address
        slope = 100,
        unit = 'mm',
        abslimits = (1000, 11025),  # because of Beamstop
        precision = 10,
        lowlevel = True,
    ),
    table_z_obs = device('nicos_mlz.refsans.devices.beckhoff.nok.BeckhoffCoderDetector',
        description = 'Coder of detector table inside scatteringtube',
        tangodevice = tango_base + 'det_table/io/modbus',
        address = 0x3020 + 1 * 10,  # word address
        slope = 100,
        unit = 'mm',
        lowlevel = True,
    ),
    det_table_a = device('nicos.devices.generic.Axis',
        description = 'detector table inside scatteringtube. absmin is for beamstop',
        motor = 'table_z_motor',
        obs = ['table_z_obs'],
        precision = 1,
        dragerror = 15.,
        lowlevel = True,
    ),
    det_table = device('nicos_mlz.refsans.devices.focuspoint.FocusPoint',
        description = 'detector table inside scatteringtube. with pivot',
        unit = 'mm',
        table = 'det_table_a',
        pivot = 'det_pivot',
    ),
)
