# -*- coding: utf-8 -*-

description = 'Spodi neutron guide'

group = 'lowlevel'

includes = []

devices = dict(
    p1_nguide = device('nicos.devices.generic.VirtualMotor',
        description = 'Pressure 1',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        unit = 'mbar',
        abslimits = (0, 1000),
        curvalue = 991,
    ),
    p2_nguide = device('nicos.devices.generic.VirtualMotor',
        description = 'Pressure 2',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        unit = 'mbar',
        abslimits = (0, 1000),
        curvalue = 993,
    ),
    p3_nguide = device('nicos.devices.generic.VirtualMotor',
        description = 'Pressure 3',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        unit = 'mbar',
        abslimits = (0, 1000),
        curvalue = 963,
    ),
    o2_nguide = device('nicos.devices.generic.VirtualMotor',
        description = 'O2',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        unit = '%% O2',
        abslimits = (0, 100),
        curvalue = 0.2,
    ),
    o2part_nguide = device('nicos.devices.generic.VirtualMotor',
        description = 'O2 part',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        curvalue = 2,
        unit = 'hPa',
        abslimits = (0, 20),
    ),
    T_nguide = device('nicos.devices.generic.VirtualTemperature',
        description = 'Temperature',
        fmtstr = '%.2f',
        maxage = 65,
        pollinterval = 30,
        abslimits = (10, 35),
        unit = 'degC',
    ),
)

display_order = 100
startupcode = '''
'''
