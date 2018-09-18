# -*- coding: utf-8 -*-

description = 'Beam shutter setup'
group = 'lowlevel'
display_order = 5

excludes = ['virtual_shutter']

tango_base = 'tango://phys.kws1.frm2:10000/kws1/'
tango_base_frm2 = 'tango://ictrlfs.ictrl.frm2:10000/frm2/'

devices = dict(
    shutter_in = device('nicos.devices.tango.DigitalInput',
        tangodevice = tango_base + 'sps/shutter_read',
        lowlevel = True,
    ),
    shutter_set = device('nicos.devices.tango.DigitalOutput',
        tangodevice = tango_base + 'sps/shutter_write',
        lowlevel = True,
    ),
    shutter = device('nicos_mlz.kws1.devices.shutter.Shutter',
        description = 'shutter control',
        output = 'shutter_set',
        input = 'shutter_in',
        waittime = 1,
    ),
    nl3b_shutter = device('nicos.devices.tango.NamedDigitalInput',
        description = 'Neutron guide 3b shutter status',
        mapping = {'closed': 0,
                   'open': 1},
        tangodevice = tango_base_frm2 + 'shutter/nl3b',
        pollinterval = 60,
        maxage = 120,
    ),
    sixfold_shutter = device('nicos.devices.tango.NamedDigitalInput',
        description = 'Sixfold shutter status',
        mapping = {'closed': 0,
                   'open': 1},
        tangodevice = tango_base_frm2 + 'shutter/sixfold',
        pollinterval = 60,
        maxage = 120,
    ),
)

extended = dict(
    representative = 'shutter',
)
