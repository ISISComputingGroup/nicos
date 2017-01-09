# -*- coding: utf-8 -*-

description = "Polarizer setup"
group = "lowlevel"
display_order = 60

excludes = ['virtual_polarizer']

tango_base = "tango://phys.kws2.frm2:10000/kws2/"

devices = dict(
    polarizer = device('kws2.polarizer.Polarizer',
                       description = 'high-level polarizer switcher',
                       input_in = 'pol_in',
                       input_out = 'pol_out',
                       output = 'pol_set',
                       flipper = 'flipper',
                       timeout = 60,
                      ),

    pol_set   = device('devices.tango.DigitalOutput',
                       tangodevice = tango_base + 'fzjdp_digital/pol_write',
                       fmtstr = '%#x',
                       lowlevel = True,
                      ),
    pol_in    = device('devices.tango.DigitalInput',
                       tangodevice = tango_base + 'fzjdp_digital/pol_in',
                       fmtstr = '%#x',
                       lowlevel = True,
                      ),
    pol_out   = device('devices.tango.DigitalInput',
                       tangodevice = tango_base + 'fzjdp_digital/pol_out',
                       fmtstr = '%#x',
                       lowlevel = True,
                      ),

    flipper   = device('devices.generic.ManualSwitch',
                       description = '3He spin flipper (currently virtual)',
                       states = ['up', 'down'],
                      ),
)
