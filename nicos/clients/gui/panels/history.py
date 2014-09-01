#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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
#   Christian Felder <c.felder@fz-juelich.de>
#
# *****************************************************************************

"""NICOS GUI history log window."""

import os
import sys
from time import time as currenttime, localtime, mktime

sys.QT_BACKEND_ORDER = ["PyQt4", "PySide"]

from PyQt4.QtGui import QDialog, QFont, QListWidgetItem, QToolBar, \
    QMenu, QStatusBar, QSizePolicy, QMainWindow, QApplication, QAction
from PyQt4.QtCore import QObject, QTimer, QDateTime, Qt, QByteArray, QSettings, \
    SIGNAL, pyqtSignature as qtsig

import numpy as np
try:
    from nicos.clients.gui.widgets.grplotting import ViewPlot
    _gr_available = True
except ImportError as e:
    from nicos.clients.gui.widgets.qwtplotting import ViewPlot
    _gr_available = False
    _import_error = e

from nicos.core import Param, listof
from nicos.utils import safeFilename
from nicos.clients.gui.panels import Panel
from nicos.clients.gui.utils import loadUi, dialogFromUi, DlgUtils
from nicos.protocols.cache import cache_load
from nicos.devices.cacheclient import CacheClient
from nicos.pycompat import cPickle as pickle, iteritems, string_types


class View(QObject):
    def __init__(self, parent, name, keys, interval, fromtime, totime,
                 yfrom, yto, window, dlginfo, query_func):
        QObject.__init__(self, parent)
        self.name = name
        self.dlginfo = dlginfo
        self.keys = keys
        self.interval = interval
        self.window = window
        self.fromtime = fromtime
        self.totime = totime
        self.yfrom = yfrom
        self.yto = yto

        self.keyinfo = {}

        if self.fromtime is not None:
            self.keydata = {}
            totime = self.totime or currenttime()
            for key in keys:
                string_mapping = {}
                history = query_func(key, self.fromtime, totime)
                if history is None:
                    from nicos.clients.gui.main import log
                    log.error('Error getting history for %s.', key)
                    history = []
                ltime = 0
                lvalue = None
                interval = self.interval
                maxdelta = max(2 * interval, 11)
                x, y = np.zeros(2 * len(history)), np.zeros(2 * len(history))
                i = 0
                for vtime, value in history:
                    if value is None:
                        continue
                    delta = vtime - ltime
                    if delta < interval:
                        # value comes too fast -> ignore
                        continue
                    if isinstance(value, string_types):
                        # create a new unique integer value for the string
                        value = string_mapping.setdefault(
                            value, len(string_mapping))
                    if delta > maxdelta and lvalue is not None:
                        # synthesize a point inbetween
                        x[i] = vtime - interval
                        y[i] = lvalue
                        i += 1
                    x[i] = ltime = max(vtime, fromtime)
                    y[i] = lvalue = value
                    i += 1
                x.resize((2 * i or 100,))
                y.resize((2 * i or 100,))
                # keydata is a list of five items: x value array, y value array,
                # index of last value, index of last "real" value (not counting
                # synthesized points from the timer, see below), last received
                # value (even if thrown away)
                self.keydata[key] = [x, y, i, i, lvalue]
                if string_mapping:
                    self.keyinfo[key] = ', '.join('%s=%s' % (v, k) for (k, v) in
                                                  iteritems(string_mapping))
        else:
            self.keydata = dict((key, [np.zeros(500), np.zeros(500), 0, 0, None])
                                for key in keys)

        self.listitem = None
        self.plot = None
        if self.totime is None:
            # add another point with the same value every interval time (but not
            # more often than 11 seconds)
            self.timer = QTimer(self, interval=max(interval, 11) * 1000)
            self.timer.timeout.connect(self.on_timer_timeout)
            self.timer.start()

    def on_timer_timeout(self):
        for key, kd in iteritems(self.keydata):
            if kd[0][kd[2]-1] < currenttime() - self.interval:
                self.newValue(currenttime(), key, '=', kd[4], real=False)

    def newValue(self, vtime, key, op, value, real=True):
        if op != '=':
            return
        kd = self.keydata[key]
        n = kd[2]
        real_n = kd[3]
        kd[4] = value
        if real_n > 0 and kd[0][real_n-1] > vtime - self.interval:
            return
        # double array size if array is full
        if n == kd[0].shape[0]:
            # we select a certain maximum # of points to avoid filling up memory
            # and taking forever to update
            if kd[0].shape[0] > 5000:
                # don't add more points, make existing ones more sparse
                kd[0][:n/2] = kd[0][1::2]
                kd[1][:n/2] = kd[1][1::2]
                n = kd[2] = kd[3] = n / 2
            else:
                kd[0].resize((2 * kd[0].shape[0],))
                kd[1].resize((2 * kd[1].shape[0],))
        # fill next entry
        if not real and real_n < n:
            # do not generate endless amounts of synthesized points, one
            # is enough
            kd[0][n-1] = vtime
            kd[1][n-1] = value
        else:
            kd[0][n] = vtime
            kd[1][n] = value
            kd[2] += 1
            if real:
                kd[3] = kd[2]
        # check sliding window
        if self.window:
            i = -1
            threshold = vtime - self.window
            while kd[0][i+1] < threshold and i < n:
                if kd[0][i+2] > threshold:
                    kd[0][i+1] = threshold
                    break
                i += 1
            if i >= 0:
                kd[0][0:n - i] = kd[0][i+1:n+1].copy()
                kd[1][0:n - i] = kd[1][i+1:n+1].copy()
                kd[2] -= i+1
                kd[3] -= i+1
        if self.plot:
            self.plot.pointsAdded(key)


