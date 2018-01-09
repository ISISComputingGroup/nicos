#  -*- coding: utf-8 -*-

description = 'Sample table (translation)'
group = 'optional'

taco_base = '//resedasrv.reseda.frm2/reseda'
tango_base = 'tango://resedahw2.reseda.frm2:10000/reseda'

devices = dict(
    srz_mot = device('nicos.devices.tango.Motor',
        description = 'Sample rotation: z (motor)',
        tangodevice = '%s/sampletable/srz' % tango_base,
        fmtstr = '%.3f',
        unit = 'deg',
        lowlevel = True,
    ),
    srz_enc = device('nicos.devices.taco.Coder',
        description = 'Sample rotation: z (encoder)',
        tacodevice = '%s/enc/probe_1' % taco_base,
        fmtstr = '%.3f',
        unit = 'deg',
        lowlevel = True,
    ),
    srz = device('nicos.devices.generic.Axis',
        description = 'Sample rotation: z',
        motor = 'srz_mot',
        coder = 'srz_enc',
        fmtstr = '%.3f',
        precision = 0.1,
    ),
    stx = device('nicos.devices.tango.Motor',
        description = 'Sample table: x',
        tangodevice = '%s/sampletable/stx' % tango_base,
        fmtstr = '%.3f',
        unit = 'mm',
    ),
    sty = device('nicos.devices.tango.Motor',
        description = 'Sample table: y',
        tangodevice = '%s/sampletable/sty' % tango_base,
        fmtstr = '%.3f',
        unit = 'mm'
    ),
    sgx = device('nicos.devices.tango.Motor',
        description = 'Sample goniometer: x',
        tangodevice = '%s/sampletable/sgx' % tango_base,
        fmtstr = '%.3f',
        unit = 'deg',
    ),
    sgy = device('nicos.devices.tango.Motor',
        description = 'Sample goniometer: x',
        tangodevice = '%s/sampletable/sgy' % tango_base,
        fmtstr = '%.3f',
        unit = 'deg',
    ),
    st_air = device('nicos.devices.tango.NamedDigitalOutput',
        description = 'Sample table pressured air',
        tangodevice = '%s/iobox/plc_air_sampletable' % tango_base,
        mapping = {'on': 1,
                   'off': 0},
    ),
)
