description = 'setup for the HTML status monitor'
group = 'special'

Row = Column = Block = BlockRow = lambda *args: args
Field = lambda *args, **kwds: args or kwds

_expcolumn = Column(
    Block('Experiment', [
        BlockRow(Field(name='Proposal', key='exp/proposal', width=7),
                 Field(name='Title',    key='exp/title',    width=15,
                       istext=True, maxlen=15),
                 Field(name='Sample',   key='sample/samplename', width=15,
                       istext=True, maxlen=15),
                 Field(name='Remark',   key='exp/remark',   width=30,
                       istext=True, maxlen=30),
                 Field(name='Current status', key='exp/action', width=30,
                       istext=True),
                 Field(name='Last file', key='exp/lastscan')),
    ]),
)

_column3 = Column(
    Block('Analyzer', [BlockRow('ath', 'att')], 'analyzer'),
    Block('Detector', [
        BlockRow('timer', 'mon2', 'ctr1'),
        BlockRow(Field(dev='det_fore', item=0, name='Forecast', format='%.2f'),
                 Field(dev='det_fore', item=2, name='Forecast', format='%d'),
                 Field(dev='det_fore', item=3, name='Forecast', format='%d')),
        BlockRow(Field(dev='MonHV', width=5),
                 Field(dev='DetHV', width=5)),
    ], '!cascade'),
    Block('Cascade', [
        BlockRow(Field(name='ROI',   key='psd/lastcounts', item=0, width=9),
                 Field(name='Total', key='psd/lastcounts', item=1, width=9),
                 Field(name='MIEZE', key='psd/lastcontrast', item=0, format='%.3f', width=6),
                 Field(name='Last image', key='exp/lastimage')),
        BlockRow('timer', 'mon2', 'ctr1'),
        BlockRow(Field(dev='MonHV', width=5), Field(dev='PSDGas', width=6),
                 Field(dev='PSDHV', width=5), Field(dev='dtx')),
    ], 'cascade'),
    Block('3He cell', [
        BlockRow(Field(name='Polarization', dev='pol', width=7),
                 Field(name='Guide field', dev='He_GF')),
    ], 'helios'),
    Block('MIEZE', [
        BlockRow(Field(name='Setting', dev='mieze', item=0, istext=True, width=5),
                 Field(name='tau', dev='mieze', item=1, unit='ps', width=7),
                 Field(name='Tuning', key='mieze/tuning', istext=True, width=10)),
        BlockRow('dc1', 'freq1', 'amp1', 'coilamp1'),
        BlockRow('dc2', 'freq2', 'amp2', 'coilamp2'),
        BlockRow('fp1', 'fp2', 'rp1', 'rp2'),
        BlockRow('cc1', 'cc2', 'freq3', 'amp3'),
    ], 'mieze'),
#    Block('X-Z table axes', [BlockRow('mx', 'my')], 'gauss'),
    Block('TAS', [
        BlockRow(Field(name='H', dev='mira', item=0, format='%.3f', unit=''),
                 Field(name='K', dev='mira', item=1, format='%.3f', unit=''),
                 Field(name='L', dev='mira', item=2, format='%.3f', unit=''),
                 Field(name='E', dev='mira', item=3, format='%.3f', unit='')),
        BlockRow(Field(name='Mode', key='mira/scanmode'),
                 Field(name='ki', dev='mono'), Field(name='kf', dev='ana'),
                 Field(name='Unit', key='mira/energytransferunit')),
    ], 'tas'),
    Block('Diffraction', [
        BlockRow(Field(name='H', dev='mira', item=0, format='%.3f', unit=''),
                 Field(name='K', dev='mira', item=1, format='%.3f', unit=''),
                 Field(name='L', dev='mira', item=2, format='%.3f', unit='')),
        BlockRow(Field(name='ki', dev='mono')),
    ], 'diff'),
    Block('MIRA Magnet', [BlockRow('I')], 'miramagnet'),
)

