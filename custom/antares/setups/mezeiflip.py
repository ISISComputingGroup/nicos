description = 'Mezei spin flipper using Lambda Genesys power supply'
group = 'optional'

devices = dict(
    dct1 = device('devices.taco.CurrentSupply',
                  tacodevice = '//antaressrv/antares/lambda/out1',
                  abslimits=(0, 5)),

    dct2 = device('devices.taco.CurrentSupply',
                  tacodevice = '//antaressrv/antares/lambda/out2',
                  abslimits=(0, 5)),

    flip = device('mira.flipper.Flipper',
                  description = 'Mezei flipper before sample (in shielding table)',
                  flip = 'dct1',
                  corr = 'dct2'),

)
