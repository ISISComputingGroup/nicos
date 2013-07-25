description = 'NICOS system setup'

sysconfig = dict(
    cache = 'localhost',
    instrument = 'SE',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['emailer', 'smser'],
)

modules = ['nicos.commands.standard']

devices = dict(
    SE   = device('devices.instrument.Instrument',
                      instrument = 'SE'),

    Sample   = device('devices.experiment.Sample'),

    Exp      = device('devices.experiment.Experiment',
                      localcontact = 'Harald Schneider <ha.schneider@fz-juelich.de>,' \
                                     ' Juergen Peters <juergen.peters@frm2.tum.de>',
                      dataroot = '/data',
                      sample = 'Sample',
                      elog = False),

    filesink = device('devices.datasinks.AsciiDatafileSink'),

    conssink = device('devices.datasinks.ConsoleSink'),

    daemonsink = device('devices.datasinks.DaemonSink'),

    emailer  = device('devices.notifiers.Mailer',
                      sender = 'se-trouble@frm2.tum.de',
                      copies = [],
                      subject = 'SE'),

    smser    = device('devices.notifiers.SMSer',
                      server = 'triton.admin.frm2'),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The free space on the data storage',
                      path = '/data',
                      minfree = 5,
                     ),
)
