description = 'Large sample manipulation stage using servostar controller'
group = 'optional'

devices = dict(
    stx_servostar = device('antares.servostar.ServoStarMotor',
                           description = 'Sample Translation X',
                           tacodevice = 'antares/mani/x',
                           pollinterval = 5,
                           maxage = 12,
                           precision = 0.01,
                           userlimits = (0, 1010),
                           abslimits = (0, 1010),
                          ),
    sty_servostar = device('antares.servostar.ServoStarMotor',
                           description = 'Sample Translation Y',
                           tacodevice = 'antares/mani/y',
                           pollinterval = 5,
                           precision = 0.01,
                           maxage = 12,
                           userlimits = (0, 580),
                           abslimits = (0, 580),
                          ),
    sry_servostar = device('antares.servostar.ServoStarMotor',
                           description = 'Sample Rotation around Y',
                           tacodevice = 'antares/mani/phi',
                           pollinterval = 5,
                           maxage = 12,
                           precision = 0.01,
                           abslimits = (-9999, 9999),
                           userlimits = (-9999, 9999),
                          ),
)

startupcode = '''
'''
