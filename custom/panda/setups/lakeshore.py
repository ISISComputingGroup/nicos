description = 'LakeShore 340 cryo controller'

includes = ['alias_T']

devices = dict(
    T_ls340   = device('devices.taco.TemperatureController',
                      tacodevice = 'panda/ls340/control',
                      #~ sensor_A = 'T_ls340_A',
                      #~ sensor_B = 'T_ls340_B',
                      #~ sensor_C = 'T_ls340_C',
                      #~ sensor_D = 'T_ls340_D',
                      maxage = 2,
                      abslimits = (0, 300)),
    T_ls340_A = device('devices.taco.TemperatureSensor',
                      tacodevice = 'panda/ls340/sensora',
                      maxage = 2),
    T_ls340_B = device('devices.taco.TemperatureSensor',
                      tacodevice = 'panda/ls340/sensorb',
                      maxage = 2),
    T_ls340_C = device('devices.taco.TemperatureSensor',
                      tacodevice = 'panda/ls340/sensorc',
                      maxage = 2),
    T_ls340_D = device('devices.taco.TemperatureSensor',
                      tacodevice = 'panda/ls340/sensord',
                      maxage = 2),


    #~ cc_compressor_wut = device('panda.wechsler.Beckhoff',
                #~ host='compressor.panda.frm2',
                #~ description='WUT-IO device to switch compressors on/off',
                #~ addr=1,
                #~ lowlevel=True,
                #~ ),
    #~ cc_compressor_switch = device('panda.satbox.SatBox',
                #~ bus='cc_compressor_wut',
                #~ description='Temporary HACK to switch CC-compressor on (1) or off(0)',
                #~ widths=[1],
                #~ fmtstr='%d',
                #~ unit='mm'),

)

startupcode = '''
T.alias='T_ls340'
Ts.alias='T_ls340_B'
'''
