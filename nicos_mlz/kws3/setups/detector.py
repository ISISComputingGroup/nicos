# -*- coding: utf-8 -*-

description = 'Detector motor setup'
group = 'lowlevel'
display_order = 65

excludes = ['virtual_detector']

tango_base = 'tango://phys.kws3.frm2:10000/kws3/'
s7_motor = tango_base + 's7_motor/'

devices = dict(
    beamstop = device('nicos_mlz.kws3.devices.resolution.Beamstop',
        description = 'select beamstop presets',
        moveable = 'det_beamstop_x',
        resolution = 'resolution',
        outpos = 100,
    ),
    det_x = device('nicos.devices.tango.Motor',
        description = 'detector translation X',
        tangodevice = s7_motor + 'det_x',
        unit = 'mm',
        precision = 0.01,
    ),
    det_y = device('nicos.devices.tango.Motor',
        description = 'detector translation Y',
        tangodevice = s7_motor + 'det_y',
        unit = 'cm',
        precision = 0.01,
    ),
    det_z = device('nicos.devices.tango.Motor',
        description = 'detector translation Z',
        tangodevice = s7_motor + 'det_z',
        unit = 'mm',
        precision = 0.01,
    ),
    det_beamstop_x = device('nicos.devices.tango.Motor',
        description = 'beamstop x',
        tangodevice = s7_motor + 'beamstop_x',
        unit = 'mm',
        precision = 0.5,
    ),
)

extended = dict(
    poller_cache_reader = ['resolution']
)
