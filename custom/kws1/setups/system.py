# -*- coding: utf-8 -*-

description = 'system setup'
group = 'lowlevel'
display_order = 80

sysconfig = dict(
    cache = 'localhost',
    instrument = 'KWS1',
    experiment = 'Exp',
    datasinks = ['conssink', 'filesink', 'daemonsink'],
    notifiers = ['email'],
)

includes = ['notifiers']

modules = ['commands.standard']

devices = dict(
    KWS1     = device('devices.instrument.Instrument',
                      description = 'KWS-1 instrument',
                      instrument = 'KWS-1',
                      doi = 'http://dx.doi.org/10.17815/jlsrf-1-26',
                      responsible = 'H. Frielinghaus <h.frielinghaus@fz-juelich.de>',
                     ),

    Sample   = device('kws1.sample.KWSSample',
                      description = 'Sample object',
                     ),

    Exp      = device('devices.experiment.Experiment',
                      description = 'experiment object',
                      dataroot = '/data',
                      sendmail = True,
                      serviceexp = '0',
                      sample = 'Sample',
                     ),

    filesink = device('devices.datasinks.AsciiScanfileSink',
                      lowlevel = True,
                     ),

    conssink = device('devices.datasinks.ConsoleScanSink',
                      lowlevel = True,
                     ),

    daemonsink = device('devices.datasinks.DaemonSink',
                        lowlevel = True,
                       ),

    Space    = device('devices.generic.FreeSpace',
                      description = 'The amount of free space for storing data',
                      path = None,
                      minfree = 5,
                     ),
)
