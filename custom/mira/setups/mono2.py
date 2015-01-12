description = 'MIRA2 monochromator'
group = 'lowlevel'

includes = ['base', 'mslit2']

devices = dict(
    m2tt     = device('devices.taco.HoveringAxis',
                      description = 'Monochromator two-theta angle',
                      tacodevice = '//mirasrv/mira/axis/m2tt',
                      abslimits = (-170, -20),
                      startdelay = 1,
                      stopdelay = 4,
                      backlash = 1,
                      speed = 0.25,
                      switch = 'air_mono',
                      switchvalues = (0, 1),
                      fmtstr = '%.3f',
                     ),

    m2th     = device('mira.axis.PhytronAxis',
                      description = 'Monochromator theta angle',
                      tacodevice = '//mirasrv/mira/axis/m2th',
                      abslimits = (-54, -31),
                      fmtstr = '%.3f',
                     ),

    mono     = device('devices.tas.Monochromator',
                      description = 'Monochromator unit to move incoming wavevector',
                      unit = 'A-1',
                      theta = 'm2th',
                      twotheta = 'm2tt',
                      focush = None,
                      focusv = 'm2fv',
                      abslimits = (0.1, 10),
                      # calibration 1/2013, valid from 1.2 to 1.4 ki
                      vfocuspars = [220.528, -40.485, 2.789],
                      scatteringsense = -1,
                      dvalue = 3.355,
                     ),

    m2tx     = device('mira.axis.PhytronAxis',
                      description = 'Monochromator translation parallel to the blades',
                      tacodevice = '//mirasrv/mira/axis/m2tx',
                      abslimits = (-12.5, 10),
                      fmtstr = '%.2f',
                     ),
    m2ty     = device('mira.axis.PhytronAxis',
                      description = 'Monochromator translation perpendicular to the blades',
                      tacodevice = '//mirasrv/mira/axis/m2ty',
                      abslimits = (-14.9, 9.9),
                      fmtstr = '%.2f',
                     ),
    m2gx     = device('mira.axis.PhytronAxis',
                      description = 'Monochromator tilt',
                      tacodevice = '//mirasrv/mira/axis/m2gx',
                      abslimits = (-1, 1),
                      fmtstr = '%.2f',
                     ),
    m2fv     = device('mira.axis.PhytronAxis',
                      description = 'Monochromator vertical focus',
                      tacodevice = '//mirasrv/mira/axis/m2fv',
                      abslimits = (-360, 360),
                      fmtstr = '%.2f',
                     ),
    #PBe      = device('mira.varian.VarianPump',
    #                  description = 'Be filter pressure',
    #                  tacodevice = '//mirasrv/mira/network/rs10_3',
    #                  warnlimits = (1e-8, 1e-5),
    #                  fmtstr = '%.2g',
    #                  unit = 'mbar',
    #                 ),
    Pccr     = device('devices.taco.AnalogInput',
                      description = 'CCR isolation vacuum pressure',
                      tacodevice = '//mirasrv/mira/leybold/sensor',
                      warnlimits = (1e-9, 1e-5),
                      fmtstr = '%.2g',
                     ),
    TBe      = device('devices.taco.TemperatureSensor',
                      description = 'Sensor D: Be filter temperature',
                      tacodevice = '//mirasrv/mira/ls340/d',
                      warnlimits = (0, 65),
                      pollinterval = 3,
                      maxage = 5,
                      fmtstr = '%.1f',
                     ),
)
