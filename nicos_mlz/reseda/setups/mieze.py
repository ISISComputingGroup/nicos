#  -*- coding: utf-8 -*-

description = 'RESEDA MIEZE setup'
group = 'basic'
includes = [
    'reseda', 'det_cascade', 'arm_0', 'armcontrol',  'slits', 'attenuators',
    'slitsng', 'tuning'
]

startupcode = '''
Exp.measurementmode = 'mieze'
'''
