description = 'detector related devices including beamstop'

includes = []

# included by sans1
group = 'lowlevel'

nethost = 'sans1srv.sans1.frm2'

tangohost = 'tango://sans1hw.sans1.frm2:10000'

BS1_X_OFS = -475.055  # from entangle

devices = dict(
    det1_t_ist = device('nicos.devices.taco.FRMTimerChannel',
        description = 'measured time of detector 1',
        tacodevice = '//%s/sans1/qmesydaq/timer' % (nethost,),
        fmtstr = '%.0f',
        lowlevel = True,
        maxage = 120,
        pollinterval = 15,
    ),
    # det1_t_ist = device('nicos.devices.taco.FRMTimerChannel',
    #     tacodevice = '//%s/sans1/qmesydaq/det' % (nethost, ),
    #     fmtstr = '%.1f',
    #     pollinterval = 1,
    #     maxage = 3,
    #     # lowlevel = True,
    # ),
    # det1_t_soll = device('nicos.devices.taco.FRMTimerChannel',
    #     tacodevice = '//%s/sans1/qmesydaq/timer' % (nethost, ),
    #     fmtstr = '%.1f',
    #     pollinterval = 5,
    #     maxage = 13,
    #     # lowlevel = True,
    # ),
    det1_hv_interlock = device('nicos.devices.tango.DigitalInput',
        description = 'interlock for detector 1 high voltage',
        tangodevice = '%s/sans1/interlock/hv' % (tangohost, ),
        lowlevel = True,
    ),
    det1_hv_discharge_mode = device('nicos.devices.tango.DigitalInput',
        description = 'set discharge mode of detector 1',
        tangodevice = '%s/sans1/interlock/mode' % (tangohost, ),
        lowlevel = True,
    ),
    det1_hv_discharge = device('nicos.devices.tango.DigitalOutput',
        description = 'enable and disable discharge of detector 1',
        tangodevice = '%s/sans1/interlock/discharge' % (tangohost, ),
        lowlevel = True,
    ),
    # det1_hv_supply = device('nicos.devices.taco.VoltageSupply',
    det1_hv_supply = device('nicos_mlz.sans1.devices.hv.VoltageSupply',
        description = 'high voltage power supply of detector 1',
        tacodevice = '//%s/sans1/iseg/hv' % (nethost,),
        abslimits = (0.0, 1501.0),
        maxage = 120,
        pollinterval = 15,
        fmtstr = '%d',
        lowlevel = True,
        precision = 3,
    ),
    det1_hv_ax = device('nicos_mlz.sans1.devices.hv.Sans1HV',
        description = 'high voltage of detector 1',
        unit = 'V',
        fmtstr = '%d',
        supply = 'det1_hv_supply',
        discharger = 'det1_hv_discharge',
        interlock = 'det1_hv_interlock',
        maxage = 120,
        pollinterval = 15,
        lowlevel = True,
    ),
    det1_hv_offtime = device('nicos_mlz.sans1.devices.hv.Sans1HVOffDuration',
        description = 'Duration below operating voltage',
        hv_supply = 'det1_hv_ax',
        maxage = 120,
        pollinterval = 15,
    ),
    # det1_hv = device('nicos.devices.generic.Switcher',
    det1_hv = device('nicos_mlz.sans1.devices.hv.VoltageSwitcher',
        description = 'high voltage of detector 1 switcher',
        moveable = 'det1_hv_ax',
        mapping = {'ON': (1500, 1),
                   'LOW': (1, 69),
                   'OFF': (0, 1)},
        precision = 1,
        unit = '',
        fallback = 'unknown',
    ),
    hv_current = device('nicos.devices.taco.AnalogInput',
        description = 'high voltage current of detector 1',
        tacodevice = '//%s/sans1/iseg/hv-current' % (nethost,),
        maxage = 120,
        pollinterval = 15,
        lowlevel = True,
    ),
    # det1_x = device('nicos.devices.taco.Axis',
    #     description = 'detector 1 x axis',
    #     tacodevice = '//%s/sans1/detector1/x' % (nethost, ),
    #     fmtstr = '%.1f',
    #     abslimits = (4, 570),
    #     maxage = 120,
    #     pollinterval = 5,
    #     requires = dict(level='admin'),
    #     precision = 0.3,
    # ),
    det1_x = device('nicos.devices.generic.Axis',
        description = 'detector 1 x axis',
        fmtstr = '%.0f',
        abslimits = (4, 570),
        maxage = 120,
        pollinterval = 5,
        requires = dict(level = 'admin'),
        precision = 0.3,
        motor = 'det1_xmot',
        coder = 'det1_xenc',
        obs = [],
    ),
    det1_xmot = device('nicos.devices.tango.Motor',
        description = 'detector 1 x motor',
        tangodevice = '%s/sans1/detector1/x_mot' % (tangohost, ),
        fmtstr = '%.1f',
        abslimits = (4, 570),
        lowlevel = True,
    ),
    det1_xenc = device('nicos.devices.tango.Sensor',
        description = 'detector 1 x motor',
        tangodevice = '%s/sans1/detector1/x_enc' % (tangohost, ),
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    det1_z = device('nicos.devices.generic.LockedDevice',
        description =
        'detector 1 z position interlocked with high voltage supply',
        device = 'det1_z_ax',
        lock = 'det1_hv',
        # lockvalue = None,     # go back to previous value
        unlockvalue = 'LOW',
        # keepfixed = False,    # do not fix supply voltage after movement
        fmtstr = '%.0f',
        maxage = 120,
        pollinterval = 15,
    ),
    # det1_z_ax = device('nicos.devices.taco.Axis',
    #     description = 'detector 1 z axis',
    #     tacodevice = '//%s/sans1/detector1/z' % (nethost, ),
    #     fmtstr = '%.1f',
    #     abslimits = (1100, 20000),
    #     maxage = 120,
    #     pollinterval = 5,
    #     lowlevel = True,
    #     precision = 1,
    #     userlimits = (1111, 20000),
    # ),
    det1_z_ax = device('nicos.devices.generic.Axis',
        description = 'detector 1 z axis',
        fmtstr = '%.0f',
        abslimits = (1100, 20000),
        maxage = 120,
        pollinterval = 5,
        lowlevel = True,
        precision = 1.0,
        dragerror = 150.0,
        motor = 'det1_zmot',
        coder = 'det1_zenc',
        obs = [],
    ),
    # det1_zmot = device('nicos.devices.taco.motor.Motor',
    # det1_zmot = device('nicos.devices.tango.Motor',
    det1_zmot = device('nicos_mlz.sans1.devices.hv.Sans1ZMotor',
        description = 'detector 1 z motor',
        tangodevice = '%s/sans1/detector1/z_mot' % (tangohost, ),
        fmtstr = '%.1f',
        abslimits = (1100, 20000),
        userlimits = (1111, 20000),
        lowlevel = True,
    ),
    det1_zenc = device('nicos.devices.tango.Sensor',
        description = 'detector 1 z encoder',
        tangodevice = '%s/sans1/detector1/z_enc' % (tangohost, ),
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    # det1_omg = device('nicos.devices.taco.Axis',
    #     description = 'detector 1 omega axis',
    #     tacodevice = '//%s/sans1/detector1/omega' % (nethost, ),
    #     fmtstr = '%.1f',
    #     abslimits = (-0.2, 21),
    #     maxage = 120,
    #     pollinterval = 5,
    #     requires = dict(level='admin'),
    #     userlimits = (0, 20),
    #     precision = 0.2,
    # ),
    det1_omg = device('nicos.devices.generic.Axis',
        description = 'detector 1 omega axis',
        fmtstr = '%.0f',
        # abslimits = (-0.2, 21),
        maxage = 120,
        pollinterval = 5,
        requires = dict(level = 'admin'),
        precision = 0.2,
        motor = 'det1_omegamot',
        coder = 'det1_omegamot',
        obs = [],
    ),
    det1_omegamot = device('nicos.devices.tango.Motor',
        description = 'detector 1 omega motor',
        tangodevice = '%s/sans1/detector1/omg_mot' % (tangohost, ),
        fmtstr = '%.1f',
        # abslimits = (-0.2, 21),
        lowlevel = True,
    ),

    bs1_xmot = device('nicos.devices.tango.Motor',
        description = 'beamstop 1 x motor',
        tangodevice = '%s/sans1/beamstop1/x_mot' % tangohost,
        fmtstr = '%.2f',
        # abslimits = (480, 868), # taken from entangle
        lowlevel = True,
    ),
#    bs1_xenc = device('nicos.devices.tango.Sensor',
    bs1_xenc = device('nicos_mlz.sans1.devices.beamstop.FunnySensor',
        description = 'beamstop 1 x coder',
        tangodevice = '%s/sans1/beamstop1/x_enc' % (tangohost, ),
        fmtstr = '%.2f',
        lowlevel = True,
        limits = [0, 1000],
    ),
    bs1_ymot = device('nicos.devices.tango.Motor',
        description = 'beamstop 1 y motor',
        tangodevice = '%s/sans1/beamstop1/y_mot' % tangohost,
        fmtstr = '%.1f',
        # abslimits = (60, 590), # taken from entangle
        userlimits = (100, 500),
        lowlevel = True,
    ),
#    bs1_yenc = device('nicos.devices.tango.Sensor',
    bs1_yenc = device('nicos_mlz.sans1.devices.beamstop.FunnySensor',
        description = 'beamstop 1 y coder',
        tangodevice = '%s/sans1/beamstop1/y_enc' % (tangohost, ),
        fmtstr = '%.1f',
        # userlimits = (60, 590),
        lowlevel = True,
        limits = [-100, 600],
    ),
    bs1_xax = device('nicos_mlz.sans1.devices.beamstop.BeamStopAxis',
        description = 'beamstop 1 x axis',
        motor = 'bs1_xmot',
        coder = 'bs1_xenc',
        obs = [],
        precision = 0.1,
        fmtstr = '%.2f',
        lowlevel = True,
    ),
    bs1_yax = device('nicos_mlz.sans1.devices.beamstop.BeamStopAxis',
        description = 'beamstop 1 y axis',
        motor = 'bs1_ymot',
        coder = 'bs1_yenc',
        obs = [],
        precision = 0.1,
        fmtstr = '%.2f',
        lowlevel = True
    ),
    bs1 = device('nicos_mlz.sans1.devices.beamstop.BeamStop',
                       description = 'selects the shape of the beamstop',
                       xaxis = 'bs1_xax',
                       yaxis = 'bs1_yax',
                       ypassage = -99, # encoder value! # XXX!
                       unit = 'mm',
                       slots = { # in encoder values !
                                '100x100' : 125.2 - BS1_X_OFS,
                                'd35'     : 197.0 - BS1_X_OFS,
                                '70x70'   : 253.4 - BS1_X_OFS,
                                '55x55'   : 317.4 - BS1_X_OFS,
                                'none'    : 348.0 - BS1_X_OFS,  # no shapeholder!
                                '85x85'   : 390.4 - BS1_X_OFS,
                               },
                       # limits for free-move area (in encoder values!)
                       xlimits = (480, 868), # XXX!
                       ylimits = (100, 590), # XXX!
#                       requires = dict(level='admin'),
                      ),
    bs1_shape = device('nicos.devices.generic.ParamDevice',
                       description = 'selected beam shape',
                       device = 'bs1',
                       parameter = 'shape',
                      ),
)
