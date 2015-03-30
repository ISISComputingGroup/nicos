# This setup file configures the nicos status monitor.

description = 'setup for the status monitor'
group = 'special'

Row = Column = Block = BlockRow = lambda *args: args
Field = lambda *args, **kwds: args or kwds

_expcolumn = Column(
    Block('Experiment', [
        BlockRow(Field(name='Proposal', key='exp/proposal', width=7),
                 Field(name='Title', key='exp/title', width=20,
                       istext=True, maxlen=20),
                 Field(name='Sample', key='sample/samplename'),
                 Field(name='Remark', key='exp/remark'),
                 Field(name='Current status', key='exp/action', width=40,
                       istext=True, maxlen=40),
                 Field(name='Last file', key='exp/lastscan'))]),
)


_reactorBlock = Block('Reactor', [
    BlockRow(Field(name='Reactor power', dev='ReactorPower', format='%.1f', width=6),
             Field(name='6-fold-shutter', dev='Sixfold'),
             Field(name='NL-1', dev='NL1', min='open', width=6),
             )
    ],
)

_shutterBlock = Block('Shutter', [
    BlockRow(Field(name='Photo-shutter', dev='photoshutter'),
             Field(name='Gamma-shutter', dev='gammashutter'),
             )
    ]
)

_sampleTableBlock = Block('Sample table', [
    BlockRow(Field(name='omega', dev='omega_sampletable',)),
    BlockRow(Field(name='x', dev='x_sampletable',)),
    BlockRow(Field(name='y', dev='y_sampletable',)),
    ]
)

_sampleStepperBlock = Block('Sample stepper', [
    BlockRow(Field(name='omega', dev='omega_samplestepper')),
    ]
)

_activeDetectorBlock = Block('Active detector', [
    BlockRow(Field(name='Detector', key='exp/detlist', item=0)),
    ]
)

_slitsBlock = Block('Slits', [
    BlockRow(Field(name='Slit dia1', dev='d_diaphragm1')),
    BlockRow(Field(name='Slit dia2', dev='d_diaphragm2')),
    ]
)

_cryoStreamBlock = Block('Cryo-stream', [
    BlockRow(Field(name='Temperature', dev='T_cryostream')),
    BlockRow(Field(name='Setpoint', key='T_cryostream/setpoint')),
    ], 'cryostream'
)

_outsideWorldBlock = Block('Outside world', [
    BlockRow(Field(name='Next U-Bahn U6', dev='ubahn'),
             Field(name='Outside T', dev='meteo'),
             )
    ],
)


_secondRow = Row(
    Column(_reactorBlock),
    Column(_shutterBlock))

_thirdRow = Row(
    Column(_sampleTableBlock),
    Column(_sampleStepperBlock, _activeDetectorBlock),
    Column(_slitsBlock))

_forthRow = Row(
    Column(_cryoStreamBlock),
    Column(_outsideWorldBlock)
    )


devices = dict(
    Monitor = device('services.monitor.qt.Monitor',
                     title = 'NICOS status monitor',
                     loglevel = 'info',
                     cache = 'phys.biodiff.frm2:14869',
                     font = 'Luxi Sans',
                     valuefont = 'Consolas',
                     padding = 0,
                     layout = [Row(_expcolumn), _secondRow, _thirdRow, _forthRow],
                    ),
)
