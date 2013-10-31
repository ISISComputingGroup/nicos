#  -*- coding: utf-8 -*-

name = 'setup for the poller'
group = 'special'

sysconfig = dict(
    cache = 'antareshw.antares.frm2'
)

devices = dict(
    Poller = device('services.poller.Poller',
                     description = 'Device polling service',
                     alwayspoll = ['ubahn'],
                     neverpoll = [],
                     blacklist = ['tas'],
                   ),
)
