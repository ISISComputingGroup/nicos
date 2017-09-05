description = 'Neutron counter box and channels in the SINQ AMOR.'

pvprefix = 'SQ:AMOR:counter'

devices = dict(
    timepreset=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsTimerActiveChannel',
        epicstimeout=3.0,
        description='Used to set and view time preset',
        unit='sec',
        valuepv=pvprefix + '.TP',
        presetpv=pvprefix + '.TP',
    ),
    elapsedtime=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsTimerPassiveChannel',
        epicstimeout=3.0,
        description='Used to view elapsed time while counting',
        unit='sec',
        valuepv=pvprefix + '.T',
    ),
    countpreset=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterActiveChannel',
        epicstimeout=3.0,
        description='Used to set and view count preset',
        type='counter',
        valuepv=pvprefix + '.PR2',
        presetpv=pvprefix + '.PR2',
    ),
    c1=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='First scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S2',
    ),
    c2=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Second scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S3',
    ),
    c3=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Third scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S4',
    ),
    c4=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Fourth scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S5',
    ),
    c5=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Fifth scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S6',
    ),
    c6=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Sixth scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S7',
    ),
    c7=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Seventh scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S8',
    ),
    c8=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsCounterPassiveChannel',
        epicstimeout=3.0,
        description='Eighth scalar counter channel',
        type='counter',
        valuepv=pvprefix + '.S9',
    ),
    psd_tof=device(
        'nicos_sinq.amor.devices.epics_scaler_record.EpicsScalerRecord',
        epicstimeout=3.0,
        description='EL737 counter box that counts neutrons and '
                    'starts streaming events',
        startpv=pvprefix + '.CNT',
        pausepv=pvprefix + ':Pause',
        statuspv=pvprefix + ':Status',
        errormsgpv=pvprefix + ':MsgTxt',
        timers=['timepreset', 'elapsedtime'],
        counters=['countpreset', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7',
                  'c8'],
    ),
    cter1=device(
        'nicos_sinq.amor.devices.epics_extensions.EpicsAsynController',
        epicstimeout=3.0,
        description='Controller of the counter box',
        commandpv='SQ:AMOR:cter1.AOUT',
        replypv='SQ:AMOR:cter1.AINP',
    ),
)