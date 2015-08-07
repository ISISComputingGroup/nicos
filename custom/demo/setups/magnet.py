description = 'plug-and-play magnet sample environment'
group = 'optional'

includes = ['alias_B']

devices = dict(
    B_virt            = device('devices.generic.VirtualMotor',
                               description = 'virtual "magnetic field"',
                               abslimits = (-10, 10),
                               unit = 'T'),

    garfield_onoff    = device('nicos.devices.generic.ManualSwitch',
                               description = 'on/off switch',
                               states = ['on', 'off'],
                              ),
    garfield_polarity = device('nicos.devices.generic.ManualSwitch',
                               description = 'polarity switch',
                               states = ['+', '-'],
                              ),
    garfield_current  = device('devices.generic.VirtualMotor',
                               description = 'current source for garfield test',
                               abslimits = (0, 250),
                               unit = 'A',
                               ramp = 1.,
                              ),
    B_garfield        = device('frm2.magnet.GarfieldMagnet',
                               description = 'magnetic field device, handling polarity switching and stuff',
                               currentsource = 'garfield_current',
                               onoffswitch = 'garfield_onoff',
                               polswitch = 'garfield_polarity',
                               unit = 'T',
                               calibration = (0.0018467, -0.0346142, 0.021774, 0.0638581, 0.0541159),
                               abslimits = (-0.75, 0.75),
                              ),

    mira_switch       = device('nicos.devices.generic.ManualSwitch',
                               description = 'polarity switch',
                               states = [-1, 0, 1],
                              ),
    mira_current      = device('devices.generic.VirtualMotor',
                               description = 'current source for miramagnet test',
                               abslimits = (-250, 250),
                               unit = 'A',
                               ramp = 1.,
                              ),
    B_mira            = device('frm2.magnet.MiraMagnet',
                               description = 'magnetic field device, handling polarity switching and stuff',
                               currentsource = 'mira_current',
                               switch = 'mira_switch',
                               unit = 'T',
                               calibration = (0.000872603, -0.0242964, 0.0148907,
                                              0.0437158, 0.0157436),
                               abslimits = (-0.5, 0.5),
                              ),
)

alias_config = [
    ('B', 'B_mira', 100),
    ('B', 'B_garfield', 99),
    ('B', 'B_virt', 0),
]
