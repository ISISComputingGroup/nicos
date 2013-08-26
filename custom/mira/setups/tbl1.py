description = 'Huber rotation tables'

group = 'optional'

devices = dict(
    tbl1    = device('devices.taco.Motor',
                       description = 'First general-use rotator table',
                       tacodevice = '//mirasrv/mira/rot/tbl1',
                       abslimits = (-360, 360),
                       resetcall = 'deviceReset'),
)
