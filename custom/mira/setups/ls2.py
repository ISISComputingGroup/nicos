description = 'LakeShore 340 cryo controller'
group = 'optional'

includes = ['alias_T']

tango_url = 'tango://mira1.mira.frm2:10000/mira/'

devices = dict(
    T_ls2    = device('devices.tango.TemperatureController',
                      description = 'temperature regulation',
                      tangodevice = tango_url + 'ls2/ls_control1',
                      pollinterval = 0.7,
                      maxage = 2,
                      abslimits = (0, 350),
                     ),
    T_ls2_A  = device('devices.tango.Sensor',
                      description = 'sensor A',
                      tangodevice = tango_url + 'ls2/ls_sensor1',
                      pollinterval = 0.7,
                      maxage = 2,
                     ),
    T_ls2_B  = device('devices.tango.Sensor',
                      description = 'sensor B',
                      tangodevice = tango_url + 'ls2/ls_sensor2',
                      pollinterval = 0.7,
                      maxage = 2,
                     ),
)

startupcode = '''
T.alias = T_ls2
Ts.alias = T_ls2_A
'''
