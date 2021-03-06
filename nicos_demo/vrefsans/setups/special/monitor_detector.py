# coding: utf-8

# created by Martin Haese, Tel FRM 10763
# last modified 01.02.2018
# to call it
# ssh -X refsans@refsansctrl01 oder 02
# cd /refsanscontrol/src/nicos-core
# INSTRUMENT=nicos_mlz.refsans bin/nicos-monitor -S monitor_detector

description = 'REFSANS detector monitor'
group = 'special'

_experimentcol = Column(
    Block(' experiment ', [
        BlockRow(
                 Field(name='proposal', key='exp/proposal', width=8),
                 Field(name='proposer', key='exp/proposer', width=24),
                 Field(name='title',    key='exp/title',    width=24,
                       istext=True, maxlen=20),
                 Field(name='Sample', dev='Sample', width=20),
                 Field(name='current status', key='exp/action', width=24,
                       istext=True, maxlen=40),
            )
        ],
    ),
)

# Legende fuer _detconfigcol
# dev='...' stellt hier nur die moeglichen Werte dar, keine devices

_detconfigcol = Column(
    Block(' detector information ', [
        BlockRow(
            Field(name='data acquisition system', dev='das_mesytec_fast_both', width=20),
            Field(name='total counts', dev='image', width=16),
            Field(name='count time',   dev='timer', width=12, unit='sec'),
            Field(name='count rate',   dev='detector_count_rate', width=12, unit='cps'),
            Field(name='monitor 1', key='mon1', width=12),
            Field(name='monitor 2', key='mon2', width=12),
            Field(name='last file', key='det/lastfilenumber', width=12),
            ),
        ],
    ),
)

# In _detarecol soll das aktuelle Bild des Detektors angezeigt
# und moeglichst alle 1 bis 2 Sekunde aktualisiert werden.
_detarecol = Column(
    Block(' active detector area ', [
        BlockRow(
            Field(dev='detector',
                picture='/refsanscontrol/src/nicos-core/nicos_mlz/refsans/setups/screenshots/detector_2D.png',
                # picture='detector_area.png',
                width=54, height=40),
            ),
        ],
    ),
)

# In _histogramcol soll das Histogram aus der aktuell laufenden Messung
# berechnete und moeglichst alle 10 bis 30 Sekunden aktualisiert werden.
_histogramcol = Column(
    Block(' wavelength histogram ', [
        BlockRow(
            Field(dev='histogram',
                picture='/refsanscontrol/src/nicos-core/nicos_mlz/refsans/setups/screenshots/detector_histo.png',
                # picture='histogram.png',
                width=50, height=40),
            ),
        ],
    ),
)

_beanstop1col = Column(
    Block('beamstop 1', [
        BlockRow(
            Field(name='status',   dev='stop1_on_off',  width=8),
            Field(name='hor pos',  dev='stop1_horizontal_position', width=8),
            Field(name='vert pos', dev='stop1_vertical_position', width=8),
            ),
        ],
    ),
)

_beanstop2col = Column(
    Block('beamstop 2', [
        BlockRow(
            Field(name='status',   dev='stop2_on_off',  width=8),
            Field(name='hor pos',  dev='stop2_horizontal_position', width=8),
            Field(name='vert pos', dev='stop2_vertical_position', width=8),
            ),
        ],
    ),
)

_momentumcol = Column(
    Block('momentum transfer', [
        BlockRow(
            Field(name='theta', dev='sample_theta',  width=8),
            Field(name='q_min', dev='q_min', width=8, unit='1/AA'),
            Field(name='q_max', dev='q_max', width=8, unit='1/AA'),
            ),
        ],
    ),
)

devices = dict(
    Monitor = device('nicos.services.monitor.qt.Monitor',
        title = description,
        loglevel = 'info',
        cache = 'localhost',
        valuefont = 'Consolas',
        padding = 5,
        layout = [
            Row(_experimentcol),
            Row(_detconfigcol),
            Row(_detarecol, _histogramcol),
            Row(_beanstop1col, _beanstop2col, _momentumcol),
        ],
    ),
)
