description = 'bottom sample table devices'

group = 'lowlevel'

tango_base = 'tango://sans1hw.sans1.frm2:10000/sans1/table/'

devices = dict(
    st1_omg = device('nicos.devices.generic.Axis',
        description = 'table 1 omega axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-180, 180),
        precision = 0.01,
        motor = 'st1_omgmot',
        coder = 'st1_omgenc',
        obs = [],
    ),
    st1_omgmot = device('nicos.devices.tango.Motor',
        description = 'table 1 omega motor',
        tangodevice = tango_base + 'st1_omgmot',
        fmtstr = '%.2f',
        abslimits = (-180, 180),
        lowlevel = True,
    ),
    st1_omgenc = device('nicos.devices.tango.Sensor',
        description = 'table 1 omega encoder',
        tangodevice = tango_base + 'st1_omgenc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    st1_chi = device('nicos.devices.generic.Axis',
        description = 'table 1 chi axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-5, 5),
        precision = 0.01,
        motor = 'st1_chimot',
        coder = 'st1_chienc',
        obs = [],
    ),
    st1_chimot = device('nicos.devices.tango.Motor',
        description = 'table 1 chi motor',
        tangodevice = tango_base + 'st1_chimot',
        fmtstr = '%.2f',
        abslimits = (-5, 5),
        lowlevel = True,
    ),
    st1_chienc = device('nicos.devices.tango.Sensor',
        description = 'table 1 chi encoder',
        tangodevice = tango_base + 'st1_chienc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    st1_phi = device('nicos.devices.generic.Axis',
        description = 'table 1 phi axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-5, 5),
        precision = 0.01,
        motor = 'st1_phimot',
        coder = 'st1_phienc',
        obs = [],
    ),
    st1_phimot = device('nicos.devices.tango.Motor',
        description = 'table 1 phi motor',
        tangodevice = tango_base + 'st1_phimot',
        fmtstr = '%.2f',
        abslimits = (-5, 5),
        lowlevel = True,
    ),
    st1_phienc = device('nicos.devices.tango.Sensor',
        description = 'table 1 phi encoder',
        tangodevice = tango_base + 'st1_phienc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    st1_y = device('nicos.devices.generic.Axis',
        description = 'table 1 y axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-99, 99),
        precision = 0.01,
        motor = 'st1_ymot',
        coder = 'st1_yenc',
        obs = [],
    ),
    st1_ymot = device('nicos.devices.tango.Motor',
        description = 'table 1 y motor',
        tangodevice = tango_base + 'st1_ymot',
        fmtstr = '%.2f',
        abslimits = (-99, 99),
        lowlevel = True,
    ),
    st1_yenc = device('nicos.devices.tango.Sensor',
        description = 'table 1 y encoder',
        tangodevice = tango_base + 'st1_yenc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    st1_z = device('nicos.devices.generic.Axis',
        description = 'table 1 z axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-50, 50),
        precision = 0.01,
        motor = 'st1_zmot',
        coder = 'st1_zenc',
        obs = [],
    ),
    st1_zmot = device('nicos.devices.tango.Motor',
        description = 'table 1 z motor',
        tangodevice = tango_base + 'st1_zmot',
        fmtstr = '%.2f',
        abslimits = (-50, 50),
        lowlevel = True,
    ),
    st1_zenc = device('nicos.devices.tango.Sensor',
        description = 'table 1 z encoder',
        tangodevice = tango_base + 'st1_zenc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    st1_x = device('nicos.devices.generic.Axis',
        description = 'table 1 x axis',
        pollinterval = 15,
        maxage = 60,
        fmtstr = '%.2f',
        abslimits = (-500.9, 110.65),
        precision = 0.01,
        motor = 'st1_xmot',
        coder = 'st1_xenc',
        obs = [],
    ),
    st1_xmot = device('nicos.devices.tango.Motor',
        description = 'table 1 x motor',
        tangodevice = tango_base + 'st1_xmot',
        fmtstr = '%.2f',
        abslimits = (-750, 150),
        lowlevel = True,
    ),
    st1_xenc = device('nicos.devices.tango.Sensor',
        description = 'table 1 x encoder',
        tangodevice = tango_base + 'st1_xenc',
        fmtstr = '%.2f',
        lowlevel = True,
    ),
)
