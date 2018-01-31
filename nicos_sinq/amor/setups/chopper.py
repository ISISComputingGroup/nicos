description = 'Astrium chopper device in SINQ AMOR'

pvprefix = 'SQ:AMOR:chopper:'

devices = dict(
    ch1_speed=device('nicos_sinq.devices.epics.astrium_chopper.EpicsChopperSpeed',
        description='Speed controller for the master chopper',
        epicstimeout=3.0,
        readpv=pvprefix + 'ch1.ActSpd',
        writepv=pvprefix + 'ch1.Spd',
        targetpv=pvprefix + 'ch1.Spd-RB',
        timeout=None,
        window=2.0,
        precision=0.01,
        lowlevel=True,
    ),
    ch1=device('nicos_sinq.devices.epics.astrium_chopper.EpicsChopperDisc',
        description='Chopper master',
        epicstimeout=3.0,
        basepv=pvprefix + 'ch1',
        speed='ch1_speed',
    ),
    ch2_phase=device('nicos_ess.devices.epics.base.EpicsWindowTimeoutDeviceEss',
        description='Phase controller for the slave chopper 2',
        epicstimeout=3.0,
        readpv=pvprefix + 'ch2.ActPhs',
        writepv=pvprefix + 'ch2.Phs',
        targetpv=pvprefix + 'ch2.Phs-RB',
        timeout=None,
        window=2.0,
        precision=0.01,
        lowlevel=True,
    ),
    ch2_ratio=device('nicos_ess.devices.epics.base.EpicsDigitalMoveableEss',
        description='Ratio controller for the slave chopper',
        epicstimeout=3.0,
        readpv=pvprefix + 'ch2.Ratio',
        writepv=pvprefix + 'ch2.Ratio',
        lowlevel=True
    ),
    ch2=device('nicos_sinq.devices.epics.astrium_chopper.EpicsChopperDisc',
        description='Chopper slave',
        epicstimeout=3.0,
        basepv=pvprefix + 'ch2',
        phase='ch2_phase',
        ratio='ch2_ratio',
    ),
    chopper=device('nicos_sinq.devices.epics.astrium_chopper.EpicsAstriumChopper',
        description='Astrium Chopper',
        precision=1,
        choppers=['ch1', 'ch2']
    )

)
