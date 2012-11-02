description = 'Sample stick rotation motor'
group = 'optional'

includes = ['base']

devices = dict(
    srot   = device('devices.taco.Motor',
                    tacodevice = 'mira/newportmc/motor',
                    abslimits = (-180, 180),
                    )

)
