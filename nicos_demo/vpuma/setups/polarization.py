description = 'Polarization analysis'

group = 'basic'

includes = ['pumabase', 'multianalyzer', 'multidetector', 'cad', 'analyzer',
            'monochromator', 'aliases', 'lengths', 'slits']

devices = dict(
    ana_polarization = device('nicos.devices.tas.Monochromator',
        description = 'analyzer wavevector',
        unit = 'A-1',
        dvalue = 3.355,
        theta = 'ra6',
        twotheta = 'rd6_cad',
        focush = None,
        focusv = None,
        abslimits = (0.1, 10),
        scatteringsense = -1,
        crystalside = -1,
    ),
    rd6_cad = device('nicos_mlz.puma.devices.StackedAxis',
        description = "Combined axis of 'rd6' and 'cad'",
        # description = 'Sample scattering angle Two Theta',
        bottom = 'cad',
        top = 'rd6',
    ),
    lsd1 = device('nicos.devices.generic.ManualMove',
        description = 'distance sample-deflector 1',
        default = 633,
        unit = 'mm',
        fmtstr = '%.0f',
        abslimits = (0, 1000),
    ),
    lsd2 = device('nicos.devices.generic.ManualMove',
        description = 'distance sample-deflector 2',
        default = 683,
        unit = 'mm',
        fmtstr = '%.0f',
        abslimits = (0, 1000),
    ),
    d = device('nicos.devices.generic.ManualMove',
        description = 'distance of analyzer rails',
        default = 20,
        unit = 'mm',
        fmtstr = '%.0f',
        abslimits = (20., 20.),
    ),
    bA = device('nicos.devices.generic.ManualMove',
        description = 'width of analyzer blades',
        default = 25,
        unit = 'mm',
        fmtstr = '%.1f',
        abslimits = (25, 25),
    ),
    dA = device('nicos.devices.generic.ManualMove',
        description = 'net plane distance analyzer',
        default = 3.354,
        unit = 'AA',
        abslimits = (3.354, 3.354),
    ),
    bD = device('nicos.devices.generic.ManualMove',
        description = 'diameter of detector tubes',
        default = 25.4,
        unit = 'mm',
        fmtstr = '%.2f',
        abslimits = (25.4, 25.4),
    ),
    tilt = device('nicos_mlz.puma.devices.Collimator',
        description = 'tilt angle of collimator',
        motor = device('nicos.devices.generic.VirtualMotor',
            curvalue = -0.6,
            fmtstr = '%.2f',
            abslimits = (-5, 5),
            unit = 'deg',
        ),
        precision = 0.05,
    ),
    alpha0 = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'collimator divergency',
        device = 'tilt',
        parameter = 'divergency',
        unit = 'deg',
        fmtstr = '%.1f',
    ),
    gamma1 = device('nicos_mlz.puma.devices.Deflector',
        description = 'tilt angle of deflector 1',
        motor = device('nicos.devices.generic.VirtualMotor',
            curvalue = -0.8,
            unit = 'deg',
            fmtstr = '%.2f',
            abslimits = (-5, 5),
        ),
        precision = 0.05,
    ),
    gamma2 = device('nicos_mlz.puma.devices.Deflector',
        description = 'tilt angle of deflector 2',
        motor = device('nicos.devices.generic.VirtualMotor',
            curvalue = 0.75,
            unit = 'deg',
            fmtstr = '%.2f',
            abslimits = (-5, 5),
        ),
        precision = 0.05,
    ),
    eta = device('nicos.devices.generic.ManualMove',
        description = 'analyzer mosaicity',
        default = 0.4,
        unit = 'deg',
        fmtstr = '%.1f',
        abslimits = (0.4, 0.4)
    ),
    lpsd = device('nicos.devices.generic.ManualMove',
        description = 'distance sample PSD',
        default = 2316,
        unit = 'mm',
        fmtstr = '%.0f',
        abslimits = (2316, 2316),
    ),
    psdwidth = device('nicos.devices.generic.ManualMove',
        description = 'PSD channel width',
        default = 0.7,
        unit = 'mm',
        fmtstr = '%.2f',
        abslimits = (0.7, 0.7),
    ),
    R = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'peak reflectivity',
        device = 'gamma1',
        parameter = 'reflectivity',
        unit = '',
        fmtstr = '%.1f',
    ),
    L = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'deflector length',
        device = 'gamma1',
        parameter = 'length',
        unit = 'mm',
        fmtstr = '%.1f',
    ),
    dWA = device('nicos.devices.generic.ReadonlyParamDevice',
        description = 'wafer thickness',
        device = 'gamma1',
        parameter = 'thickness',
        unit = 'mm',
        fmtstr = '%.2f',
    ),
    bS = device('nicos.devices.generic.ManualMove',
        description = 'sample slit width',
        default = 10,
        unit = 'mm',
        fmtstr = '%.2f',
        abslimits = (0, 40),
    ),
)

alias_config = {
    'ana': {'ana_polarization': 200},
}
