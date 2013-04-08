description = 'FRM-II Neutron guide hall west infrastructure devices'

group = 'lowlevel'

nethost = 'tacodb.taco.frm2'

devices = dict(
    Sixfold  = device('devices.taco.NamedDigitalInput',
                      description = 'Sixfold shutter status',
                      mapping = {'closed': 0, 'open': 1},
                      pollinterval = 60,
                      maxage = 120,
                      tacodevice = '//%s/frm2/shutter/sixfold' % (nethost, )
                     ),

    Crane    = device('devices.taco.AnalogInput',
                      description = 'The position of the crane in the guide '
                                    'hall West from Western end',
                      tacodevice = '//%s/frm2/smc10/pos' % (nethost, ),
                      tacotimeout = 0.5,
                      pollinterval = 5,
                      maxage = 30,
                      unit = 'm'
                     ),
)
