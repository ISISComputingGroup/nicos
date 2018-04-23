description = 'FRM II 5.5 T superconducting magnet'

group = 'plugplay'

includes = ['alias_B', 'alias_sth']

# setupname is set by nicos before loading this file
# setupname = filename - '.py' extension
nethost = setupname


devices = {
    'B_%s' % setupname: device('nicos.devices.taco.CurrentSupply',
        description = 'The magnetic field',
        tacodevice = '//%s/magnet/smc120/t' % nethost,
        abslimits = (-5.555, 5.555),
    ),
    'sth_%s' % setupname: device('nicos.devices.taco.Axis',
        description = 'Cryotstat tube rotation',
        tacodevice = '//%s/magnet/axis/tube' % nethost,
        abslimits = (-180, 180),
    ),
}

# Maximum temeratures for field operation above 80A (6.6T) taken from the manual
maxtemps = [None, 4.3, 4.3, 5.1, 4.7, None, None, None, 4.3]

for i in range(1, 9):
    dev = device('nicos.devices.taco.TemperatureSensor',
        description = '5.5T magnet temperature sensor %d' % i,
        tacodevice = '//%s/magnet/ls218/sens%d' % (nethost, i),
        warnlimits = (0, maxtemps[i]),
        pollinterval = 30,
        maxage = 90,
        unit = 'K',
    )
    devices['%s_T%d' % (setupname, i)] = dev

alias_config = {
    'B':   {'B_%s' % setupname: 100},
    'sth': {'sth_%s' % setupname: 100},
}

extended = dict(
    representative = 'B_%s' % setupname,
)
