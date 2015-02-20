description = 'virtual detector'
group = 'lowlevel'

includes = ['system']

devices = dict(
    card     = device('devices.generic.VirtualCounterCard',
                      lowlevel = True
                     ),

    timer    = device('devices.generic.VirtualTimer',
                      lowlevel = True,
                      card = 'card',
                     ),

    mon1     = device('devices.generic.VirtualCounter',
                      lowlevel = True,
                      type = 'monitor',
                      countrate = 1000,
                      card = 'card',
                      fmtstr = '%d',
                     ),

    ctr1     = device('devices.generic.VirtualCounter',
                      lowlevel = True,
                      type = 'counter',
                      countrate = 2000,
                      card = 'card',
                      fmtstr = '%d',
                     ),

    ctr2     = device('devices.generic.VirtualCounter',
                      lowlevel = True,
                      type = 'counter',
                      countrate = 120,
                      card = 'card',
                      fmtstr = '%d',
                     ),

    det      = device('devices.generic.MultiChannelDetector',
                      description = 'Classical detector with single channels',
                      timer = 'timer',
                      monitors = ['mon1'],
                      counters = ['ctr1', 'ctr2'],
                      maxage = 3,
                      pollinterval = 0.5,
                     ),

    card2    = device('devices.generic.VirtualCounterCard',
                      lowlevel = True
                     ),

    ctr4     = device('devices.generic.VirtualCounter',
                      description = 'single counter channel demo',
                      type = 'counter',
                      countrate = 3000,
                      card = 'card2',
                      fmtstr = '%d',
                     ),
)

startupcode='''
SetDetectors(det)
'''
