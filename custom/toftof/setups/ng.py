description = 'elliptical neutron guide nose'

group = 'optional'

includes = []

nethost = 'ng-focus.toftof.frm2'

devices = dict(
    ng_left     = device('toftof.neutronguide.NeutronGuideBladeMotor',
                         description = 'Left mirror bender of the flexible'
                                       ' neutron guide',
                         tacodevice = '//%s/ngfocus/left/motor' % (nethost,),
                         limitsw = 'ng_left_sw',
                         fmtstr = '%7.3f',
                         abslimits = (-20000.0, 20000.),
                        ),
    ng_left_sw  = device('devices.taco.DigitalInput',
                         description = 'Limit switch of the left motor',
                         tacodevice = '//%s/ngfocus/left/sw' % (nethost,),
                         fmtstr = '%d',
                         lowlevel = True,
                        ),
    ng_right   = device('toftof.neutronguide.NeutronGuideBladeMotor',
                         description = 'Right mirror bender of the flexible'
                                       ' neutron guide',
                         tacodevice = '//%s/ngfocus/right/motor' % (nethost,),
                         limitsw = 'ng_right_sw',
                         fmtstr = '%7.3f',
                         abslimits = (-20000.0, 20000.),
                        ),
    ng_right_sw = device('devices.taco.DigitalInput',
                         description = 'Limit switch of the right motor',
                         tacodevice = '//%s/ngfocus/right/sw' % (nethost,),
                         fmtstr = '%d',
                         lowlevel = True,
                        ),
    ng_bottom  = device('toftof.neutronguide.NeutronGuideBladeMotor',
                         description = 'Bottom mirror bender of the flexible'
                                       ' neutron guide',
                         tacodevice = '//%s/ngfocus/bottom/motor' % (nethost,),
                         limitsw = 'ng_bottom_sw',
                         fmtstr = '%7.3f',
                         abslimits = (-20000.0, 20000.),
                        ),
    ng_bottom_sw = device('devices.taco.DigitalInput',
                          description = 'Limit switch of the bottom motor',
                          tacodevice = '//%s/ngfocus/bottom/sw' % (nethost,),
                          fmtstr = '%d',
                          lowlevel = True,
                        ),
    ng_top      = device('toftof.neutronguide.NeutronGuideBladeMotor',
                         description = 'Top mirror bender of the flexible'
                                       ' neutron guide',
                         tacodevice = '//%s/ngfocus/top/motor' % (nethost,),
                         limitsw = 'ng_top_sw',
                         fmtstr = '%7.3f',
                         abslimits = (-20000.0, 20000.),
                        ),
    ng_top_sw   = device('devices.taco.DigitalInput',
                         description = 'Limit switch of the top motor',
                         tacodevice = '//%s/ngfocus/top/sw' % (nethost,),
                         fmtstr = '%d',
                         lowlevel = True,
                        ),
    ng_focus    = device('devices.generic.Slit',
                         description = 'Focussing neutron guide',
                         left = 'ng_left',
                         right = 'ng_right',
                         bottom = 'ng_bottom',
                         top = 'ng_top',
                         opmode = '4blades',
                         pollinterval = 5,
                         maxage = 10,
                        ),
)
