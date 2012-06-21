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

"""NICOS livewidget 2D data plot window/panel."""

from __future__ import with_statement

__version__ = "$Revision$"

from PyQt4.QtCore import Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtCore import pyqtSignature as qtsig
from PyQt4.QtGui import QPrinter, QPrintDialog, QDialog, QMainWindow, \
     QMenu, QToolBar, QStatusBar, QSizePolicy, QListWidgetItem, QLabel

from nicos.gui.utils import loadUi
from nicos.gui.panels import Panel
from nicos.gui.livewidget import LWWidget, LWData, Logscale, \
     MinimumMaximum, BrightnessContrast, Integrate, Histogram

DATATYPES = frozenset(('<I4', '<i4', '>I4', '>i4', '<I2', '<i2', '>I2', '>i2',
                       'I1', 'i1', 'f8', 'f4'))


class LiveDataPanel(Panel):
    panelName = 'Live data view'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        loadUi(self, 'live.ui', 'panels')

        self._format = None
        self._runtime = 0
        self._no_direct_display = False
        self._range_active = False

        self.statusBar = QStatusBar(self)
        policy = self.statusBar.sizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Fixed)
        self.statusBar.setSizePolicy(policy)
        self.statusBar.setSizeGripEnabled(False)
        self.layout().addWidget(self.statusBar)

        self.widget = LWWidget(self)
        self.widget.setAxisLabels('time channels', 'detectors')
        self.widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.setKeepAspect(False)
        self.widget.setControls(Logscale | MinimumMaximum | BrightnessContrast |
                                Integrate | Histogram)
        self.widgetLayout.addWidget(self.widget)

        self.liveitem = QListWidgetItem('<Live>', self.fileList)
        self.liveitem.setData(32, '')
        self.liveitem.setData(33, '')

        self.splitter.restoreState(self.splitterstate)

        self.connect(client, SIGNAL('livedata'), self.on_client_livedata)
        self.connect(client, SIGNAL('liveparams'), self.on_client_liveparams)
        if client.connected:
            self.on_client_connected()
        self.connect(client, SIGNAL('connected'), self.on_client_connected)

        self.connect(self.actionLogScale, SIGNAL("toggled(bool)"),
                     self.widget, SLOT("setLog10(bool)"))
        self.connect(self.widget,
                     SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.on_widget_customContextMenuRequested)
        self.connect(self.widget,
                     SIGNAL('profilePointPicked(int, double, double)'),
                     self.on_widget_profilePointPicked)

    def setSettings(self, settings):
        self._instrument = settings.get('instrument', '')
        if 'instrument' in settings:
            self.widget.setInstrumentOption(settings['instrument'])

    def loadSettings(self, settings):
        self.splitterstate = settings.value('splitter').toByteArray()

    def saveSettings(self, settings):
        settings.setValue('splitter', self.splitter.saveState())

    def getMenus(self):
        self.menu = menu = QMenu('&Live data', self)
        menu.addAction(self.actionPrint)
        menu.addSeparator()
        menu.addAction(self.actionSetAsROI)
        menu.addAction(self.actionUnzoom)
        menu.addAction(self.actionLogScale)
        menu.addAction(self.actionNormalized)
        menu.addAction(self.actionLegend)
        return [menu]

    def getToolbars(self):
        bar = QToolBar('Live data')
        bar.addAction(self.actionPrint)
        bar.addSeparator()
        bar.addAction(self.actionLogScale)
        bar.addSeparator()
        bar.addAction(self.actionUnzoom)
        #bar.addAction(self.actionSetAsROI)
        return [bar]

    def on_widget_customContextMenuRequested(self, point):
        self.menu.popup(self.mapToGlobal(point))

    def on_widget_profilePointPicked(self, type, x, y):
        if self._instrument.lower() != 'toftof' or type != 0:
            return
        if not hasattr(self, '_toftof_detinfo'):
            info = self.client.eval('m._detinfo_parsed, m._anglemap', None)
            if info is None:
                return self.showError('Cannot retrieve detector info.')
            self._toftof_detinfo, self._toftof_anglemap = info
            self._toftof_inverse_anglemap = 0
            self._toftof_infowindow = QMainWindow(self)
            self._toftof_label = QLabel(self._toftof_infowindow)
            self._toftof_infowindow.setCentralWidget(self._toftof_label)
            self._toftof_infowindow.setContentsMargins(10, 10, 10, 10)
        detnr = int(x - 0.5)
        detentry = self._toftof_anglemap[detnr]
        self._toftof_infowindow.show()
        self._toftof_label.setTextFormat(Qt.RichText)
        entrynames = ['EntryNr', 'Rack', 'Plate', 'Pos', 'RPos',
                      '2Theta', 'CableNr', 'CableType', 'CableLen', 'CableEmpty',
                      'Card', 'Chan', 'Total', 'DetName', 'BoxNr', 'BoxChan']
        formats = ['%s', '%d', '%d', '%d', '%d', '%.3f', '%d', '%d', '%.2f',
                   '%d', '%d', '%d', '%d', '%r', '%d', '%d']
        empties = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
        self._toftof_label.setText(
            'Detector info:<br><table>' +
            ''.join('<tr><td>%s</td><td></td><td>%s</td></tr>%s' %
                    (name, format % value, '<tr></tr>' if empty else '')
                    for (name, format, empty, value)
                    in zip(entrynames, formats, empties,
                           self._toftof_detinfo[detentry])) +
            '</table>')

    def on_client_connected(self):
        pass
    #     datapath = self.client.eval('session.experiment.datapath', [])
    #     caspath = path.join(datapath[0], 'cascade')
    #     if path.isdir(caspath):
    #         for fn in sorted(os.listdir(caspath)):
    #             if fn.endswith('.pad'):
    #                 self.add_to_flist(path.join(caspath, fn), 'pad', False)
    #             elif fn.endswith('tof'):
    #                 self.add_to_flist(path.join(caspath, fn), 'tof', False)

    def on_client_liveparams(self, params):
        tag, fname, dtype, nx, ny, nz, runtime = params
        self._runtime = runtime
        if dtype not in DATATYPES:
            self._format = None
            print 'Unsupported live data format:', params
            return
        self._format = dtype
        self._nx = nx
        self._ny = ny
        self._nz = nz

    def on_client_livedata(self, data):
        if self._format:
            self.widget.setData(
                LWData(self._nx, self._ny, self._nz, self._format, data))

    #@qtsig('')
    #def on_actionSetAsROI_triggered(self):
    #    zoom = self.widget.plot().getZoomer().zoomRect()

    @qtsig('')
    def on_actionUnzoom_triggered(self):
        self.widget.plot().getZoomer().zoom(0)

    @qtsig('')
    def on_actionPrint_triggered(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setColorMode(QPrinter.Color)
        printer.setOrientation(QPrinter.Landscape)
        printer.setOutputFileName('')
        if QPrintDialog(printer, self).exec_() == QDialog.Accepted:
            self.widget.plot().print_(printer)

    def closeEvent(self, event):
        with self.sgroup as settings:
            settings.setValue('geometry', QVariant(self.saveGeometry()))
        event.accept()
        self.emit(SIGNAL('closed'), self)
