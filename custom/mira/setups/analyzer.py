description = 'analyzer table'
group = 'lowlevel'

devices = dict(
#    ath      = device('mira.axis.PhytronAxis',
#                      description = 'analyzer theta',
#                      tacodevice = '//mirasrv/mira/axis/ath',
#                      abslimits = (90 - 90, 90 + 90),
#                      fmtstr = '%.3f',
#                      offset = 90.0),

    ath_co   = device('devices.taco.Coder',
                      tacodevice = '//mirasrv/mira/encoder/ath',
                      lowlevel = True),
    ath_mo   = device('devices.taco.Motor',
                      tacodevice = '//mirasrv/mira/motor/ath',
                      abslimits = (0, 180),
                      lowlevel = True),
    ath      = device('devices.generic.Axis',
                      description = 'Analyzer theta angle',
                      coder = 'ath_co',
                      motor = 'ath_mo',
                      obs = [],
                      precision = 0.005),

    att      = device('devices.taco.HoveringAxis',
                      description = 'Analyzer two-theta angle',
                      tacodevice = '//mirasrv/mira/axis/att',
                      abslimits = (-90 - 135, -90 + 135),
                      startdelay = 1,
                      stopdelay = 2,
                      switch = 'air_ana',
                      switchvalues = (0, 1),
                      fmtstr = '%.3f'),

#    att      = device('mira.axis.PhytronAxis',
#                      description = 'analyzer two-theta',
#                      tacodevice = '//mirasrv/mira/axis/att',
#                      abslimits = (-90 - 135, -90 + 135),
#                      fmtstr = '%.2f',
#                      offset = -90.0),
    vatt     = device('devices.generic.VirtualMotor',
                      description = 'Virtual analyzer two-theta',
                      abslimits = (-180, 180),
                      unit = 'deg'),

    ana      = device('devices.tas.Monochromator',
                      description = 'Analyzer unit (see ana.unit for setting new unit)',
                      unit = 'A-1',
                      theta = 'ath',
                      twotheta = 'att',
                      focush = None,
                      focusv = None,
                      abslimits = (0.1, 10),
                      dvalue = 3.355,
                      scatteringsense = -1),
)
