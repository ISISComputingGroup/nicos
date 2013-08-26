description = 'polarity reversing relays'
group = 'optional'

devices = dict(
    relay1    = device('mira.beckhoff.BeckhoffNamedDigitalOutput',
                       description = 'Polarity switchover relay 1',
                       tacodevice = '//mirasrv/mira/modbus/beckhoff',
                       startoffset = 0,
                       mapping = {'off': 0, 'on': 1}),
    relay2    = device('mira.beckhoff.BeckhoffNamedDigitalOutput',
                       description = 'Polarity switchover relay 2',
                       startoffset = 1,
                       tacodevice = '//mirasrv/mira/modbus/beckhoff',
                       mapping = {'off': 0, 'on': 1}),
)
