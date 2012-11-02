description = 'PUMA attenuator'

includes = ['motorbus8']

devices = dict(
    att_sw    = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 104,
                       first = 0,
                       last = 9,
                       lowlevel = True,
                       ),
    att_press = device('devices.vendor.ipc.Input',
                       bus = 'motorbus8',
                       addr = 103,
                       first = 13,
                       last = 13,
                       lowlevel = True,
                       ),
    att_set   = device('devices.vendor.ipc.Output',
                       bus = 'motorbus8',
                       addr = 114,
                       first = 3,
                       last = 7,
                       lowlevel = True,
                       ),

    atn       = device('puma.attenuator.Attenuator',
                       io_status = 'att_sw',
                       io_set = 'att_set',
                       io_press = 'att_press',
                       abslimits = (0, 38),
                       unit = 'mm',
                       ),
)

