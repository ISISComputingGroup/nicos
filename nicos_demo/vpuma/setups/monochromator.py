description = 'Virtual monochromator devices'

group = 'lowlevel'

devices = dict(
    st_mth = device('nicos.devices.generic.VirtualMotor',
        description = 'mtt motor device',
        unit = 'deg',
        abslimits = (5, 175),
        jitter = 0.0,
        speed = 0.5,
        lowlevel = True,
    ),
    mth = device('nicos.devices.generic.Axis',
        description = 'Monochromator Theta',
        motor = 'st_mth',
        precision = 0.011,
        # offset = -0.236,
        maxtries = 10,
    ),
    st_mtt = device('nicos.devices.generic.VirtualMotor',
        description = 'monochromator scattering angle',
        unit = 'deg',
        abslimits = (-110, -14.1),
        jitter = 0.0,
        speed = 0.5,
        lowlevel = True,
    ),
    mtt = device('nicos.devices.generic.Axis',
        description = 'Monochromator Two Theta',
        motor = 'st_mtt',
        precision = 0.005,
        # offset = -0.151,
        maxtries = 10,
        jitter = 0.1,
        dragerror = 10,
    ),
    mfvpg  = device('nicos_mlz.puma.devices.focus.FocusAxis',
        description = 'Vertical focus of PG-Monochromator',
        motor = device('nicos.devices.generic.VirtualMotor',
            unit = 'deg',
            abslimits = (-20, 55),
        ),
        uplimit = 38,
        lowlimit = 16.0,
        flatpos = 37,
        startpos = 38,
        precision = 0.1,
    ),
    mfhpg  = device('nicos_mlz.puma.devices.focus.FocusAxis',
        description = 'Horizontal focus of PG-Monochromator',
        motor = device('nicos.devices.generic.VirtualMotor',
            unit = 'deg',
            abslimits = (-20, 55),
        ),
        uplimit = 70,
        lowlimit = -12.0,
        flatpos = 4.668,
        startpos = -7.874,
        precision = 0.1,
    ),
    mono_pg002 = device('nicos.devices.tas.Monochromator',
        description = 'PG-002 monochromator',
        order = 1,
        unit = 'A-1',
        theta = 'mth',
        twotheta = 'mtt',
        reltheta = True,
        focush = None,  # 'mfhpg',
        focusv = None,  # 'mfvpg',
        # focus value should equal mth (for arcane reasons...)
        hfocuspars = [0.59065,7.33506,0.86068,-0.22745,0.02901],
        vfocuspars = [0.59065,7.33506,0.86068,-0.22745,0.02901],
        abslimits = (1, 7.5),
        dvalue = 3.355,
        scatteringsense = -1,
        crystalside = -1,
    ),
)