class NewViewDialog(QDialog, DlgUtils):

    def __init__(self, parent, info=None, devlist=None):
        QDialog.__init__(self, parent)
        DlgUtils.__init__(self, 'History viewer')
        loadUi(self, 'history_new.ui', 'panels')

        self.fromdate.setDateTime(QDateTime.currentDateTime())
        self.todate.setDateTime(QDateTime.currentDateTime())

        self.connect(self.customY, SIGNAL('toggled(bool)'), self.toggleCustomY)
        self.toggleCustomY(False)

        if devlist:
            self.devices.addItems(devlist)

        self.connect(self.simpleTime, SIGNAL('toggled(bool)'), self.toggleSimpleExt)
        self.connect(self.extTime, SIGNAL('toggled(bool)'), self.toggleSimpleExt)
        self.connect(self.frombox, SIGNAL('toggled(bool)'), self.toggleSimpleExt)
        self.connect(self.tobox, SIGNAL('toggled(bool)'), self.toggleSimpleExt)
        self.toggleSimpleExt(True)

        self.connect(self.simpleTimeSpec,
                     SIGNAL('textChanged(const QString&)'),
                     self.setIntervalFromSimple)

        self.connect(self.helpButton, SIGNAL('clicked()'), self.showDeviceHelp)
        self.connect(self.simpleHelpButton, SIGNAL('clicked()'),
                     self.showSimpleHelp)

        if info is not None:
            self.devices.setEditText(info['devices'])
            self.namebox.setText(info['name'])
            self.simpleTime.setChecked(info['simpleTime'])
            self.simpleTimeSpec.setText(info['simpleTimeSpec'])
            self.slidingWindow.setChecked(info['slidingWindow'])
            self.frombox.setChecked(info['frombox'])
            self.tobox.setChecked(info['tobox'])
            self.fromdate.setDateTime(QDateTime.fromTime_t(info['fromdate']))
            self.todate.setDateTime(QDateTime.fromTime_t(info['todate']))
            self.interval.setText(info['interval'])
            self.customY.setChecked(info['customY'])
            self.customYFrom.setText(info['customYFrom'])
            self.customYTo.setText(info['customYTo'])

    def showSimpleHelp(self):
        self.showInfo('Please enter a time interval with unit like this:\n\n'
            '30m   (30 minutes)\n'
            '12h   (12 hours)\n'
            '3d    (3 days)\n')

    def showDeviceHelp(self):
        self.showInfo('Enter a comma-separated list of device names or '
            'parameters (as "device.parameter").  Example:\n\n'
            'T, T.setpoint\n\nshows the value of device T, and the value '
            'of the T.setpoint parameter.')

    def toggleCustomY(self, on):
        self.customYFrom.setEnabled(on)
        self.customYTo.setEnabled(on)
        if on:
            self.customYFrom.setFocus()

    def toggleSimpleExt(self, on):
        on = self.simpleTime.isChecked()
        self.simpleTimeSpec.setEnabled(on)
        self.slidingWindow.setEnabled(on)
        self.frombox.setEnabled(not on)
        self.fromdate.setEnabled(not on and self.frombox.isChecked())
        self.tobox.setEnabled(not on)
        self.todate.setEnabled(not on and self.tobox.isChecked())

    def setIntervalFromSimple(self, text):
        try:
            _itime, interval = parseTimeSpec(text)
        except Exception:
            pass
        else:
            self.interval.setText(str(interval))

    def accept(self):
        if self.simpleTime.isChecked():
            try:
                parseTimeSpec(self.simpleTimeSpec.text())
            except ValueError:
                self.showSimpleHelp()
                return
        if self.customY.isChecked():
            try:
                float(self.customYFrom.text())
            except ValueError:
                self.showError('You have to input valid y axis limits.')
                return
            try:
                float(self.customYTo.text())
            except ValueError:
                self.showError('You have to input valid y axis limits.')
                return
        return QDialog.accept(self)

    def infoDict(self):
        return dict(
            devices = self.devices.currentText(),
            name = self.namebox.text(),
            simpleTime = self.simpleTime.isChecked(),
            simpleTimeSpec = self.simpleTimeSpec.text(),
            slidingWindow = self.slidingWindow.isChecked(),
            frombox = self.frombox.isChecked(),
            tobox = self.tobox.isChecked(),
            fromdate = self.fromdate.dateTime().toTime_t(),
            todate = self.todate.dateTime().toTime_t(),
            interval = self.interval.text(),
            customY = self.customY.isChecked(),
            customYFrom = self.customYFrom.text(),
            customYTo = self.customYTo.text(),
        )


