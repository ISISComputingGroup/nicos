description = 'setup for the velocity selector'

jcns_tango_host = 'tango://cpci01.antares.frm2:10000'

devices = dict(
    selector_state = device('devices.vendor.astrium.SelectorState',
                            tacodevice = '//antaressrv/antares/network/selector',
                            lowlevel = True,
                            pollinterval = 10,
                            maxage = 12,
                            comtries = 5,
                           ),
    selector = device('devices.vendor.astrium.SelectorSpeed',
                      description = 'Selector speed control',
                      abslimits = (3100, 21000),
                      blockedspeeds = [(3300,4200),(7500,9500)],
                      statedev = 'selector_state',
                      unit = 'rpm',
                      fmtstr = '%.0f',
                      precision = 50,
                      timeout = 600,
                      warnlimits = (0, 3200),
                     ),
    selector_lambda = device('devices.vendor.astrium.SelectorLambda',
                      description = 'Selector center wavelength control',
                      seldev = 'selector',
                      unit = 'A',
                      fmtstr = '%.2f',
                      twistangle = 23.5,
                      length = 0.25,
                      beamcenter = 0.115,
                      maxspeed = 21000,
                     ),
    selector_lambda_tilt = device('devices.vendor.astrium.SelectorLambda',
                      description = 'Selector center wavelength control',
                      seldev = 'selector',
                      unit = 'A',
                      fmtstr = '%.2f',
                      twistangle = 12.63,
                      length = 0.25,
                      beamcenter = 0.115,
                      maxspeed = 21000,
                     ),
    selector_sspeed = device('devices.vendor.astrium.SelectorValue',
                             description = 'Selector speed read out by optical sensor',
                             statedev = 'selector_state',
                             valuename = 'SSPEED',
                             unit = 'Hz',
                             fmtstr = '%.1d',
                            ),
    selector_vacuum = device('devices.vendor.astrium.SelectorValue',
                             description = 'Vacuum in the selector',
                             statedev = 'selector_state',
                             valuename = 'VACUM',
                             unit = 'x1e-3 mbar',
                             fmtstr = '%.5f',
                             warnlimits = (0, 0.005),
                            ),
    selector_rtemp = device('devices.vendor.astrium.SelectorValue',
                             description = 'Temperature of the selector',
                             statedev = 'selector_state',
                             valuename = 'RTEMP',
                             unit = 'C',
                             fmtstr = '%.1f',
                             warnlimits = (10, 45),
                            ),
    selector_wflow = device('devices.vendor.astrium.SelectorValue',
                             description = 'Cooling water flow rate through selector',
                             statedev = 'selector_state',
                             valuename = 'WFLOW',
                             unit = 'l/min',
                             fmtstr = '%.1f',
                             warnlimits = (1.5, 10),
                            ),
    selector_winlt = device('devices.vendor.astrium.SelectorValue',
                             description = 'Cooling water temperature at inlet',
                             statedev = 'selector_state',
                             valuename = 'WINLT',
                             unit = 'C',
                             fmtstr = '%.1f',
                             warnlimits = (15, 20),
                            ),
    selector_woutt = device('devices.vendor.astrium.SelectorValue',
                             description = 'Cooling water temperature at outlet',
                             statedev = 'selector_state',
                             valuename = 'WOUTT',
                             unit = 'C',
                             fmtstr = '%.1f',
                             warnlimits = (15, 20),
                            ),
    selector_vibrt = device('devices.vendor.astrium.SelectorValue',
                             description = 'Selector vibration',
                             statedev = 'selector_state',
                             valuename = 'VIBRT',
                             unit = 'mm/s',
                             fmtstr = '%.2f',
                             warnlimits = (0, 1),
                            ),
    selector_linear = device('devices.tango.Motor',
                      description = 'Selector translation',
                      unit = 'mm',
                      tangodevice = '%s/antares/fzjs7/Selektor_linear' % jcns_tango_host,
                      lowlevel = True,
                     ),
    selector_inout = device('devices.generic.Switcher',
                        description = 'Moves Selector in and out of beam',
                        moveable = 'selector_linear',
                        mapping = { 'in':165.0, 'out':0.0 },
                        fallback = '<undefined>',
                        unit = '',
                        maxage = 5,
                        pollinterval = 3,
                        precision = 0.5,
                       ),
    selector_tilt = device('devices.taco.Motor',
                        speed = 0.05,
                        unit = 'deg',
                        description = 'tilt of velocity selector',
                        tacodevice = 'antares/copley/m16',
                        abslimits = (-0, 10),
                        userlimits = (-0, 10),
                        lowlevel = False,
                        maxage = 7,
                        pollinterval = 3,
                      ),
)
