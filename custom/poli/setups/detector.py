description = 'POLI detector and counter card'
group = 'lowlevel'

includes = []

nethost = 'heidi22.poli.frm2'

devices = dict(
    timer = device('devices.taco.FRMTimerChannel',
                   tacodevice = '//%s/heidi2/frmctr/at' % nethost,
                   fmtstr = '%.2f',
                   lowlevel = True,
                  ),
    mon1  = device('devices.taco.FRMCounterChannel',
                   tacodevice = '//%s/heidi2/frmctr/a1' % nethost,
                   type = 'monitor',
                   fmtstr = '%d',
                   lowlevel = True,
                  ),
    mon2  = device('devices.taco.FRMCounterChannel',
                   tacodevice = '//%s/heidi2/frmctr/a2' % nethost,
                   type = 'monitor',
                   fmtstr = '%d',
                   lowlevel = True,
                  ),
    ctr1  = device('devices.taco.FRMCounterChannel',
                   tacodevice = '//%s/heidi2/frmctr/a3' % nethost,
                   type = 'counter',
                   fmtstr = '%d',
                   lowlevel = True,
                  ),

    det   = device('devices.generic.MultiChannelDetector',
                   description = 'FRM-II multichannel counter card',
                   timer  = 'timer',
                   monitors = ['mon1', 'mon2'],
                   counters = ['ctr1'],
                   fmtstr = 'timer %s, mon1 %s, mon2 %s, ctr1 %s',
                   maxage = 2,
                   pollinterval = 1.0,
                  ),
)

startupcode = """
SetDetectors(det)
"""