class BaseHistoryWindow(object):

    def __init__(self):
        loadUi(self, 'history.ui', 'panels')

        self.user_color = Qt.white
        self.user_font = QFont('monospace')

        self.views = []
        # stack of views to display
        self.viewStack = []
        # maps watched keys to their views
        self.keyviews = {}
        # current plot object
        self.currentPlot = None

        self.enablePlotActions(False)

    def openViews(self, views):
        """Open some views given by the specs in *views*, a list of strings.

        Each string can be a comma-separated list of key names, and an optional
        simple time spec (like "1h") separated by a colon.

        If a view spec matches the name of a preset, it is used instead.
        """
        for viewspec in views:
            timespec = '1h'
            if ':' in viewspec:
                viewspec, timespec = viewspec.rsplit(':', 1)
            info = dict(
                name = viewspec,
                devices = viewspec,
                simpleTime = True,
                simpleTimeSpec = timespec,
                slidingWindow = True,
                frombox = False,
                tobox = False,
                fromdate = 0,
                todate = 0,
                interval = '',
                customY = False,
                customYFrom = '',
                customYTo = '',
            )
            self._createViewFromDialog(info)

    def addPreset(self, name, info):
        # overridden in the Panel
        pass

    def enablePlotActions(self, on):
        for action in [
            self.actionSavePlot, self.actionPrint, self.actionAttachElog,
            self.actionSaveData, self.actionAutoScale,
            self.actionEditView, self.actionCloseView, self.actionDeleteView,
            self.actionResetView,
            self.actionUnzoom, self.actionLogScale, self.actionLegend,
            self.actionSymbols, self.actionLines, self.actionLinearFit,
            ]:
            action.setEnabled(on)

    def on_viewList_currentItemChanged(self, item, previous):
        if item is None:
            return
        for view in self.views:
            if view.listitem == item:
                self.openView(view)

    def on_viewList_itemClicked(self, item):
        # this handler is needed in addition to currentItemChanged
        # since one can't change the current item if it's the only one
        self.on_viewList_currentItemChanged(item, None)

    def on_logYinDomain(self, flag):
        if not flag:
            self.actionLogScale.setChecked(flag)

    def newvalue_callback(self, data):
        (vtime, key, op, value) = data
        if key not in self.keyviews:
            return
        value = cache_load(value)
        for view in self.keyviews[key]:
            view.newValue(vtime, key, op, value)

    def _createViewFromDialog(self, info):
        parts = [part.strip().lower().replace('.', '/')
                 for part in info['devices'].split(',')]
        if not parts:
            return
        keys = [part if '/' in part else part + '/value' for part in parts]
        name = info['name']
        if not name:
            name = info['devices']
            if info['simpleTime']:
                name += ' (%s)' % info['simpleTimeSpec']
        window = None
        if info['simpleTime']:
            try:
                itime, _ = parseTimeSpec(info['simpleTimeSpec'])
            except ValueError:
                return
            fromtime = currenttime() - itime
            totime = None
            if info['slidingWindow']:
                window = itime
        else:
            if info['frombox']:
                fromtime = mktime(localtime(info['fromdate']))
            else:
                fromtime = None
            if info['tobox']:
                totime = mktime(localtime(info['todate']))
            else:
                totime = None
        try:
            interval = float(info['interval'])
        except ValueError:
            interval = 5.0
        if info['customY']:
            try:
                yfrom = float(info['customYFrom'])
            except ValueError:
                return
            try:
                yto = float(info['customYTo'])
            except ValueError:
                return
        else:
            yfrom = yto = None
        view = View(self, name, keys, interval, fromtime, totime, yfrom, yto,
                    window, info, self.gethistory_callback)
        self.views.append(view)
        view.listitem = QListWidgetItem(view.name, self.viewList)
        self.openView(view)
        if view.totime is None:
            for key in view.keys:
                self.keyviews.setdefault(key, []).append(view)

    @qtsig('')
    def on_actionNew_triggered(self):
        self.showNewDialog()

    def showNewDialog(self, devices=''):
        devlist = []
        if hasattr(self, 'client'):
            devlist = self.client.getDeviceList()
        newdlg = NewViewDialog(self, devlist=devlist)
        newdlg.devices.setEditText(devices)
        ret = newdlg.exec_()
        if ret != QDialog.Accepted:
            return
        info = newdlg.infoDict()
        self._createViewFromDialog(info)
        if newdlg.savePreset.isChecked():
            self.addPreset(info['name'], info)

    def newView(self, devices):
        newdlg = NewViewDialog(self)
        newdlg.devices.setEditText(devices)
        info = newdlg.infoDict()
        self._createViewFromDialog(info)

    def openView(self, view):
        if not view.plot:
            view.plot = ViewPlot(self.plotFrame, self, view)
        self.viewList.setCurrentItem(view.listitem)
        self.setCurrentView(view)

    def setCurrentView(self, view):
        if self.currentPlot:
            self.plotLayout.removeWidget(self.currentPlot)
            self.currentPlot.hide()
        if view is None:
            self.currentPlot = None
            self.enablePlotActions(False)
        else:
            self.currentPlot = view.plot
            try: self.viewStack.remove(view)
            except ValueError: pass
            self.viewStack.append(view)

            self.enablePlotActions(True)
            self.viewList.setCurrentItem(view.listitem)
            self.actionLogScale.setChecked(view.plot.isLogScaling())
            self.actionLegend.setChecked(view.plot.isLegendEnabled())
            self.actionSymbols.setChecked(view.plot.hasSymbols)
            self.actionLines.setChecked(view.plot.hasLines)
            self.plotLayout.addWidget(view.plot)
            if _gr_available:
                view.plot.setAutoScale(True)
                view.plot.logYinDomain.connect(self.on_logYinDomain)
                self.actionAutoScale.setChecked(True)
            else:
                self.actionAutoScale.setEnabled(False)
            view.plot.show()

    @qtsig('')
    def on_actionEditView_triggered(self):
        view = self.viewStack[-1]
        newdlg = NewViewDialog(self, view.dlginfo)
        newdlg.setWindowTitle('Edit history view')
        ret = newdlg.exec_()
        if ret != QDialog.Accepted:
            return
        info = newdlg.infoDict()
        if newdlg.savePreset.isChecked():
            self.addPreset(info['name'], info)
        self.viewStack.pop()
        self.clearView(view)
        self.setCurrentView(None)
        self._createViewFromDialog(info)

    @qtsig('')
    def on_actionCloseView_triggered(self):
        view = self.viewStack.pop()
        if self.viewStack:
            self.setCurrentView(self.viewStack[-1])
        else:
            self.setCurrentView(None)
        view.plot = None

    @qtsig('')
    def on_actionResetView_triggered(self):
        view = self.viewStack.pop()
        hassym = view.plot.hasSymbols
        view.plot = None
        self.openView(view)
        self.actionSymbols.setChecked(hassym)
        view.plot.setSymbols(hassym)

    @qtsig('')
    def on_actionDeleteView_triggered(self):
        view = self.viewStack.pop()
        self.clearView(view)
        if self.viewStack:
            self.setCurrentView(self.viewStack[-1])
        else:
            self.setCurrentView(None)

    def clearView(self, view):
        self.views.remove(view)
        for i in range(self.viewList.count()):
            if self.viewList.item(i) == view.listitem:
                self.viewList.takeItem(i)
                break
        if view.totime is None:
            for key in view.keys:
                self.keyviews[key].remove(view)

    @qtsig('')
    def on_actionSavePlot_triggered(self):
        filename = self.currentPlot.savePlot()
        if filename:
            self.statusBar.showMessage('View successfully saved to %s.' %
                                       filename)

    @qtsig('')
    def on_actionPrint_triggered(self):
        if self.currentPlot.printPlot():
            self.statusBar.showMessage('View successfully printed.')

    @qtsig('')
    def on_actionUnzoom_triggered(self):
        if _gr_available:
            self.currentPlot._plot.reset()
            self.currentPlot.update()
        else:
            self.currentPlot.zoomer.zoom(0)

    @qtsig('bool')
    def on_actionLogScale_toggled(self, on):
        self.currentPlot.setLogScale(on)

    @qtsig('bool')
    def on_actionLegend_toggled(self, on):
        self.currentPlot.setLegend(on)

    @qtsig('bool')
    def on_actionSymbols_toggled(self, on):
        self.currentPlot.setSymbols(on)

    @qtsig('bool')
    def on_actionLines_toggled(self, on):
        self.currentPlot.setLines(on)

    @qtsig('')
    def on_actionLinearFit_triggered(self):
        self.currentPlot.fitLinear()

    @qtsig('')
    def on_actionSaveData_triggered(self):
        self.currentPlot.saveData()


