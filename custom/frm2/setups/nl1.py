description = 'FRM-II neutron guide line 1 shutter'

group = 'lowlevel'

includes = ['guidehall']

nethost = 'tacodb.taco.frm2'

devices = dict(
    NL1      = device('devices.taco.NamedDigitalInput',
                      description = 'NL1 shutter status',
                      mapping = {0: 'closed', 1: 'open'},
                      pollinterval = 60,
                      maxage = 120,
                      tacodevice = '//%s/frm2/shutter/nl1' % (nethost, ),
                     ),
)
