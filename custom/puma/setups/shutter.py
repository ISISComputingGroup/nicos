#  -*- coding: utf-8 -*-

description = 'PUMA shutters'

includes = ['system', 'motorbus8']

devices = dict(
    sr7_cl    = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 115,
                       first = 1,
                       last = 1,
                       lowlevel = True,
                       ),
    sr7_p1    = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 106,
                       first = 8,
                       last = 8,
                       lowlevel = True,
                       ),
    sr7_p2    = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 106,
                       first = 9,
                       last = 9,
                       lowlevel = True,
                       ),
    sr7_p3    = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 106,
                       first = 10,
                       last = 10,
                       lowlevel = True,
                       ),
    sh_oc     = device('devices.vendor.ipc.Output',
                       bus = 'motorbus8',
                       addr = 115,
                       first = 2,
                       last = 2,
                       lowlevel = True,
                       ),
    sr7_sv    = device('devices.vendor.ipc.Output',
                       bus = 'motorbus8',
                       addr = 106,
                       first = 11,
                       last = 11,
                       lowlevel = True,
                       ),

    SR7       = device('puma.sr7.SR7Shutter',
                       sr7cl = 'sr7_cl',
                       sr7p1 = 'sr7_p1',
                       sr7p2 = 'sr7_p2',
                       sr7p3 = 'sr7_p3',
                       sr7set = 'sh_oc',
                       ),
)
