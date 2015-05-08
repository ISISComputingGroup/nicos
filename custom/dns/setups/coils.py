# -*- coding: utf-8 -*-

__author__  = "Christian Felder <c.felder@fz-juelich.de>"


description = "Coil setup"
group = "optional"

tango_host = 'tango://phys.dns.frm2:10000'
_PS_URL = tango_host + '/dns/toellner/%s'
_DIO_URL = tango_host + '/dns/FZJDP_Digital/%s'
_POLCHANGE = {"+": 0, "-": 1}

##
# magnetic field definitions on 13-03-2015/20-03-2015
off     = (0, 0, 0, 0, 0, (0, 0), "off")
zero    = (0, .15, -.50, -2.15, -2.15, (0.0, 0.0), "off")
# fields with spin flipper
x7_sf   = (-0.5, -1.5, -1.20, -2.15, -2.15, (1.0,0.25), "on")
# x7_old: (0.94,0.40)
mx7_sf  = (0, 2.30, -0.35, -2.15, -2.15, (1.05, 0.38), "on")
y7_sf   = (-0.3, 2.0, -2.95, -2.15, -2.15, (1.0,0.32), "on")
# y7_old: (0.945,0.31)/(0.98,0.32)
# was (1.0,0.15) before 20.05.15; changed to (1.0,0.32) on 20.05.15
my7_sf  = (0, -1.40, 1.65, -2.15, -2.15, (0.98, 0.38), "on")
z7_sf   = (0, .15, -.50, 0.0, 0.0, (1.0,0.20), "on")
# z7_old: (0.94,0.35)
mz7_sf  = (0, .15, -.50, -4.3, -4.3, (1.00, 0.20), "on")
z7_high_sf   = (0, .15, -.50, 5.0, 5.0, (1.0,0.15), "on")
#old ZB=ZT=4A
# fields without spin flipper
x7_nsf  = x7_sf[:6] + ("off", )
mx7_nsf = mx7_sf[:6] + ("off", )
y7_nsf  = y7_sf[:6] + ("off", )
my7_nsf = my7_sf[:6] + ("off", )
z7_nsf  = z7_sf[:6] + ("off", )
mz7_nsf = mz7_sf[:6] + ("off", )
z7_high_nsf = z7_high_sf[:6] + ('off',)


devices = dict(
    flipper       = device('devices.polarized.flipper.MezeiFlipper',
                           description = 'Neutron spin flipper',
                           flip = "Fi",
                           corr = "Co",
                          ),
    flip_currents = device('devices.generic.ParamDevice',
                           description = 'Helper device for setting the'
                                         'currents on the flipper device as a '
                                         'moveable',
                           device = 'flipper',
                           parameter = 'currents',
                           unit = 'A',
                           lowlevel = True,
                          ),
    polch_Fi = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for Flipper Field',
                      tangodevice = _DIO_URL % 'Polum1',
                      mapping = _POLCHANGE,
                      lowlevel = True
                     ),
# Devices for toellner must be changed with new names from database
    Fi       = device('dns.toellner.Toellner',
                      description = 'Flipper Field',
                      tangodevice = _PS_URL % 'fi',
                      abslimits = (-3.2, 3.2),
                      polchange = 'polch_Fi',
                     ),
    polch_Co = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for Flipper Compensation',
                      tangodevice = _DIO_URL % 'Polum2',
                      mapping = _POLCHANGE,
                      lowlevel = True
                     ),
    Co       = device('dns.toellner.Toellner',
                      description = 'Flipper Compensation Field',
                      tangodevice = _PS_URL % 'co',
                      abslimits = (-3.2, 3.2),
                      polchange = 'polch_Co',
                     ),
    A        = device('dns.toellner.Toellner',
                      description = 'Coil A',
                      tangodevice = _PS_URL % 'a',
                      abslimits = (-3.2, 3.2),
                      polchange = 'polch_A',
                     ),
    polch_A  = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for coil A',
                      tangodevice = _DIO_URL % 'Polum3',
                      mapping = _POLCHANGE,
                      lowlevel = True,
                     ),
    B        = device('dns.toellner.Toellner',
                      description = 'Coil B',
                      tangodevice = _PS_URL % 'b',
                      abslimits = (-3.2, 3.2),
                      polchange = 'polch_B',
                     ),
    polch_B  = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for coil B',
                      tangodevice = _DIO_URL % 'Polum4',
                      mapping = _POLCHANGE,
                      lowlevel = True,
                     ),
    ZB       = device('dns.toellner.Toellner',
                      description = 'Coil-Z Bottom',
                      tangodevice = _PS_URL % 'zb',
                      abslimits = (-5, 5),
                      polchange = 'polch_ZB',
                     ),
    polch_ZB = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for coil Z Bottom',
                      tangodevice = _DIO_URL % 'Polum5',
                      mapping = _POLCHANGE,
                      lowlevel = True,
                     ),
    ZT       = device('dns.toellner.Toellner',
                      description = 'Coil-Z Top',
                      tangodevice = _PS_URL % 'zt',
                      abslimits = (-5, 5),
                      polchange = 'polch_ZT',
                     ),
    polch_ZT = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for coil Z Top',
                      tangodevice = _DIO_URL % 'Polum6',
                      mapping = _POLCHANGE,
                      lowlevel = True,
                     ),
    C        = device('dns.toellner.Toellner',
                      description = 'Coil C',
                      tangodevice = _PS_URL % 'c',
                      abslimits = (-3.2, 3.2),
                      polchange = 'polch_C',
                     ),
    polch_C  = device('devices.tango.NamedDigitalOutput',
                      description = 'Polarity changer for coil C',
                      tangodevice = _DIO_URL % 'Polum7',
                      mapping = _POLCHANGE,
                      lowlevel = True,
                     ),
    field    = device('devices.generic.MultiSwitcher',
                      description = 'Guide field switcher',
                      moveables = ["A", "B", "C", "ZB", "ZT",
                                   "flip_currents", "flipper"],
                      mapping = {
                          "off": off,
                          "zero field": zero,
                          "x7_sf": x7_sf,
                          "-x7_sf": mx7_sf,
                          "y7_sf": y7_sf,
                          "-y7_sf": my7_sf,
                          "z7_sf": z7_sf,
                          "-z7_sf": mz7_sf,
                          "x7_nsf": x7_nsf,
                          "-x7_nsf": mx7_nsf,
                          "y7_nsf": y7_nsf,
                          "-y7_nsf": my7_nsf,
                          "z7_nsf": z7_nsf,
                          "-z7_nsf": mz7_nsf,
                          "z7_high_sf": z7_high_sf,
                          "z7_high_nsf": z7_high_nsf,
                      },
                      precision = [.1, .1, .1, .1, .1, 0, 0],
                     ),
)

startupcode = '''
'''
