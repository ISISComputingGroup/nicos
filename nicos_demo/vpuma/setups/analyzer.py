description = 'Analyzer devices'

group = 'lowlevel'

includes = ['aliases']

devices = dict(
    st_ath = device('nicos.devices.generic.VirtualMotor',
        description = 'ath motor device',
        unit = 'deg',
        abslimits = (-0, 60),
        jitter = 0.0,
        speed = 0.5,
        lowlevel = True,
    ),
    ath = device('nicos.devices.generic.Axis',
        description = 'Rocking angle theta of analyser',
        motor = 'st_ath',
        precision = 0.01,
        # offset = -0.551,
        maxtries = 8,
    ),
    st_att = device('nicos.devices.generic.VirtualMotor',
        description = 'att motor device',
        unit = 'deg',
        abslimits = (-117, 117),
        jitter = 0.0,
        speed = 0.5,
        lowlevel = True,
    ),
    att = device('nicos.devices.generic.Axis',
        description = 'Scattering angle two-theta of analyser',
        motor = 'st_att',
        precision = 0.01,
        # offset = 0.205,
        jitter = 0.2,
        dragerror = 1,
        maxtries = 30,
    ),
    ana_pg002 = device('nicos.devices.tas.Monochromator',
        description = 'PG-002 analyzer',
        unit = 'A-1',
        theta = 'ath',
        twotheta = 'att',
        reltheta = True,
        focush = None,
        focusv = None,
        abslimits = (1, 5),
        dvalue = 3.355,
        scatteringsense = -1,
        crystalside = -1,
    ),
)

alias_config = {
    'ana': {'ana_pg002': 100},
}
