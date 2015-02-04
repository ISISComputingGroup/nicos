description = 'PANDA triple-axis setup'

group = 'basic'

includes = ['system', 'sampletable', 'ana', 'detector', 'panda_s7', 'manual',
            'alias_sth', 'monofoci', 'reactor']
# monoturm is included by panda_s7

#~ modules = ['nicos.commands.tas','nicos.panda.commands']
modules = ['nicos.commands.tas']

sysconfig = dict(
    instrument = 'panda',
)

devices = dict(
    alphastorage = device('panda.guidefield.AlphaStorage',
                          description = 'Virtual device for handling \\alpha changes',
                          abslimits = (-360, 360),
                          unit = 'deg',
                          lowlevel = True,
                         ),
    panda = device('devices.tas.TAS',
                   description = 'the PANDA spectrometer',
                   instrument = 'PANDA',
                   responsible = 'Astrid Schneidewind <astrid.schneidewind@frm2.tum.de>',
                   cell = 'Sample',
                   phi = 'stt',
                   psi = 'sth',
                   mono = 'mono',
                   ana = 'ana',
                   alpha = 'alphastorage',
                   scatteringsense = (-1, 1, -1),
                   energytransferunit ='meV',
#                   countloopdelay = 0.2,
                  ),
    ki    = device('devices.tas.Wavevector',
                   description = 'incoming wavevector',
                   unit = 'A-1',
                   base = 'mono',
                   tas = 'panda',
                   scanmode = 'CKI',
                  ),
    kf    = device('devices.tas.Wavevector',
                   description = 'final wavevector',
                   unit = 'A-1',
                   base = 'ana',
                   tas = 'panda',
                   scanmode = 'CKF',
                  ),
    Ei       = device('devices.tas.Energy',
                      description = 'incoming energy',
                      unit = 'meV',
                      base = 'mono',
                      tas = 'panda',
                      scanmode = 'CKI',
                     ),

    Ef       = device('devices.tas.Energy',
                      description = 'outgoing energy',
                      unit = 'meV',
                      base = 'ana',
                      tas = 'panda',
                      scanmode = 'CKF',
                     ),
    mono  = device('devices.generic.DeviceAlias',
                   description = 'Current mono',
                   alias = 'mono_virtual_dummy',
                  ),
    mono_virtual_dummy = device('devices.tas.Monochromator',
                                description = 'Dummy mono used for bootstrapping',
                                unit = 'A-1',
                                theta = 'mth',
                                twotheta = 'mtt',
                                reltheta = True,
                                focush = None,
                                focusv = None,
                                hfocuspars = [0],
                                vfocuspars = [0],
                                abslimits = (1, 10),
                                dvalue = 3.355,
                                scatteringsense = -1,
                                fixed = 'DO NOT USE THIS DUMMY DEVICE! please set mono.alias to another device.',
                                fixedby = ('NICOS', 99),
                                lowlevel = True,
                               ),
    ana  = device('devices.generic.DeviceAlias',
                  description = 'Current ana',
                  devclass = 'devices.tas.Monochromator',
                  alias = 'ana_pg',
                  loglevel = 'debug',
                 ),
    ana_pg   = device('devices.tas.Monochromator',
                      description = 'PG analyser (default)',
                      unit = 'A-1',
                      theta = 'ath',
                      twotheta = 'att',
                      focush = 'afh_pg',
                      focusv = None,
                      abslimits = (1, 10),
                      hfocuspars = [44.8615, 4.64632, 2.22023],
                      dvalue = 3.355,
                      scatteringsense = -1,
                     ),
    sth  = device('devices.generic.DeviceAlias',
                  description = 'Current sample rotation device',
                  alias = 'sth_virtual_dummy',
                 ),
    sth_virtual_dummy = device('devices.generic.VirtualMotor',
                               unit = 'deg',
                               abslimits = (0, 360),
                               userlimits = (5, 355),
                               description = 'Virtual device to startup the TAS-Device, DONT USE !',
                               fixed = 'DO NOT USE THIS DUMMY DEVICE! please set sth.alias to another device.',
                               fixedby = ('NICOS', 99),
                               lowlevel = True,
                              ),
)

startupcode = '''
from nicos import session
from nicos.core import SIMULATION
if session.mode == SIMULATION:
    AddSetup('mono_pg')
else:
    _mymono = focibox.read(0)
    printinfo('detected mono is: %s, trying to load it' % _mymono)
    if _mymono == 'PG':
        AddSetup('mono_pg')
    elif _mymono == 'Si':
        AddSetup('mono_si')
    elif _mymono == 'Cu':
        AddSetup('mono_cu')
    elif _mymono == 'Heusler':
        AddSetup('mono_heusler')
    else:
        printerror('Wrong or no Mono on table!')
    del _mymono # clean up namespace
'''
