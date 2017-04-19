description = 'Neutron Grating Interferometer'

group = 'optional'

tango_base = 'tango://antareshw.antares.frm2:10000/antares/'

includes = []


devices = dict(
    G0rz  = device('devices.tango.Motor',
                   speed = 1,
                   unit = 'deg',
                   description = 'Rotation of G0 grating around beam direction',
                   tangodevice = tango_base + 'fzjs7/G0rz',
                   abslimits = (-400, 400),
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.01,
                  ),

    G0ry  = device('devices.tango.Motor',
                   speed = 1,
                   unit = 'deg',
                   description = 'Rotation of G0 grating around vertical axis',
                   tangodevice = tango_base + 'fzjs7/G0ry',
                   abslimits = (-1, 400),
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.01,
                  ),

    G0tx  = device('devices.tango.Motor',
                   speed = 0.5,
                   unit = 'mm',
                   description = 'Stepping of G0 perpendicular to the beam direction',
                   tangodevice = tango_base + 'fzjs7/G0tx',
                   abslimits = (-2, 25),
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.01,
                  ),

    G1rz  = device('devices.tango.Motor',
                   speed = 0.2,
                   unit = 'deg',
                   description = 'Rotation of G1 grating around beam direction',
                   tangodevice = tango_base + 'fzjs7/G1rz',
                   abslimits = (-400, 400),
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.0005,
                  ),

    G1tz  = device('devices.tango.Motor',
                   speed = 1,
                   unit = 'mm',
                   description = 'Translation of G1 in beam direction. (Talbot distance)',
                   tangodevice = tango_base + 'fzjs7/G1tz',
                   abslimits = (-99999, 99999),  # Really?!
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.05,
                  ),

    G12rz = device('devices.tango.Motor',
                   speed = 1,
                   unit = 'deg',
                   description = 'Rotation of G2 and G1 around beam axis',
                   tangodevice = tango_base + 'fzjs7/G12rz',
                   abslimits = (-400, 400),
                   userlimits = (-250, 250),
                   maxage = 5,
                   pollinterval = 3,
                   precision = 0.01,
                  ),
)
