description = 'MIRA2 monochromator'
group = 'lowlevel'

includes = ['base', 'mslit2', 'sample', 'alias_mono']

tango_base = 'tango://mira1.mira.frm2:10000/mira/'

devices = dict(
    co_m2tt  = device('nicos.devices.tango.Sensor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2tt_enc',
                      unit = 'deg',
                     ),
    mo_m2tt  = device('nicos.devices.tango.Motor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2tt_mot',
                      unit = 'deg',
                      precision = 1,  # due to backlash
                     ),
    m2tt     = device('mira.axis.HoveringAxis',
                      description = 'monochromator two-theta angle',
                      precision = 0.04,
                      backlash = 1,
                      motor = 'mo_m2tt',
                      coder = 'co_m2tt',
                      obs = [],
                      startdelay = 1,
                      stopdelay = 4,
                      speed = 0.25,
                      switch = 'air_mono',
                      switchvalues = (0, 1),
                      fmtstr = '%.3f',
                     ),

    co_m2th  = device('nicos.devices.tango.Sensor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2th_enc',
                      unit = 'deg',
                     ),
    mo_m2th  = device('nicos.devices.tango.Motor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2th_mot',
                      unit = 'deg',
                      precision = 0.002,
                     ),
    m2th     = device('nicos.devices.generic.Axis',
                      description = 'monochromator theta angle',
                      motor = 'mo_m2th',
                      coder = 'co_m2th',
                      obs = [],
                      fmtstr = '%.3f',
                      precision = 0.002,
                     ),

    mono     = device('nicos.devices.tas.Monochromator',
                      description = 'monochromator unit to move incoming wavevector',
                      unit = 'A-1',
                      theta = 'm2th',
                      twotheta = 'm2tt',
                      focush = None,
                      focusv = 'm2fv',
                      abslimits = (0.1, 10),
                      # calibration 1/2013, valid from 1.2 to 1.4 ki
                      vfocuspars = [220.528, -40.485, 2.789],
                      scatteringsense = -1,
                      crystalside = -1,
                      dvalue = 3.355,
                     ),

    co_m2tx  = device('nicos.devices.tango.Sensor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2tx_enc',
                      unit = 'mm',
                     ),
    mo_m2tx  = device('nicos.devices.tango.Motor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2tx_mot',
                      unit = 'mm',
                      precision = 0.1,
                     ),
    m2tx     = device('nicos.devices.generic.Axis',
                      description = 'monochromator translation parallel to the blades',
                      motor = 'mo_m2tx',
                      coder = 'co_m2tx',
                      obs = [],
                      fmtstr = '%.2f',
                      precision = 0.1,
                     ),

    co_m2ty  = device('nicos.devices.tango.Sensor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2ty_enc',
                      unit = 'mm',
                     ),
    mo_m2ty  = device('nicos.devices.tango.Motor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2ty_mot',
                      unit = 'mm',
                      precision = 0.1,
                     ),
    m2ty     = device('nicos.devices.generic.Axis',
                      description = 'monochromator translation perpendicular to the blades',
                      motor = 'mo_m2ty',
                      coder = 'co_m2ty',
                      obs = [],
                      fmtstr = '%.2f',
                      precision = 0.1,
                     ),

    co_m2gx  = device('nicos.devices.tango.Sensor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2gx_enc',
                      unit = 'deg',
                     ),
    mo_m2gx  = device('nicos.devices.tango.Motor',
                      lowlevel = True,
                      tangodevice = tango_base + 'mono2/m2gx_mot',
                      unit = 'deg',
                      precision = 0.05,
                     ),
    m2gx     = device('nicos.devices.generic.Axis',
                      description = 'monochromator tilt',
                      motor = 'mo_m2gx',
                      coder = 'co_m2gx',
                      obs = [],
                      fmtstr = '%.2f',
                      precision = 0.05,
                     ),

    m2fv     = device('nicos.devices.tango.Motor',
                      description = 'monochromator vertical focus',
                      tangodevice = tango_base + 'mono2/m2fv_mot',
                      unit = 'deg',
                      precision = 0.5,
                      fmtstr = '%.1f',
                     ),

    PBe      = device('mira.center.CrappySensor',
                      description = 'Be filter pressure',
                      tangodevice = tango_base + 'leybold/sensor2',
                      warnlimits = (1e-8, 0.00051),
                      fmtstr = '%.2g',
                     ),
    Pccr     = device('mira.center.CrappySensor',
                      description = 'CCR isolation vacuum pressure',
                      tangodevice = tango_base + 'leybold/sensor1',
                      warnlimits = (1e-9, 1e-5),
                      fmtstr = '%.2g',
                     ),
    TBe      = device('nicos.devices.tango.Sensor',
                      description = 'LakeShore sensor: Be filter temperature',
                      tangodevice = tango_base + 'ls/t_be',
                      warnlimits = (0, 65),
                      pollinterval = 3,
                      maxage = 5,
                      fmtstr = '%.1f',
                     ),
)

startupcode = '''
mth.alias = m2th
mtt.alias = m2tt
mtx.alias = m2tx
mty.alias = m2ty
mgx.alias = m2gx
mfv.alias = m2fv
'''
