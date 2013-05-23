#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2013 by the NICOS contributors (see AUTHORS)
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

"""Qt version of instrument monitor."""

import threading
from time import sleep

from PyQt4 import uic
from PyQt4.QtGui import QFrame, QLabel, QPalette, QMainWindow, QVBoxLayout, \
     QColor, QFont, QFontMetrics, QSizePolicy, QHBoxLayout, QApplication, \
     QCursor
from PyQt4.QtCore import Qt, SIGNAL

from nicos.services.monitor import Monitor as BaseMonitor
from nicos.guisupport.widget import DisplayWidget
from nicos.guisupport.display import ValueDisplay
from nicos.guisupport.plots import TrendPlot, plot_available


class MonitorWindow(QMainWindow):
    def keyPressEvent(self, event):
        if event.text() == 'q':
            self.close()
        return QMainWindow.keyPressEvent(self, event)


class BlockBox(QFrame):
    """Provide the equivalent of a Tk LabelFrame: a group box that has a
    definite frame around it.
    """
    def __init__(self, parent, text, font):
        QFrame.__init__(self, parent, frameShape=QFrame.Panel,
                        frameShadow=QFrame.Raised, lineWidth=2)
        self._label = QLabel(' ' + text + ' ', parent, autoFillBackground=True,
                             font=font)
        self._label.resize(self._label.sizeHint())
        self._label.show()
        self.connect(self, SIGNAL('enableDisplay'), self.enableDisplay)
    def moveEvent(self, event):
        self._repos()
        return QFrame.moveEvent(self, event)
    def resizeEvent(self, event):
        self._repos()
        return QFrame.resizeEvent(self, event)
    def _repos(self):
        mps = self.pos()
        msz = self.size()
        lsz = self._label.size()
        self._label.move(mps.x() + 0.5*(msz.width() - lsz.width()),
                         mps.y() - 0.5*lsz.height())
    def enableDisplay(self, layout, isvis):
        QFrame.setVisible(self, isvis)
        self._label.setVisible(isvis)
        if not isvis:
            layout.removeWidget(self)
        else:
            layout.insertWidget(1, self)


