description = 'Detector CARESS HWB Devices'

group = 'lowlevel'

nameservice = 'stressictrl.stressi.frm2'
caresspath = '/opt/caress'
toolpath = '/opt/caress'
nethost = 'stressisrv.stressi.frm2'

devices = dict(
    mon = device('nicos.devices.vendor.qmesydaq.caress.Counter',
                 description = 'HWB MON',
                 fmtstr = '%d',
                 type = 'monitor',
                 nameserver = '%s' % (nameservice,),
                 config = 'MON 500 qmesydaq.caress_object monitor1',
                 caresspath = caresspath,
                 toolpath = toolpath,
                 lowlevel = True,
                 absdev = False,
                ),
    tim1 = device('nicos.devices.vendor.qmesydaq.caress.Timer',
                  description = 'HWB TIM1',
                  fmtstr = '%.2f',
                  unit = 's',
                  nameserver = '%s' % (nameservice,),
                  config = 'TIM1 500 qmesydaq.caress_object timer 1',
                  caresspath = caresspath,
                  toolpath = toolpath,
                  lowlevel = True,
                  absdev = False,
                 ),
    image = device('nicos.devices.vendor.qmesydaq.caress.Image',
                   description = 'Image data device',
                   fmtstr = '%d',
                   pollinterval = 86400,
                   nameserver = '%s' % (nameservice,),
                   config = 'HISTOGRAM 500 qmesydaq.caress_object histogram 0 '
                            '256 256',
                   caresspath = caresspath,
                   toolpath = toolpath,
                   lowlevel = True,
                   absdev = False,
                  ),
    # histogram = device('frm2.qmesydaqsinks.HistogramSink',
    #                    description = 'Histogram data written via QMesyDAQ',
    #                    image = 'image',
    #                   ),
    listmode = device('frm2.qmesydaqsinks.ListmodeSink',
                      description = 'Listmode data written via QMesyDAQ',
                      image = 'image',
                     ),
    adet = device('nicos.devices.generic.Detector',
                  description = 'Classical detector with single channels',
                  timers = ['tim1'],
                  monitors = ['mon'],
                  counters = [],
                  images = ['image'],
                  pollinterval = None,
                  liveinterval = 1.,
                 ),
    ysd = device('nicos.devices.generic.ManualMove',
                 description = 'Distance detector to sample',
                 fmtstr = '%.1f',
                 default = 1035,
                 unit = 'mm',
                 abslimits = (700, 1700),
                 requires =  {'level': 'admin',},
                ),
    hv1   = device('nicos.devices.taco.VoltageSupply',
                   description = 'ISEG HV power supply 1',
                   requires = {'level': 'admin'},
                   tacodevice = '//%s/stressi/det/hv1' % (nethost,),
                   abslimits = (0, 3200),
#                  ramp = 120,
                  ),
    hv1_current = device('nicos.devices.taco.AnalogInput',
                         description = 'ISEG HV power supply 1 current',
                         tacodevice = '//%s/stressi/det/current1' % (nethost,),
                        ),
    hv2   = device('nicos.devices.taco.VoltageSupply',
                   description = 'ISEG HV power supply 2',
                   requires = {'level': 'admin'},
                   tacodevice = '//%s/stressi/det/hv2' % (nethost,),
                   abslimits = (-2500, 0),
#                  ramp = 120,
                  ),
    hv2_current = device('nicos.devices.taco.AnalogInput',
                         description = 'ISEG HV power supply 2 current',
                         tacodevice = '//%s/stressi/det/current2' % (nethost,),
                        ),
)

startupcode='''
SetDetectors(adet)
'''
