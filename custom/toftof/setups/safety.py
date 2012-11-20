description = 'safety system and shutter'
includes = ['system']

nethost = 'toftofsrv'

devices = dict(
    saf      = device('toftof.safety.SafetyInputs',
                      i7053_1 = 'i7053_1',
                      i7053_2 = 'i7053_2',
                      i7053_3 = 'i7053_3'),
    i7053_1  = device('devices.taco.DigitalInput',
                      lowlevel = True,
                      tacodevice = '//%s/toftof/sec/70531' % (nethost,)),
    i7053_2  = device('devices.taco.DigitalInput',
                      lowlevel = True,
                      tacodevice = '//%s/toftof/sec/70532' % (nethost,)),
    i7053_3  = device('devices.taco.DigitalInput',
                      lowlevel = True,
                      tacodevice = '//%s/toftof/sec/70533' % (nethost,)),

    shopen   = device('devices.taco.io.DigitalOutput',
                      tacodevice = '//%s/toftof/shutter/open' % (nethost,),
                      lowlevel = True),
    shclose  = device('devices.taco.io.DigitalOutput',
                      tacodevice = '//%s/toftof/shutter/close' % (nethost,),
                      lowlevel = True),
    shstatus = device('devices.taco.io.DigitalOutput',
                      tacodevice = '//%s/toftof/shutter/status' % (nethost,),
                      lowlevel = True),
    shutter  = device('toftof.safety.Shutter',
                      open = 'shopen',
                      close = 'shclose',
                      status = 'shstatus',
                      unit = ''),
)
