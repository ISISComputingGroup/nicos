description = 'PANDA PG-monochromator'

group = 'lowlevel'

includes = []

modules = []

excludes = ['mono_si', 'mono_cu', 'mono_heusler']

extended = dict( dynamic_loaded = True)

devices = dict(
    mono_pg     = device('devices.tas.Monochromator',
                         description = 'PG Monochromator of PANDA',
                         unit = 'A-1',
                         theta = 'mth',
                         twotheta = 'mtt',
                         reltheta = True,
                         focush = 'mfh_pg',
                         focusv = 'mfv_pg',
                         hfocuspars = [29.188, -1.1611, 0.6019],
                         hfocusflat = 343.9,
                         vfocuspars = [557.79, -215.59, 66.843, -9.6554, 0.5228],
                         vfocusflat = 17.3,
                         abslimits = (1, 10),
                         dvalue = 3.355,
                         scatteringsense = -1,
                        ),
    mfh_pg_step = device('panda.mcc2.MCC2Motor',
                         description = 'horizontal focusing MOTOR of PG monochromator',
                         bus = 'focimotorbus',
                         mccmovement = 'linear',
                         precision = 0.01,
                         fmtstr = '%.3f',
                         channel = 'X',
                         addr = 0,
                         slope = 900*24/360., # 900:1 gear, 24 steps per rev, 360deg per rev
                         abslimits = (-400,400),
                         userlimits = (-360,360),
                         unit = 'deg',
                         idlecurrent = 0.1,
                         movecurrent = 0.2,
                         rampcurrent = 0.25,
                         microstep = 16,
                         # speed = 1.5,
                         speed = 5,
                         accel = 50,
                         lowlevel = True,
                        ),
    mfh_pg      = device('panda.rot_axis.RotAxis',
                         description = 'horizontal focus of PG monochromator',
                         motor = 'mfh_pg_step',
                         coder = 'mfh_pg_step',
                         obs = [],
                         precision = 1,
                         refpos = 208.75,
                         refspeed = 1.5,
                         autoref = -10, # autoref every 10 full turns
                        ),
    mfv_pg_step = device('panda.mcc2.MCC2Motor',
                         description = 'vertical focusing MOTOR of PG monochromator',
                         bus = 'focimotorbus',
                         mccmovement = 'linear',
                         precision = 0.01,
                         fmtstr = '%.3f',
                         channel = 'Y',
                         addr = 0,
                         slope = 900*24/360., # 900:1 gear, 24 steps per rev, 360deg per rev
                         abslimits = (-400,400),
                         userlimits = (-360,360),
                         unit = 'deg',
                         idlecurrent = 0.1,
                         movecurrent = 0.2,
                         rampcurrent = 0.25,
                         microstep = 16,
                         speed = 5,
                         accel = 50,
                         lowlevel = True,
                        ),
    mfv_pg      = device('panda.rot_axis.RotAxis',
                         description = 'vertical focus of PG monochromator',
                         motor = 'mfv_pg_step',
                         coder = 'mfv_pg_step',
                         obs = [],
                         precision = 1,
                         refpos = 221.3,
                         refspeed = 1.5,
                         autoref = -10, # autoref every 10 full turns
                        ),
)

startupcode = """
try:
    _=(ana, mono, mfv, mfh, focibox)
except NameError, e:
    printerror("The requested setup 'panda' is not fully loaded!")
    raise NameError('One of the required devices is not loaded : %s, please check!' % e)

if focibox.read(0) == 'PG':
    from nicos import session
    mfh.alias = session.getDevice('mfh_pg')
    mfv.alias = session.getDevice('mfv_pg')
    mono.alias = session.getDevice('mono_pg')
    ana.alias = session.getDevice('ana_pg')
    mfh.motor._pushParams() # forcibly send parameters to HW
    mfv.motor._pushParams() # forcibly send parameters to HW
    focibox.comm('XMA', forcechannel=False) # enable output for mfh
    focibox.comm('YMA', forcechannel=False) # enable output for mfv
    focibox.driverenable = True
    #maw(mtx, 0) #correct center of rotation for Si-mono only
    del session
else:
    printerror('WRONG MONO ON TABLE FOR SETUP mono_pg !!!')
"""
