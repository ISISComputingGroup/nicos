description = 'sample table and radial collimator'

group = 'lowlevel'

nethost = 'toftofsrv.toftof.frm2'

devices = dict(
    gx = device('nicos.devices.taco.motor.Motor',
        description = 'X translation of the sample table',
        tacodevice = '//%s/toftof/huber/gxm' % nethost,
        fmtstr = "%7.3f",
        abslimits = (0.0, 40.),
    ),
    gy = device('nicos.devices.taco.motor.Motor',
        description = 'Y translation of the sample table',
        tacodevice = '//%s/toftof/huber/gym' % nethost,
        fmtstr = "%7.3f",
        abslimits = (0.0, 40.),
    ),
    gz = device('nicos.devices.taco.motor.Motor',
        description = 'Z translation of the sample table',
        tacodevice = '//%s/toftof/huber/gzm' % nethost,
        fmtstr = "%7.3f",
        abslimits = (-14.8, 50.),
    ),
    gcx = device('nicos.devices.taco.motor.Motor',
        description = 'Chi rotation of the sample goniometer',
        tacodevice = '//%s/toftof/huber/gcxm' % nethost,
        fmtstr = "%7.3f",
        abslimits = (-20.0, 20.),
    ),
    gcy = device('nicos.devices.taco.motor.Motor',
        description = 'Psi rotation of the sample goniometer',
        tacodevice = '//%s/toftof/huber/gcym' % nethost,
        fmtstr = "%7.3f",
        abslimits = (-20.0, 20.),
    ),
    gphi = device('nicos.devices.taco.motor.Motor',
        description = 'Phi rotation of the sample table',
        tacodevice = '//%s/toftof/huber/gphim' % nethost,
        fmtstr = "%7.3f",
        abslimits = (-100.0, 100.),
    ),
)
