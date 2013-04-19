description = 'base setup for all instrument configurations'
group = 'lowlevel'

includes = ['system', 'slits', 'sample', 'nl6', 'fak40', 'reactor']

devices = dict(
    MonoToni = device('mira.toni.ModBus',
                      tacodevice = 'mira/rs232/monotoni',
                      lowlevel = True),

    atten1   = device('mira.toni.Valve',
                      bus = 'MonoToni',
                      addr = 241,
                      channel = 6,
                      states = ['out', 'in'],
                      warnlimits = ('out', 'out')),
    atten2   = device('mira.toni.Valve',
                      bus = 'MonoToni',
                      addr = 241,
                      channel = 7,
                      states = ['out', 'in'],
                      warnlimits = ('out', 'out')),
    lamfilter = device('mira.toni.Valve',
                       bus = 'MonoToni',
                       addr = 241,
                       channel = 4,
                       states = ['in', 'out'],
                       warnlimits = ('in', 'in')),
    FOL       = device('mira.toni.Valve',
                       bus = 'MonoToni',
                       addr = 241,
                       channel = 0,
                       states = ['out', 'in']),
    flip1     = device('mira.toni.Valve',
                       bus = 'MonoToni',
                       addr = 241,
                       channel = 3,
                       states = ['out', 'in']),
    flip2     = device('mira.toni.Valve',
                       bus = 'MonoToni',
                       addr = 241,
                       channel = 3,
                       states = ['in', 'out']),
    ms2pos    = device('mira.toni.Valve',
                       bus = 'MonoToni',
                       addr = 241,
                       channel = 5,
                       states = ['out', 'in'],
                       warnlimits = ('in', 'in')),

    Shutter   = device('mira.shutter.Shutter',
                       tacodevice = 'mira/io/shutteropen',
                       pollinterval = 1,
                       output = 'mira/io/closeshutter',
                       mapping = {'closed': 0, 'open': 1},
                       warnlimits = ('open', 'open')),

    Cooling   = device('devices.taco.NamedDigitalInput',
                       mapping = {'refill': 0, 'okay': 1},
                       warnlimits = ('okay', 'okay'),
                       pollinterval = 10,
                       maxage = 30,
                       tacodevice = 'mira/io/cooling'),
    CoolTemp  = device('devices.taco.AnalogInput',
                       tacodevice = 'mira/i7000/coolingtemp',
                       warnlimits = (10, 30),
                       pollinterval = 10,
                       maxage = 30),

    UBahn     = device('frm2.ubahn.UBahn'),

    # LeckToni  = device('mira.toni.ModBus',
    #                    tacodevice = 'mira/rs232/lecktoni',
    #                    lowlevel = True),

    # Leckmon   = device('mira.toni.Leckmon',
    #                    bus = 'LeckToni',
    #                    addr = 0x17,
    #                    unit = ''),
)
