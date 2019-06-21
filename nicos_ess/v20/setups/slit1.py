description = 'Slit 1'
servername = 'EXV20'
nameservice = '192.168.1.254'

devices = dict(
    slit1hl = device('nicos.devices.vendor.caress.Motor',
        description = 'Slit 1 Horizontal Left',
        fmtstr = '%.2f',
        unit = 'mm',
        coderoffset = 0,
        abslimits = (-30, 30),
        nameserver = '%s' % (nameservice,),
        objname = '%s' % (servername),
        config = 'MB1HL 500 nist222dh1787.hmi.de:/st222.caress_object '
                 'CopleyStepnet 2 -4000 BeckhoffKL5001 BK5120/63/32/8/0 '
                 '-4096 -107854',
        lowlevel = True,
        loadblock = '''start=never,async
stop = never, async
read = always, async
motion_usefloat = true
motion_autodelete = false
motion_display = 10
motion_displayformat = %0.3f
motion_enc_signedbits = 24
loadoffset = yes
'''

    ),
    slit1hr = device('nicos.devices.vendor.caress.Motor',
        description = 'Slit 1 Horizontal Right',
        fmtstr = '%.2f',
        unit = 'mm',
        coderoffset = 0,
        abslimits = (-30, 30),
        nameserver = '%s' % (nameservice,),
        objname = '%s' % (servername),
        config = 'MB1HR 500 nist222dh1787.hmi.de:/st222.caress_object '
                 'CopleyStepnet 3 -4000 BeckhoffKL5001 BK5120/63/32/12/0 '
                 '-4096 230417',
        lowlevel = True,
        loadblock = '''start=never,async
stop = never, async
read = always, async
motion_usefloat = true
motion_autodelete = false
motion_display = 11
motion_displayformat = %0.3f
loadoffset = yes
'''

    ),
    slit1vb = device('nicos.devices.vendor.caress.Motor',
        description = 'Slit 1 Vertical Bottom',
        fmtstr = '%.2f',
        unit = 'mm',
        coderoffset = 0,
        abslimits = (-60, 60),
        nameserver = '%s' % (nameservice,),
        objname = '%s' % (servername),
        config = 'MB1VB 500 nist222dh1787.hmi.de:/st222.caress_object '
                 'CopleyStepnet 4 4000 BeckhoffKL5001 BK5120/63/32/16/0 '
                 '4096 368403',
        lowlevel = True,
        loadblock = '''start = never, async
stop = never, async
read = always, async
motion_usefloat = true
motion_autodelete = false
motion_display = 12
motion_displayformat = %0.3f
loadoffset = yes
'''
    ),
    slit1vt = device('nicos.devices.vendor.caress.Motor',
        description = 'Slit 1 Vertical Top',
        fmtstr = '%.2f',
        unit = 'mm',
        coderoffset = 0,
        abslimits = (-60, 60),
        nameserver = '%s' % (nameservice,),
        objname = '%s' % (servername),
        config = 'MB1VT 500 nist222dh1787.hmi.de:/st222.caress_object '
                 'CopleyStepnet 5 4000 BeckhoffKL5001 BK5120/63/32/20/0 '
                 '4096 364514',
        lowlevel = True,
        loadblock = '''start = never, async
stop = never, async
read = always, async
motion_usefloat = true
motion_autodelete = false
motion_display = 13
motion_displayformat = %0.3f
loadoffset = yes
'''
    ),
    slit1 = device('nicos.devices.generic.Slit',
        description = 'Slit 1',
        left = 'slit1hl',
        right = 'slit1hr',
        top = 'slit1vt',
        bottom = 'slit1vb',
        opmode = 'offcentered',
        coordinates = 'equal',
    ),
)