class HistoryPanel(Panel, BaseHistoryWindow):
    panelName = 'History viewer'

    def __init__(self, parent, client):
        self.presetdict = {}

        Panel.__init__(self, parent, client)
        BaseHistoryWindow.__init__(self)

        self.presetmenu = QMenu('&Presets', self)
        self.statusBar = QStatusBar(self)
        policy = self.statusBar.sizePolicy()
        policy.setVerticalPolicy(QSizePolicy.Fixed)
        self.statusBar.setSizePolicy(policy)
        self.statusBar.setSizeGripEnabled(False)
        self.layout().addWidget(self.statusBar)

        self.menus = None
        self.bar = None

        self.splitter.restoreState(self.splitterstate)
        self.connect(self.client, SIGNAL('cache'), self.newvalue_callback)

    def getMenus(self):
        menu = QMenu('&History viewer', self)
        menu.addAction(self.actionNew)
        menu.addSeparator()
        menu.addAction(self.actionSavePlot)
        menu.addAction(self.actionPrint)
        menu.addAction(self.actionAttachElog)
        menu.addAction(self.actionSaveData)
        menu.addSeparator()
        menu.addAction(self.actionEditView)
        menu.addAction(self.actionCloseView)
        menu.addAction(self.actionDeleteView)
        menu.addAction(self.actionResetView)
        menu.addSeparator()
        menu.addAction(self.actionLogScale)
        menu.addAction(self.actionAutoScale)
        menu.addAction(self.actionUnzoom)
        menu.addAction(self.actionLegend)
        menu.addAction(self.actionSymbols)
        menu.addAction(self.actionLines)
        menu.addAction(self.actionLinearFit)
        menu.addSeparator()
        self._refresh_presets()
        return [menu, self.presetmenu]

    def _refresh_presets(self):
        pmenu = self.presetmenu
        pmenu.clear()
        delmenu = QMenu('Delete', self)
        try:
            for preset, info in iteritems(self.presetdict):
                paction = QAction(preset, self)
                pdelaction = QAction(preset, self)
                info = pickle.loads(str(info))
                def launchpreset(on, info=info):
                    self._createViewFromDialog(info)
                def delpreset(on, name=preset, pact=paction, pdelact=pdelaction):
                    pmenu.removeAction(pact)
                    delmenu.removeAction(pdelact)
                    self.presetdict.pop(name, None)
                    self._refresh_presets()
                self.connect(paction, SIGNAL('triggered(bool)'), launchpreset)
                pmenu.addAction(paction)
                self.connect(pdelaction, SIGNAL('triggered(bool)'), delpreset)
                delmenu.addAction(pdelaction)
        except AttributeError:
            self.presetdict = {}
        if self.presetdict:
            pmenu.addSeparator()
            pmenu.addMenu(delmenu)
        else:
            pmenu.addAction('(no presets created)')

    def getToolbars(self):
        if not self.bar:
            bar = QToolBar('History viewer')
            bar.addAction(self.actionNew)
            bar.addAction(self.actionEditView)
            bar.addSeparator()
            bar.addAction(self.actionSavePlot)
            bar.addAction(self.actionPrint)
            bar.addAction(self.actionSaveData)
            bar.addSeparator()
            bar.addAction(self.actionUnzoom)
            bar.addAction(self.actionLogScale)
            bar.addAction(self.actionAutoScale)
            bar.addSeparator()
            bar.addAction(self.actionResetView)
            bar.addAction(self.actionDeleteView)
            self.bar = bar

        return [self.bar]

    def loadSettings(self, settings):
        self.splitterstate = settings.value('splitter', b'', QByteArray)
        presetval = settings.value('presets')
        if presetval is not None:
            # there may be a problem reading the preset value...
            try:
                self.presetdict = presetval
            except TypeError:
                self.presetdict = {}
        else:
            self.presetdict = {}

    def saveSettings(self, settings):
        settings.setValue('splitter', self.splitter.saveState())
        settings.setValue('presets', self.presetdict)

    def setCustomStyle(self, font, back):
        self.user_font = font
        self.user_color = back

        for view in self.views:
            if view.plot:
                view.plot.setCanvasBackground(back)
                view.plot.replot()

        bold = QFont(font)
        bold.setBold(True)
        larger = QFont(font)
        larger.setPointSize(font.pointSize() * 1.6)
        for view in self.views:
            if view.plot:
                view.plot.setFonts(font, bold, larger)

    def requestClose(self):
        # Always succeeds, but break up circular references so that the panel
        # object can be deleted properly.
        for v in self.views:
            v.plot = None
        self.currentPlot = None
        return True

    def addPreset(self, name, info):
        if name:
            self.presetdict[name] = pickle.dumps(info)
            self._refresh_presets()

    def gethistory_callback(self, key, fromtime, totime):
        return self.client.ask('gethistory', key, str(fromtime), str(totime))

    @qtsig('')
    def on_actionAttachElog_triggered(self):
        newdlg = dialogFromUi(self, 'plot_attach.ui', 'panels')
        suffix = ".svg" if _gr_available else ".png"
        newdlg.filename.setText(
            safeFilename("history_%s" % self.currentPlot.view.name + suffix))
        ret = newdlg.exec_()
        if ret != QDialog.Accepted:
            return
        descr = newdlg.description.text()
        fname = newdlg.filename.text()
        if _gr_available:
            pathname = self.currentPlot.saveSvg()
        else:
            pathname = self.currentPlot.savePng()
        with open(pathname, 'rb') as fp:
            remotefn = self.client.ask('transfer', fp.read())
        self.client.eval('_LogAttach(%r, [%r], [%r])' % (descr, remotefn, fname))
        os.unlink(pathname)

    @qtsig('bool')
    def on_actionAutoScale_toggled(self, on):
        if self.currentPlot:
            self.currentPlot.setAutoScale(on)
            self.currentPlot.update()