class Monitor(BaseMonitor):
    """Qt specific implementation of instrument monitor."""

    def mainLoop(self):
        self._qtapp.exec_()

    def closeGui(self):
        self._master.close()

    def _class_import(self, clsname):
        modname, member = clsname.rsplit('.', 1)
        mod = __import__(modname, None, None, [member])
        return getattr(mod, member)

    def initGui(self):
        self._qtapp = QApplication(['qtapp'])#, '-style', 'windows'])
        self._master = master = MonitorWindow()
        master.show()

        if self._geometry == 'fullscreen':
            master.showFullScreen()
            QCursor.setPos(master.geometry().bottomRight())
        elif isinstance(self._geometry, tuple):
            w, h, x, y = self._geometry
            master.setGeometry(x, y, w, h)

        self._bgcolor = QColor('gray')
        self._black = QColor('black')
        self._red = QColor('red')
        self._gray = QColor('gray')

        master.setWindowTitle(self.title)
        self._bgcolor = master.palette().color(QPalette.Window)

        timefont  = QFont(self.font, self._fontsizebig + self._fontsize)
        blockfont = QFont(self.font, self._fontsizebig)
        warnfont  = QFont(self.font, self._fontsizebig)
        warnfont.setBold(True)
        labelfont = QFont(self.font, self._fontsize)
        stbarfont = QFont(self.font, int(self._fontsize * 0.8))
        valuefont = QFont(self.valuefont or self.font, self._fontsize)

        onechar  = QFontMetrics(valuefont).width('0')
        blheight = QFontMetrics(blockfont).height()
        tiheight = QFontMetrics(timefont).height()

        # split window into to panels/frames below each other:
        # one displays time, the other is divided further to display blocks.
        # first the timeframe:
        masterframe = QFrame(master)
        masterlayout = QVBoxLayout()
        self._titlelabel = QLabel('', master,
            font=timefont, autoFillBackground=True, alignment=Qt.AlignHCenter)
        pal = self._titlelabel.palette()
        pal.setColor(QPalette.WindowText, self._gray)
        self._titlelabel.setPalette(pal)
        self._titlelabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        master.connect(self._titlelabel, SIGNAL('updatetitle'),
                       self._titlelabel.setText)

        masterlayout.addWidget(self._titlelabel)
        masterlayout.addSpacing(0.2 * tiheight)

        self._warnpanel = QFrame(master)
        self._warnpanel.setVisible(False)

        warningslayout = QVBoxLayout()
        lbl = QLabel('Warnings', self._warnpanel, font=warnfont)
        lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        warningslayout.addWidget(lbl)
        self._warnlabel = QLabel('', self._warnpanel, font=blockfont)
        warningslayout.addWidget(self._warnlabel)
        self._warnpanel.setLayout(warningslayout)
        masterlayout.addWidget(self._warnpanel)
        master.connect(self._warnpanel, SIGNAL('switchwarnpanel'),
                       self._switch_warnpanel)

        displayframe = QFrame(master)
        self._plots = {}

        def _create_field(groupframe, field):
            if isinstance(field, str):
                field = {'dev': field}
            if 'gui' in field:
                instance = uic.loadUi(field['gui'])
                for w in instance.findChildren(DisplayWidget):
                    w.setSource(self)
                    # XXX necessary?
                    w.setConfig(field, labelfont, valuefont, onechar)
                    master.connect(w, SIGNAL('widgetInfo'), self.newWidgetInfo)
                return instance
            elif 'widget' in field:
                widget_class = self._class_import(field['widget'])
                instance = widget_class(groupframe)
                if isinstance(instance, DisplayWidget):
                    instance.setConfig(field, labelfont, valuefont, onechar)
                    instance.setSource(self)
                    master.connect(instance, SIGNAL('widgetInfo'), self.newWidgetInfo)
                for w in instance.findChildren(DisplayWidget):
                    w.setConfig(field, labelfont, valuefont, onechar)
                    w.setSource(self)
                    master.connect(w, SIGNAL('widgetInfo'), self.newWidgetInfo)
                return instance
            elif 'plot' in field and plot_available:
                plotwidget = self._plots.get(field['plot'])
                if plotwidget:
                    plotwidget.devices += [field.get('dev', field.get('key', ''))]
                    return None
                plotwidget = TrendPlot(groupframe)
                plotwidget.setConfig(field, labelfont, valuefont, onechar)
                plotwidget.setSource(self)
                self._plots[field['plot']] = plotwidget
                plotwidget.devices += [field.get('dev', field.get('key', ''))]
                master.connect(plotwidget, SIGNAL('widgetInfo'), self.newWidgetInfo)
                return plotwidget
            else:
                display = ValueDisplay(groupframe)
                display.setConfig(field, labelfont, valuefont, onechar)
                display.setSource(self)
                master.connect(display, SIGNAL('widgetInfo'), self.newWidgetInfo)
                return display

        # now iterate through the layout and create the widgets to display it
        displaylayout = QVBoxLayout(spacing=20)
        for superrow in self.layout:
            boxlayout = QHBoxLayout(spacing=20)
            boxlayout.setContentsMargins(10, 10, 10, 10)
            for column in superrow:
                columnlayout = QVBoxLayout(spacing=0.8*blheight)
                for block in column:
                    blocklayout_outer = QHBoxLayout()
                    blocklayout_outer.addStretch()
                    blocklayout = QVBoxLayout()
                    blocklayout.addSpacing(0.5 * blheight)
                    blockbox = BlockBox(displayframe, block[0], blockfont)
                    for row in block[1]:
                        if row in (None, '---'):
                            blocklayout.addSpacing(12)
                        else:
                            rowlayout = QHBoxLayout()
                            rowlayout.addStretch()
                            rowlayout.addSpacing(self._padding)
                            for field in row:
                                fieldwidget = _create_field(blockbox, field)
                                if fieldwidget:
                                    rowlayout.addWidget(fieldwidget)
                                    rowlayout.addSpacing(self._padding)
                            rowlayout.addStretch()
                            blocklayout.addLayout(rowlayout)
                    if len(block) > 2 and block[2]:
                        setupnames = [block[2]] if isinstance(block[2], str) \
                                     else block[2]
                        for setupname in setupnames:
                            self._onlymap.setdefault(setupname, []).append(
                                (blocklayout_outer, blockbox))
                    blocklayout.addSpacing(0.3 * blheight)
                    blockbox.setLayout(blocklayout)
                    blocklayout_outer.addWidget(blockbox)
                    blocklayout_outer.addStretch()
                    columnlayout.addLayout(blocklayout_outer)
                    columnlayout.addStretch()
                columnlayout.addStretch()
                boxlayout.addLayout(columnlayout)
            displaylayout.addLayout(boxlayout)
        displayframe.setLayout(displaylayout)

        for plot in self._plots.values():
            plot.setSource(self)

        masterlayout.addWidget(displayframe)

        masterframe.setLayout(masterlayout)
        master.setCentralWidget(masterframe)

        def resizeToMinimum():
            master.resize(master.sizeHint())
            if self._geometry == 'fullscreen':
                master.showFullScreen()
        master.connect(master, SIGNAL('resizeToMinimum'), resizeToMinimum)

        # initialize status bar
        self._statuslabel = QLabel(font=stbarfont)
        master.statusBar().addWidget(self._statuslabel)
        self._statustimer = None

    def signal(self, obj, signal, *args):
        obj.emit(SIGNAL(signal), *args)

    def newWidgetInfo(self, info):
        self._statuslabel.setText(info)

    def updateTitle(self, title):
        self._titlelabel.emit(SIGNAL('updatetitle'), title)

    def switchWarnPanel(self, on):
        self._warnpanel.emit(SIGNAL('switchwarnpanel'), on)

    def _switch_warnpanel(self, on):
        if on:
            pal = self._titlelabel.palette()
            pal.setColor(QPalette.WindowText, self._black)
            pal.setColor(QPalette.Window, self._red)
            self._titlelabel.setPalette(pal)
            self._warnlabel.setText(self._currwarnings)
            self._warnpanel.setVisible(True)
            self._master.update()
        else:
            self._warnpanel.setVisible(False)
            pal = self._titlelabel.palette()
            pal.setColor(QPalette.WindowText, self._gray)
            pal.setColor(QPalette.Window, self._bgcolor)
            self._titlelabel.setPalette(pal)
            self._master.update()

    def reconfigureBoxes(self):
        for setup, boxes in self._onlymap.iteritems():
            for layout, blockbox in boxes:
                if setup.startswith('!'):
                    enabled = setup[1:] not in self._setups
                else:
                    enabled = setup in self._setups
                blockbox.emit(SIGNAL('enableDisplay'), layout, enabled)
        # HACK: master.sizeHint() is only correct a certain time *after* the
        # layout change (I've not found out what event to generate or intercept
        # to do this in a more sane way).
        def emitresize():
            sleep(1)
            self._master.emit(SIGNAL('resizeToMinimum'))
        threading.Thread(target=emitresize, name='emitresize').start()
