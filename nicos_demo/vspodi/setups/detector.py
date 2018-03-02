description = 'Virtual SPODI detector'

group = 'lowlevel'

includes = []

devices = dict(
    mon = device('nicos.devices.generic.VirtualCounter',
        description = 'Simulated MON1',
        fmtstr = '%d',
        type = 'monitor',
        lowlevel = True,
    ),
    tim1 = device('nicos.devices.generic.VirtualTimer',
        description = 'Simulated TIM1',
        fmtstr = '%.2f',
        unit = 's',
        lowlevel = True,
    ),
    image = device('nicos.devices.generic.VirtualImage',
        description = 'Image data device',
        fmtstr = '%d',
        pollinterval = 86400,
        lowlevel = True,
        sizes = (80, 256),
    ),
    basedet = device('nicos.devices.generic.Detector',
        description = 'Classical detector with single channels',
        timers = ['tim1'],
        monitors = ['mon'],
        counters = [],
        images = ['image'],
        maxage = 86400,
        pollinterval = None,
        lowlevel = True,
    ),
    adet = device('nicos_mlz.spodi.devices.detector.Detector',
        description = 'Scanning (resolution steps) detector',
        motor = 'tths',
        detector = 'basedet',
        pollinterval = None,
        maxage = 86400,
        liveinterval = 5,
    ),
    # histogram = device('nicos_mlz.frm2.devices.qmesydaqsinks.HistogramFileFormat',
    #     description = 'Histogram data written via QMesyDAQ',
    #     image = 'image',
    # ),
    # listmode = device('nicos_mlz.frm2.devices.qmesydaqsinks.ListmodeFileFormat',
    #     description = 'Listmode data written via QMesyDAQ',
    #     image = 'image',
    # ),
    hv1 = device('nicos.devices.generic.VirtualMotor',
        description = 'ISEG HV power supply 1',
        requires = {'level': 'admin'},
        abslimits = (0, 3200),
        speed = 2,
        fmtstr = '%.1f',
        unit = 'V',
    ),
    hv2 = device('nicos.devices.generic.VirtualMotor',
        description = 'ISEG HV power supply 2',
        requires = {'level': 'admin'},
        abslimits = (-2500, 0),
        speed = 2,
        fmtstr = '%.1f',
        unit = 'V',
    ),
)

startupcode = '''
SetDetectors(adet)
'''
