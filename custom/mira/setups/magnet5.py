# SANS magnet 5 T

description = 'SANS-1 5 T magnet'

includes = ['alias_B']

devices = dict(
    B_m5T  = device('sans1.mercury.MercuryAsymmetricalMagnet',
                     description = 'The magnetic field',
                     ps1 = 'm5T_PS1',
                     ps2 = 'm5T_PS2',
                     abslimits = (-5, 5),
                     maxage = 45,
                     pollinterval = 30),
    m5T_PS1 = device('sans1.mercury.OxfordMercury',
                     unit = 'A',
                     tacodevice = '//mirasrv/mira/network/ips1',
                     abslimits = (-161, 161),
                     pollinterval = None),
    m5T_PS2 = device('sans1.mercury.OxfordMercury',
                     unit = 'A',
                     tacodevice = '//mirasrv/mira/network/ips2',
                     abslimits = (-130, 130),
                     pollinterval = None),

#    m5T_T1  = device('taco.TemperatureSensor',
 #                    tacodevice = '//mirasrv/mira/ls218/s1',
 #                    pollinterval = 30),
    m5T_T2  = device('devices.taco.TemperatureSensor',
                     tacodevice = '//mirasrv/mira/ls218/s2',
                     warnlimits = (0, 4.4),
                     maxage = 45,
                     pollinterval = 30),
    m5T_T3  = device('devices.taco.TemperatureSensor',
                     tacodevice = '//mirasrv/mira/ls218/s3',
                     warnlimits = (0, 4.4),
                     maxage = 45,
                     pollinterval = 30),
    m5T_T4  = device('devices.taco.TemperatureSensor',
                     tacodevice = '//mirasrv/mira/ls218/s4',
                     warnlimits = (0, 4.4),
                     maxage = 45,
                     pollinterval = 30),
    m5T_T5  = device('devices.taco.TemperatureSensor',
                     tacodevice = '//mirasrv/mira/ls218/s5',
                     warnlimits = (0, 4.4),
                     maxage = 45,
                     pollinterval = 30),
    m5T_T6  = device('devices.taco.TemperatureSensor',
                     tacodevice = '//mirasrv/mira/ls218/s6',
                     warnlimits = (0, 4.4),
                     maxage = 45,
                     pollinterval = 30),


)
