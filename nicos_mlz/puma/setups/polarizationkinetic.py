description = 'Kinetic polarization analysis measurements'

group = 'basic'

includes = [
    'pumabase', 'seccoll', 'collimation', 'ios', 'hv', 'notifiers', 'multidet',
    'multiana', 'rdcad', 'opticalbench', 'detector', 'ana_alias', 'pollengths',
    'slits',
]

sysconfig = {
    'datasinks': ['Listmode']
}

nethost = 'pumasrv.puma.frm2'

devices = dict(
    Listmode = device('nicos_mlz.puma.devices.kineticdetector.ListmodeSink',
        description = 'Listmode data written via QMesyDAQ',
        image = 'image',
        subdir = 'list',
        filenametemplate = ['%(pointcounter)07d.mdat'],
        detectors = ['det'],
    ),
    channels = device('nicos.devices.vendor.qmesydaq.taco.MultiCounter',
        tacodevice = '//%s/puma/qmesydaq/det' % nethost,
        lowlevel = True,
        channels = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    ),
    cycles = device('nicos_mlz.puma.devices.taco.CycleCounter',
        description = 'QMesyDAQ cycle channel',
        tacodevice = '//%s/puma/qmesydaq/counter4' % nethost,
        type = 'counter',
        lowlevel = True,
        fmtstr = '%d',
    ),
    det = device('nicos_mlz.puma.devices.kineticdetector.KineticDetector',
        description = 'Puma detector QMesydaq device (11 counters)',
        timers = ['timer'],
        monitors = ['mon1', 'cycles'],
        counters = ['channels'],
        images = [],
        maxage = 86400,
        pollinterval = None,
    ),
)

startupcode = '''
med.opmode = 'pa'
SetDetectors(det)
set('image', 'listmode', True)
'''
