description = 'polarity reversing relays'
group = 'optional'

devices = dict(
    relay1    = device('mira.beckhoff.BeckhoffNamedDigitalOutput',
                       tacodevice = 'mira/modbus/beckhoff',
                       startoffset = 64,
                       mapping = {'off': 0, 'on': 1}),
    relay2    = device('mira.beckhoff.BeckhoffNamedDigitalOutput',
                       startoffset = 65,
                       tacodevice = 'mira/modbus/beckhoff',
                       mapping = {'off': 0, 'on': 1}),
)
