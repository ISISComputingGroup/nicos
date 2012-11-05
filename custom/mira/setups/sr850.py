description = 'Stanford SR-850 lock-in amplifier, for susceptibility measurements'
group = 'optional'

includes = ['base', 'ccr5']

devices = dict(
    M = device('mira.sr850.Amplifier',
               tacodevice = 'mira/network/rs3_1'),
)

startupcode = '''
SetDetectors(M)
'''
