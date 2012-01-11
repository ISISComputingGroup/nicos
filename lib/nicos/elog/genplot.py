#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""Generate quick overview plots of scans, using Gnuplot."""

__version__ = "$Revision$"

import os


def plotDataset(dataset, fn):
    gp = os.popen('gnuplot', 'w')
    gp.write('set terminal svg size 600,400 dashed\n')
    gp.write('set xlabel "%s (%s)"\n' % (dataset.xnames[dataset.xindex],
                                         dataset.xunits[dataset.xindex]))
    gp.write('set title "Scan %s - %s"\n' %
             (dataset.sinkinfo.get('number', ''), dataset.scaninfo))
    gp.write('set grid lt 3 lc 8\n')
    gp.write('set style increment user\n')
    for ls, pt in enumerate([7, 5, 9, 11, 13, 2, 1, 3]):
        gp.write('set style line %d lt 1 lc %d pt %d\n' % (ls+1, ls+1, pt))

    data = []
    for xv, yv in zip(dataset.xresults, dataset.yresults):
        data.append('%s %s' % (xv[dataset.xindex], ' '.join(map(str, yv))))
    data = '\n'.join(data) + '\ne\n'

    plotterms = []
    ylabels = []
    yunits = set()
    for i, (name, info) in enumerate(zip(dataset.ynames, dataset.yvalueinfo)):
        if info.type in ('info', 'error', 'time', 'monitor'):
            continue
        term = '"-"'
        if info.errors == 'sqrt':
            term += ' using 1:%d:(sqrt($%d))' % (i+2, i+2)
        elif info.errors == 'next':
            term += ' using 1:%d:%d' % (i+2, i+3)
        else:
            term += ' using 1:%d' % (i+2)
        term += ' title "%s (%s)"' % (name, info.unit)
        if info.type == 'other':
            term += ' axes x1y2'
        term += ' with errorlines'
        plotterms.append(term)
        ylabels.append('%s (%s)' % (name, info.unit))
        yunits.add(info.unit)

    if len(ylabels) == 1:
        gp.write('set ylabel "%s"\n' % ylabels[0])
        gp.write('set key off\n')
    else:
        if len(yunits) == 1:
            gp.write('set ylabel "%s"\n' % yunits.pop())
        gp.write('set key outside below\n')

    gp.write('set output "%s-lin.svg"\n' % fn)
    gp.write('plot %s\n' % ', '.join(plotterms))
    for i in range(len(plotterms)):
        gp.write(data)

    gp.write('set output "%s-log.svg"\n' % fn)
    gp.write('set logscale y\n')
    gp.write('plot %s\n' % ', '.join(plotterms))
    for i in range(len(plotterms)):
        gp.write(data)
