description = 'High temperature sample stick LakeShore 336 controller'
group = 'optional'

includes = ['alias_T']

tango_base = 'tango://mira1.mira.frm2:10000/mira/'

devices = dict(
    T_ht_stick    = device('nicos.devices.tango.TemperatureController',
                      description = 'temperature regulation',
                      tangodevice = tango_base + 'ht_stick/ctrl',
                      unit = 'K',
                     ),
    T_ht_stick_A  = device('nicos.devices.tango.Sensor',
                      description = 'sensor A',
                      tangodevice = tango_base + 'ht_stick/sensora',
                      unit = 'K',
                     ),
    T_ht_stick_B  = device('nicos.devices.tango.Sensor',
                      description = 'sensor B',
                      tangodevice = tango_base + 'ht_stick/sensorb',
                      unit = 'K',
                     ),
    T_ht_stick_C  = device('nicos.devices.tango.Sensor',
                      description = 'sensor C',
                      tangodevice = tango_base + 'ht_stick/sensorc',
                      unit = 'K',
                     ),
    T_ht_stick_D  = device('nicos.devices.tango.Sensor',
                      description = 'sensor D',
                      tangodevice = tango_base + 'ht_stick/sensord',
                      unit = 'K',
                     ),
)

alias_config = {
    'T': {'T_ht_stick': 180},  # lower than default T_ccr5
    'Ts': {'T_ht_stick_B': 60, 'T_ht_stick_D' : 50},
}
