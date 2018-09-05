description = 'vacuum system monitoring'

group = 'lowlevel'

tango_base = 'tango://phys.kws2.frm2:10000/kws2/'

devices = dict(
    pressure_p20 = device('nicos.devices.tango.Sensor',
        description = 'pressure at pump 21',
        tangodevice = tango_base + 'sps/pressure_p20',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p21 = device('nicos.devices.tango.Sensor',
        description = 'pressure in collimation chamber',
        tangodevice = tango_base + 'sps/pressure_p21',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p22 = device('nicos.devices.tango.Sensor',
        description = 'pressure in sample chamber',
        tangodevice = tango_base + 'sps/pressure_p22',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p23 = device('nicos.devices.tango.Sensor',
        description = 'pressure in detector tube',
        tangodevice = tango_base + 'sps/pressure_p23',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p24 = device('nicos.devices.tango.Sensor',
        description = 'pressure in KWS2 connection to Pfeiffer pump',
        tangodevice = tango_base + 'sps/pressure_p24',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p25 = device('nicos.devices.tango.Sensor',
        description = 'pressure in lens chamber',
        tangodevice = tango_base + 'sps/pressure_p25',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p26 = device('nicos.devices.tango.Sensor',
        description = 'pressure in chopper chamber',
        tangodevice = tango_base + 'sps/pressure_p26',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p14 = device('nicos.devices.tango.Sensor',
        description = 'pressure in KWS1 connection to Pfeiffer pump',
        tangodevice = tango_base + 'sps/pressure_p14',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),
    pressure_p34 = device('nicos.devices.tango.Sensor',
        description = 'pressure in SANS1 connection to Pfeiffer pump',
        tangodevice = tango_base + 'sps/pressure_p34',
        unit = 'mbar',
        fmtstr = '%.1e',
        lowlevel = True,
    ),

    lenstemp_4 = device('nicos.devices.tango.Sensor',
        description = 'lens temperature 4',
        tangodevice = tango_base + 'sps/lenstemp_4',
        unit = 'K',
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    lenstemp_5 = device('nicos.devices.tango.Sensor',
        description = 'lens temperature 5',
        tangodevice = tango_base + 'sps/lenstemp_5',
        unit = 'K',
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    lenstemp_6 = device('nicos.devices.tango.Sensor',
        description = 'lens temperature 6',
        tangodevice = tango_base + 'sps/lenstemp_6',
        unit = 'K',
        fmtstr = '%.1f',
        lowlevel = True,
    ),
    lens_compressor = device('nicos.devices.tango.NamedDigitalInput',
        description = 'lens compressor status',
        tangodevice = tango_base + 'sps/lens_compressor',
        warnlimits = ('on', 'on'),
        mapping = {'on': 1,
                   'off': 0},
        lowlevel = True,
    ),
    pump_status = device('nicos.devices.tango.DigitalInput',
        description = 'pump status',
        tangodevice = tango_base + 'sps/pump_status',
        fmtstr = '%#02x',
        lowlevel = True,
    ),
    pump_manual_mode = device('nicos.devices.tango.DigitalInput',
        description = 'pump manual mode',
        tangodevice = tango_base + 'sps/pump_manual_mode',
        fmtstr = '%#02x',
        lowlevel = True,
    ),
    pump_request_mode = device('nicos.devices.tango.DigitalInput',
        description = 'pump request mode',
        tangodevice = tango_base + 'sps/pump_request_mode',
        fmtstr = '%#02x',
        lowlevel = True,
    ),
    pump_components_1 = device('nicos.devices.tango.DigitalInput',
        description = 'pump components state',
        tangodevice = tango_base + 'sps/pump_components_1',
        fmtstr = '%#016x',
        lowlevel = True,
    ),
    pump_components_2 = device('nicos.devices.tango.DigitalInput',
        description = 'pump components state',
        tangodevice = tango_base + 'sps/pump_components_2',
        fmtstr = '%#08x',
        lowlevel = True,
    ),
    ge_interlock = device('nicos.devices.tango.DigitalInput',
        description = 'state of SPS/GE power interlock',
        tangodevice = tango_base + 'sps/ge_interlock',
        fmtstr = '%#x',
        lowlevel = True,
    ),
    ge_interlock_timeout = device('nicos.devices.tango.DigitalInput',
        description = 'timeout state of individual 8-packs',
        tangodevice = tango_base + 'sps/ge_interlock_timeout',
        fmtstr = '%#x',
        lowlevel = True,
    ),
)