_column2 = Column(
    Block('Slits', [
        BlockRow(Field(dev='ss1', name='Sample slit 1 (ss1)', width=24, istext=True)),
        BlockRow(Field(dev='ss2', name='Sample slit 2 (ss2)', width=24, istext=True)),
    ], 'slits'),
    Block('Sample', [
        BlockRow('om', 'sth', 'phi'),
        BlockRow('stx', 'sty', 'stz'),
        BlockRow('sgx', 'sgy'),
    ], 'sample'),
    Block('Eulerian cradle', [
        BlockRow('echi', 'ephi'),
#        BlockRow(Field(dev='ec', name='Scattering plane', width=20, istext=True)),
    ], 'euler'),
    Block('Sample environment', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit'),
                 Field(name='A', dev='T_ccr5_A'), Field(name='B', dev='T_ccr5_B'),
                 Field(name='C', dev='T_ccr5_C')),
        BlockRow(Field(name='P', key='t/p'), Field(name='I', key='t/i'),
                 Field(name='D', key='t/d'), Field(name='p', dev='ccr5_p1')),
    ], 'ccr5'),
    Block('Furnace (IRF01)', [
        BlockRow(Field(name='Setpoint', key='t_irf01/setpoint', unitkey='t_irf01/unit', format='%.2f'),
                 Field(name='Temp', dev='T_irf01')),
        BlockRow(Field(name='P', key='t_irf01/p'), Field(name='I', key='t_irf01/i'),
                 Field(name='D', key='t_irf01/d')),
        BlockRow(Field(name='Heater power', key='t_irf01/heaterpower', unit='%', format='%.2f')),
    ], 'irf01'),
    Block('3He-4He insert (cryo3)', [
        BlockRow(Field(name='Setpoint', key='t/setpoint', unitkey='t/unit', format='%.2f'),
                 Field(name='T', dev='T'), Field(name='Ts', dev='Ts')),
        BlockRow(Field(name='P', key='t/p', width=4), Field(name='I', key='t/i', width=4),
                 Field(name='D', key='t/d', width=4),
                 Field(name='turbo', dev='cryo3_p1'),
                 Field(name='cycle', dev='cryo3_p4'),
                 ),
    ], 'cryo3'),
    Block('FRM Magnet', [
        BlockRow('B', Field(name='sth', dev='sth_m7T5_stick'),
                 Field(name='T1', dev='m7T5_T1', width=6),
                 Field(name='T2', dev='m7T5_T2', width=6)),
        BlockRow(Field(name='T3', dev='m7T5_T3', width=6),
                 Field(name='T4', dev='m7T5_T4', width=6),
                 Field(name='T8', dev='m7T5_T8', width=6)),
    ], 'magnet75'),
    Block('SANS-1 Magnet', [
        BlockRow('B', Field(name='T2', dev='m5T_T2', width=6),
                 Field(name='T3', dev='m5T_T3', width=6)),
        BlockRow(Field(name='T4', dev='m5T_T4', width=6),
                 Field(name='T5', dev='m5T_T5', width=6),
                 Field(name='T6', dev='m5T_T6', width=6)),
    ], 'magnet5'),
    Block('TTi + Huber', [
        BlockRow('dct1', 'dct2', Field(dev='flip', width=5)),
        BlockRow('tbl1', 'tbl2'),
    ], 'tti'),
    Block('Relays', [BlockRow('relay1', 'relay2')], 'relay'),
)

_column1 = Column(
    Block('MIRA1', [
        BlockRow('FOL', 'flip1'),
        BlockRow('mth', 'mtt'),
        BlockRow('mtx', 'mty'),
        BlockRow('mgx', 'mch'),
    ], 'mono1'),
    Block('MIRA2', [
        BlockRow('m2th', 'm2tt'),
        BlockRow('m2tx', 'm2ty', 'm2gx'),
        BlockRow('m2fv', Field(dev='atten1', width=4),
                 Field(dev='atten2', width=4), Field(dev='flip2', width=4)),
        BlockRow(Field(dev='lamfilter', width=4),
                 Field(dev='TBe', width=6), Field(dev='PBe', width=7)),
        BlockRow(Field(dev='ms2pos', width=4),
                 Field(dev='ms2', name='Mono slit 2 (ms2)', width=20, istext=True)),
    ], 'mono2'),
    Block('Environment', [
        BlockRow(Field(name='Power', dev='ReactorPower', format='%.1f', width=7),
                 Field(name='6-fold', dev='Sixfold', min='open', width=7),
                 Field(dev='NL6', min='open', width=7)),
        BlockRow(Field(dev='Shutter', width=7), Field(dev='Cooling', width=6),
                 Field(dev='CoolTemp', width=6, format='%.1f', unit=" "),
                 Field(dev='FAKTemp', width=6, format='%.1f', unit=' '),
                 Field(dev='Crane', min=10, width=7,)),
    ], 'reactor'),
)

_column4 = Column(
    Block('Temperature plots', [
        BlockRow(Field(dev='T', plot='T',
                       plotwindow=12*3600, width=100, height=40),
                 Field(dev='Ts', plot='T'), Field(dev='TBe', name='Filter', plot='T')),
    ], 'ccr5'),
    Block('Magnet temp. plots', [
        BlockRow(Field(dev='m7T5_T1', name='T1', plot='Tm',
                       plotwindow=24*3600, width=100, height=40),
                 Field(dev='m7T5_T2', name='T2', plot='Tm'),
                 Field(dev='m7T5_T3', name='T3', plot='Tm'),
                 Field(dev='m7T5_T4', name='T4', plot='Tm'),
                 Field(dev='B', plot='Tm')),
    ], 'magnet75'),
    Block('Magnet temp. plots', [
        BlockRow(Field(dev='m5T_T2', name='T2', plot='Tm5',
                       plotwindow=24*3600, width=100, height=40),
                 Field(dev='m5T_T3', name='T3', plot='Tm5'),
                 Field(dev='m5T_T4', name='T4', plot='Tm5'),
                 Field(dev='m5T_T5', name='T5', plot='Tm5'),
                 Field(dev='m5T_T6', name='T6', plot='Tm5')),
    ], 'magnet5'),
)


devices = dict(
    Monitor = device('services.monitor.html.Monitor',
                     title = 'MIRA Status monitor',
                     filename = '/miracontrol/status.html',
                     interval = 10,
                     loglevel = 'info',
                     cache = 'mira1:14869',
                     prefix = 'nicos/',
                     font = 'Luxi Sans',
                     valuefont = 'Consolas',
                     fontsize = 17,
                     layout = [[_expcolumn], [_column1, _column2, _column3], [_column4]]),
)
