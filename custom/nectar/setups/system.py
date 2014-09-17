description = 'system setup'

group = 'lowlevel'

sysconfig = dict(
    cache = 'nectarctrl.nectar.frm2',
    instrument = None,
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['email', 'smser'],
)

modules = ['nicos.commands.basic', 'nicos.commands.standard', 'antares.commands']

devices = dict(
    Sample   = device('devices.sample.Sample'),

    Exp      = device('antares.experiment.Experiment',
                      dataroot = '/data',
                      sendmail = True,
                      serviceexp = '0',
                      sample = 'Sample',
                     ),

    Instrument = device('devices.instrument.Instrument',
                        description = 'NECTAR instrument',
                        instrument = 'NECTAR',
                        responsible = 'Dr. Stefan Soellradl',
                       ),

    filesink = device('devices.datasinks.AsciiDatafileSink'),

    conssink = device('devices.datasinks.ConsoleSink'),

    daemonsink = device('devices.datasinks.DaemonSink'),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      path = None,
                      minfree = 5,
                     ),

    # Configure source and copy addresses to an existing address.
    email    = device('devices.notifiers.Mailer',
                      sender = 'nectar@frm2.tum.de',
                      copies = ['stefan.soellradl@frm2.tum.de'],
                      subject = '[NICOS]',
                     ),

    # Configure SMS receivers if wanted and registered with IT.
    smser    = device('devices.notifiers.SMSer',
                      server = 'triton.admin.frm2',
                      receivers = [],
                     ),
)
