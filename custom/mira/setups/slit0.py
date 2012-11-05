description = 'IPC slit after mono shielding'
group = ''

devices = dict(
    ss0bus    = device('devices.vendor.ipc.IPCModBusTCP',
                       lowlevel = True),# port='/dev/ttyS1'),

    ss0l      = device('devices.vendor.ipc.SlitAxis',
                       lowlevel = True,
                       bus = 'ss0bus',
                       addr = 74,
                       side = 2,
                       slope = 0.01251398,
                       offset = -13.8,
                       lowerbreak = 15,
                       loweroffset = -48.719,
                       upperbreak = 3843,
                       upperoffset = -0.81549032,
                       abslimits = (-100, 100)),
    ss0r      = device('devices.vendor.ipc.SlitAxis',
                       lowlevel = True,
                       bus = 'ss0bus',
                       addr = 74,
                       side = 3,
                       slope = -0.01244289,
                       offset = 15.0,
                       lowerbreak = 15,
                       loweroffset = 20.891,
                       upperbreak = 3857,
                       upperoffset = 68.9660158,
                       abslimits = (-100, 100)),
    ss0b      = device('devices.vendor.ipc.SlitAxis',
                       lowlevel = True,
                       bus = 'ss0bus',
                       addr = 74,
                       side = 0,
                       slope = -0.02491868,
                       offset = 21.0,
                       lowerbreak = 95,
                       loweroffset = 59.06625275,
                       upperbreak = 3785,
                       upperoffset = -151.01618681,
                       abslimits = (-100, 100)),
    ss0t      = device('devices.vendor.ipc.SlitAxis',
                       lowlevel = True,
                       bus = 'ss0bus',
                       addr = 74,
                       side = 1,
                       slope = 0.0249772,
                       offset = -17.0,
                       lowerbreak = 138,
                       loweroffset = 90.851156632,
                       upperbreak = 3819,
                       upperoffset = 1.08990879,
                       abslimits = (-100, 100)),

    ss0       = device('devices.generic.Slit',
                       left = 'ss0l',
                       right = 'ss0r',
                       bottom = 'ss0b',
                       top = 'ss0t',
                       opmode = 'offcentered',
                       pollinterval = 5,
                       maxage = 10),
)