class StandaloneHistoryWindow(QMainWindow, BaseHistoryWindow, DlgUtils):

    def __init__(self, app):
        QMainWindow.__init__(self, None)
        BaseHistoryWindow.__init__(self)
        DlgUtils.__init__(self, 'History viewer')

        self.settings = QSettings()
        self.splitter.restoreState(
            self.settings.value('splitstate', QByteArray()))

        self.app = app
        self.setCentralWidget(self.splitter)
        self.connect(self, SIGNAL('newvalue'), self.newvalue_callback)

        self.menus = None
        self.bar = None

        for toolbar in self.getToolbars():
            self.addToolBar(toolbar)
        for menu in self.getMenus():
            self.menuBar().addMenu(menu)
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def getMenus(self):
        if not self.menus:
            menu = QMenu('&History viewer', self)
            menu.addAction(self.actionNew)
            menu.addSeparator()
            menu.addAction(self.actionSavePlot)
            menu.addAction(self.actionPrint)
            menu.addAction(self.actionSaveData)
            menu.addSeparator()
            menu.addAction(self.actionEditView)
            menu.addAction(self.actionCloseView)
            menu.addAction(self.actionDeleteView)
            menu.addAction(self.actionResetView)
            menu.addSeparator()
            menu.addAction(self.actionLogScale)
            menu.addAction(self.actionUnzoom)
            menu.addAction(self.actionLegend)
            menu.addAction(self.actionSymbols)
            menu.addAction(self.actionLines)
            menu.addAction(self.actionLinearFit)
            menu.addSeparator()
            menu.addAction(self.actionClose)
            self.menus = menu

        return [self.menus]

    def getToolbars(self):
        if not self.bar:
            bar = QToolBar('History viewer')
            bar.addAction(self.actionNew)
            bar.addAction(self.actionEditView)
            bar.addSeparator()
            bar.addAction(self.actionSavePlot)
            bar.addAction(self.actionPrint)
            bar.addAction(self.actionSaveData)
            bar.addAction(self.actionClose)
            bar.addSeparator()
            bar.addAction(self.actionUnzoom)
            bar.addAction(self.actionLogScale)
            bar.addSeparator()
            bar.addAction(self.actionResetView)
            bar.addAction(self.actionDeleteView)
            self.bar = bar

        return [self.bar]

    def gethistory_callback(self, key, fromtime, totime):
        return self.app.history(None, key, fromtime, totime)

    def closeEvent(self, event):
        self.settings.setValue('splitstate', self.splitter.saveState())
        return QMainWindow.closeEvent(self, event)


