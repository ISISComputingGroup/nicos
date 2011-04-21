#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Description:
#   NICOS monitor setup file with a few devices
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
#   The basic NICOS methods for the NICOS daemon (http://nicos.sf.net)
#
#   Copyright (C) 2009 Jens Krüger <jens.krueger@frm2.tum.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# *****************************************************************************

name = 'setup for the status monitor'
group = 'special'

_reactor = [
]

_expcolumn = [
    ('Experiment', [
        [{'name': 'Proposal', 'key': 'exp/proposal', 'width': 7},
         {'name': 'Title', 'key': 'exp/title', 'width': 20,
          'istext': True, 'maxlen': 20},
         {'name': 'Current status', 'key': 'exp/action', 'width': 30,
          'istext': True},
         {'name': 'Last file', 'key': 'filesink/lastfilenumber'}]]),
]

_column1 = [
    ('MIEZE', [
        [{'dev': 'freq1', 'name': 'freq1'}, {'dev': 'freq2', 'name': 'freq2'}],
        [{'dev': 'amp1', 'name': 'amp1'},   {'dev': 'amp2', 'name': 'amp2'}],
        [{'dev': 'fp1', 'name': 'FP 1'},    {'dev': 'fp2', 'name': 'FP 2'}],
        [{'dev': 'rp1', 'name': 'RP 1'},    {'dev': 'rp2', 'name': 'RP 2'}],
        '---',
        [{'dev': 'dc1', 'name': 'DC 1'},    {'dev': 'dc2', 'name': 'DC 2'}],
        '---',
        [{'dev': 'freq3', 'name': 'freq3'}, {'dev': 'freq4', 'name': 'freq4'}],
        [{'dev': 'amp3', 'name': 'amp3'},   {'dev': 'amp4', 'name': 'amp4'}],
    ], 'mieze'),
]

_column2 = [
    ('Detector', [
        ['timer', 'ctr1', 'mon1'],
        '---',
        [{'dev': 'MonHV', 'name': 'Mon HV', 'min': 490, 'width': 5},
         {'dev': 'DetHV', 'name': 'Det HV', 'min': 840, 'width': 5},
         {'dev': 'PSDHV', 'name': 'PSD HV', 'min': 2800, 'width': 5}],
    ]),
    ('Sample', [[{'dev': 'om'}, {'dev': 'phi'}],
                [{'dev': 'stx'}, {'dev': 'sty'}, {'dev': 'stz'}],
                [{'dev': 'sgx'}, {'dev': 'sgy'}]]),
    ('Sample environment', [
        [{'key': 't/setpoint', 'name': 'Setpoint', 'unitkey': 't/unit'},
         {'dev': 'TA', 'name': 'Sample'}, 'TB', 'TC'],
    ]),
]

_column3 = [
#    ('MIRA1', [[{'dev': 'FOLin', 'name': 'FOL', 'width': 4},
#                {'dev': 'FlipperMira1in', 'name': 'Flip', 'width': 4}],
#               ['mth', 'mtt'],
#               ['mtx', 'mty'],
#               ['mgx', {'dev': 'mchanger', 'name': 'mch'}],]),

    ('MIRA2', [['m2th', 'm2tt'],
               ['m2tx', 'm2ty', 'm2gx'],
               ['m2fv', {'dev': 'atten1', 'name': 'Att1', 'width': 4},
                {'dev': 'atten2', 'name': 'Att2', 'width': 4},
                {'dev': 'FlipperMira2in', 'name': 'Flip', 'width': 4}],
               [{'dev': 'lamfilter', 'name': 'Be', 'width': 4},
                {'dev': 'TD', 'name': 'Be Temp', 'width': 7, 'max': 50}],
              ]),
    ('Slits', [[{'dev': 's3', 'name': 'Slit 3', 'width': 24, 'istext': True}],
               [{'dev': 's4', 'name': 'Slit 4', 'width': 24, 'istext': True}]]),
#    ('Reactor', [
#        [{'dev': 'Power', 'name': 'Power', 'min': 19, 'format': '%d', 'width': 7},
#         {'dev': 'Sixfold', 'name': '6-fold', 'min': 'open', 'width': 7}],
#        [{'dev': 'NL6', 'name': 'NL6', 'min': 'open', 'width': 7},
#         {'dev': 'Crane', 'min': 10, 'width': 7}],
#    ]),
]

devices = dict(
    Monitor = device('nicos.qmonitor.Monitor',
                     title='MIRA Status monitor',
                     loglevel='debug',
                     server='mira1:14869',
                     prefix='nicos/',
                     font='Luxi Sans',
                     valuefont='Consolas',
                     padding=5,
                     layout=[[_expcolumn], [_column1, _column2, _column3]])
)
