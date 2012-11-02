#  -*- coding: utf-8 -*-

description = 'Analyser'

includes = ['system', 'befilter']
 
 # ath,att,agx,--,--,aty,--, afh

devices = dict(
    bus1 = device('devices.vendor.ipc.IPCModBusTaco',
            tacodevice='//pandasrv/panda/moxa/port1',
            loglevel='info',
            timeout=0.5,
    ),
    
    # ATT is first device and has 1 stepper, 0 poti, 1 coder
    att_step = device('devices.vendor.ipc.Motor',
            bus = 'bus1',
            addr = 0x51,                # 0x5.. = stepper, 0x6.. = poti, 0x7.. = coder ; .. = channel
            slope = -200,
            unit = 'deg',
            abslimits = (-140,140),
            zerosteps = 500000,
            confbyte = 8+128,   #  128 = ten times slower (no gear at att!!!)
            speed = 100,
            accel = 50,
            microstep = 2,
            startdelay = 0,
            stopdelay = 0,
            ramptype = 1,
            #~ current = 2.0,
            lowlevel = True,
    ),
    att_enc = device('devices.vendor.ipc.Coder',
            bus = 'bus1',
            addr = 0x71,
            slope = -2**20/360.0,
            zerosteps = 854914,
            confbyte = 148,
            unit = 'deg',
            circular = -360, # map values to -180..0..180 degree
            lowlevel = True,
    ),
    anablocks_beckhoff = device('panda.wechsler.Beckhoff',
            host='anablocks.panda.frm2',
            lowlevel = True,
    ),
    anablocks = device('panda.ana.AnaBlocks',
            beckhoff = 'anablocks_beckhoff',
            powertime = 10,
            lowlevel = True,
    ),
    att = device('panda.ana.ATT_Axis',
            anablocks='anablocks',
            windowsize = 11.5,
            blockwidth = 15.12,
            blockoffset = -7.7,
            motor = 'att_step',
            coder = 'att_enc',
            obs = [],
            precision = 0.05,
            jitter = 0.5,
            maxtries = 10,
            offset = 0.4934,
    ),
    #~ att = device('devices.generic.Axis',
            #~ motor = 'att_step',
            #~ coder = 'att_enc',
            #~ obs = [],
            #~ precision = 0.05,
            #~ jitter=1,
            #~ maxtries=50
    #~ ),
    
    # ath is second device and has 1 stepper, 0 poti, 1 coder
    ath_step = device('devices.vendor.ipc.Motor',
            bus = 'bus1',
            addr = 0x52,
            slope = 1600,
            unit = 'deg',
            abslimits = (-120,5),
            zerosteps = 500000,
            speed = 250,
            accel = 24,
            microstep = 16,
            startdelay = 0,
            stopdelay = 0,
            ramptype = 1,
            lowlevel = True,
            #~ current = 2.0,
    ),
    ath_enc = device('devices.vendor.ipc.Coder',
            bus = 'bus1',
            addr = 0x72,
            slope = 2**18/360.0,
            zerosteps = 235467,
            confbyte = 50,
            unit = 'deg',
            circular = -360, # map values to -180..0..180 degree
            lowlevel = True,
    ),
    ath = device('devices.generic.Axis',
            motor = 'ath_step',
            coder = 'ath_enc',
            obs = [],
            precision = 0.03,
            maxtry = 50,
            offset = -2.297,
            #~ rotary = True,
    ),
    
    # agx is third device and has 1 stepper, 0 poti, 1 coder
    agx_step = device('devices.vendor.ipc.Motor',
            bus = 'bus1',
            addr = 0x53,
            slope = 3200,
            unit = 'deg',
            abslimits = (-5,5),
            zerosteps = 500000,
            speed = 50,
            accel = 8,
            microstep = 16,
            startdelay = 0,
            stopdelay = 0,
            ramptype = 1,
            lowlevel = True,
            #~ current = 2.0,
    ),
    agx_enc = device('devices.vendor.ipc.Coder',
            bus = 'bus1',
            addr = 0x73,
            slope = -2**13/1.0,
            zerosteps = 16121227,
            confbyte = 153,
            unit = 'deg',
            circular = -4096,    # 12 bit (4096) for turns, times 2 deg per turn divided by 2 (+/-)
            lowlevel = True,
    ),
    agx = device('devices.generic.Axis',
            motor = 'agx_step',
            coder = 'agx_enc',
            obs = [],
            precision = 0.01,
            #~ rotary = True,
    ),
    
    # fourth device is unused
    
    # fith device is unused
    
    # aty is sixth device and has 1 stepper, 0 poti, 1 coder
    aty_step = device('devices.vendor.ipc.Motor',
            bus = 'bus1',
            addr = 0x56,
            slope = 400,
            unit = 'mm',
            abslimits = (-10,10),
            zerosteps = 500000,
            speed = 50,
            accel = 8,
            microstep = 16,
            lowlevel = True,
            #~ divider = 4,
            #~ current = 1.5,
    ),
    aty_enc = device('devices.vendor.ipc.Coder',
            bus = 'bus1',
            addr = 0x76,
            slope = -2**13/1.0,
            zerosteps = 15348276,
            confbyte = 153,
            unit = 'mm',
            circular = -4096,    # 12 bit (4096) for turns, times 2 deg per turn divided by 2 (+/-)
            lowlevel = True,
    ),
    aty = device('devices.generic.Axis',
            motor = 'aty_step',
            coder = 'aty_enc',
            obs = [],
            precision = 0.05,
            fmtstr='%.1f',
    ),
    
    # seventh device is unused
    
    # afh is eigth device and has 1 stepper, 0 poti, 0 coder
    afh_step = device('devices.vendor.ipc.Motor',
            bus = 'bus1',
            addr = 0x58,
            slope = 400/360.0,
            unit = 'deg',
            #~ abslimits = (-5,340),
            abslimits = (-400,400),
            zerosteps = 500000,
            speed = 100,
            accel = 15,
            microstep = 2,
            startdelay = 0,
            stopdelay = 0,
            ramptype = 1,
            lowlevel = True,
            #~ current = 2.0,
    ),
    #~ afh_enc = device('devices.vendor.ipc.Coder',
            #~ bus = 'bus1',
            #~ addr = 0x78,
            #~ slope = -2**13/360.0,
            #~ zerosteps = 15121559,
            #~ confbyte = 145,
            #~ unit = 'deg',
            #~ circular = -4096,    # 12 bit (4096) for turns, times 2 deg per turn divided by 2 (+/-)
    #~ ),
    #~ afh = device('devices.generic.Axis',
            #~ motor = 'afh_step',
            #~ coder = 'afh_enc',
            #~ obs = [],
            #~ precision = 1,
            #~ fmtstr='%.1f',
    #~ ),
  
    #~ afh = device('devices.generic.Axis',
    afh = device('panda.rot_axis.RotAxis',
            motor = 'afh_step',
            coder = 'afh_step',
            obs = [],
            precision = 1,
            fmtstr='%.1f',
    ),
  
)