class StandaloneHistoryApp(CacheClient):

    parameters = {
        'views': Param('Strings specifying views (from command line)',
                       type=listof(str)),
    }

    def doInit(self, mode):
        import nicos.guisupport.gui_rc  #pylint: disable=W0612

        self._qtapp = QApplication(sys.argv)
        self._qtapp.setOrganizationName('nicos')
        self._qtapp.setApplicationName('history')
        self._window = StandaloneHistoryWindow(self)
        CacheClient.doInit(self, mode)

    def start(self):
        self._window.openViews(self.views)
        self._window.show()
        try:
            self._qtapp.exec_()
        except KeyboardInterrupt:
            pass
        self._stoprequest = True

    def _propagate(self, data):
        self._window.emit(SIGNAL('newvalue'), data)


def parseTimeSpec(intv):
    if not intv:
        itime = 0
    elif intv.endswith('sec'):
        itime = float(intv[:-3])
    elif intv.endswith('s'):
        itime = float(intv[:-1])
    elif intv.endswith('min'):
        itime = float(intv[:-3]) * 60
    elif intv.endswith('m'):
        itime = float(intv[:-1]) * 60
    elif intv.endswith('h'):
        itime = float(intv[:-1]) * 3600
    elif intv.endswith('days'):
        itime = float(intv[:-4]) * 24 * 3600
    elif intv.endswith('d'):
        itime = float(intv[:-1]) * 24 * 3600
    elif intv.endswith('y'):
        itime = float(intv[:-1]) * 24 * 3600 * 365
    else:
        raise ValueError
    itime = abs(itime)
    if itime >= 24 * 3600:
        interval = 30
    elif itime >= 6 * 3600:
        interval = 10
    elif itime >= 3 * 3600:
        interval = 5
    elif itime >= 1800:
        interval = 2
    else:
        interval = 1
    return itime, interval
