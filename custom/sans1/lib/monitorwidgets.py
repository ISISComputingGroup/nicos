#  -*- coding: utf-8 -*-

from PyQt4.QtGui import QPainter, QWidget, QColor, QBrush
from PyQt4.QtCore import QSize, Qt, QStringList

from nicos.core.status import BUSY, OK, ERROR, NOTREACHED

from nicos.guisupport.widget import NicosWidget, PropDef

_magenta = QBrush(QColor('#A12F86'))
_yellow = QBrush(QColor('yellow'))
_white = QBrush(QColor('white'))
_black = QBrush(QColor('black'))
_blue = QBrush(QColor('blue'))
_red = QBrush(QColor('red'))

statusbrush = {
    BUSY: _yellow,
    ERROR: _red,
    NOTREACHED: _red,
    OK: _white,
}


class Tube2(NicosWidget, QWidget):
    """Sans1Tube with two detectors..."""

    designer_description = 'SANS-1 tube with two detectors'

    def __init__(self, parent, designMode=False):
        # det1pos, det1shift, det1tilt, det2pos
        self._curval = [0, 0, 0, 0]
        self._curstr = ['', '', '', '']
        self._curstatus = [OK, OK, OK, OK]

        QWidget.__init__(self, parent)
        NicosWidget.__init__(self)

    properties = {
        'devices':   PropDef('QStringList', QStringList()),
        'height':    PropDef(int, 10),
        'width':     PropDef(int, 30),
        'name':      PropDef(str, ''),
        'posscale':  PropDef(float, 100),
        'color':     PropDef('QColor', _magenta.color())
    }

    def sizeHint(self):
        return QSize(self.props['width'] * self._scale + 10,
                     self.props['height'] * self._scale +
                     (self.props['name'] and self._scale * 2.5 or 0) + 40)

    def registerKeys(self):
        for dev in self.props['devices']:
            self.registerDevice(str(dev))

    def on_devValueChange(self, dev, value, strvalue, unitvalue, expired):
        try:
            idx = self.props['devices'].index(dev)
        except ValueError:
            return
        self._curval[idx] = value
        self._curstr[idx] = unitvalue
        self.update()

    def on_devStatusChange(self, dev, code, status, expired):
        try:
            idx = self.props['devices'].index(dev)
        except ValueError:
            return
        self._curstatus[idx] = code
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.setRenderHint(QPainter.Antialiasing)

        fontscale = self._scale
        h = self.props['height'] * fontscale
        w = self.props['width'] * fontscale
        posscale = (w - 120) / self.props['posscale']

        if self.props['name']:
            painter.setFont(self.font())
            painter.drawText(5, 0, w, fontscale * 2.5,
                             Qt.AlignCenter, self.props['name'])
            yoff = fontscale * 2.5
        else:
            yoff = 0

        painter.setPen(self.color)
        painter.drawEllipse(5, 5 + yoff, 50, h)
        painter.drawRect(30, 5 + yoff, w - 50, h)
        painter.setPen(QColor('black'))
        painter.drawArc(5, 5 + yoff, 50, h, 1440, 2880)
        painter.drawLine(30, 5 + yoff, w - 25, 5 + yoff)
        painter.drawLine(30, 5 + yoff + h, w - 25,
                                               5 + yoff + h)
        painter.drawEllipse(w - 45, 5 + yoff, 50, h)

        # draw Detector 1
        minx = 0
        pos_val = self._curval[0]
        if pos_val is not None:
            pos_status = self._curstatus[0]
            pos_str = self._curstr[0]
            shift_val = self._curval[1]
            shift_status = self._curstatus[1]
            shift_str = self._curstr[1]
            # Not used at the moment, prepared for later use
            # tilt_val = self._curval[2]
            tilt_status = self._curstatus[2]
            tilt_str = self._curstr[2]
            if tilt_str.endswith('deg'):
                tilt_str = tilt_str[:-3]+u'°'

            stat = max(pos_status, shift_status, tilt_status)
            painter.setBrush(statusbrush[stat])
            painter.drawRect(60 + pos_val * posscale, 15 + yoff + shift_val * posscale,
                             fontscale, h - 20 - 4*posscale) #XXX tilt ???
            painter.setFont(self.valueFont)
            painter.drawText(60 + pos_val * posscale - 10.5 * fontscale,
                             -5 + yoff + (shift_val - 4) * posscale + h - fontscale,
                             10 * fontscale, 2 * fontscale, Qt.AlignRight, tilt_str)
            painter.drawText(60 + pos_val * posscale + 1.5 * fontscale,
                             -5 + yoff + (shift_val - 4) * posscale + h - fontscale,
                             10 * fontscale, 2 * fontscale, Qt.AlignLeft, shift_str)
            minx = max(minx, 60 + pos_val * posscale + 5 - 4 * fontscale)
            painter.drawText(minx,
                             h + 10 + yoff, 8 * fontscale, 30, Qt.AlignCenter,
                             pos_str)
            minx = minx + 8 * fontscale

        # draw Detector 2
        pos_val = self._curval[3]
        if pos_val is not None:
            pos_status = self._curstatus[3]
            pos_str = self._curstr[3]

            painter.setBrush(statusbrush[pos_status])
            painter.drawRect(60 + pos_val * posscale, 15 + yoff,
                             fontscale, h - 20 - 5 * posscale)
            painter.setFont(self.valueFont)
            minx = max(minx, 65 + pos_val * posscale - 4 * fontscale)
            painter.drawText(minx, h + 10 + yoff,
                             8 * fontscale, 30, Qt.AlignCenter, pos_str)
            minx = minx + 8 * fontscale


class BeamOption(NicosWidget, QWidget):

    designer_description = 'SANS-1 beam option'

    def __init__(self, parent, designMode=False):
        self._curstr = ''
        self._curstatus = OK

        QWidget.__init__(self, parent)
        NicosWidget.__init__(self)

    properties = {
        'dev':       PropDef(str, ''),
        'height':    PropDef(int, 4),
        'width':     PropDef(int, 10),
        'name':      PropDef(str, ''),
    }

    def sizeHint(self):
        return QSize(self.props['width'] * self._scale,
                     self.props['height'] * self._scale +
                     (self.props['name'] and self._scale * 2.5 or 0))

    def registerKeys(self):
        self.registerDevice(self.props['dev'])

    def on_devValueChange(self, dev, value, strvalue, unitvalue, expired):
        self._curstr = unitvalue
        self.update()

    def on_devStatusChange(self, dev, code, status, expired):
        self._curstatus = code
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(_magenta)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.props['width'] * self._scale
        h = self.props['height'] * self._scale

        if self.props['name']:
            painter.setFont(self.font())
            painter.drawText(0, 0, w, self._scale * 2.5,
                             Qt.AlignCenter, self.props['name'])
            yoff = self._scale * 2.5
        else:
            yoff = 0
        painter.setBrush(statusbrush[self._curstatus])
        painter.drawRect(2, 2 + yoff, w - 4, h - 4)
        painter.setFont(self.valueFont)
        painter.drawText(2, 2 + yoff, w - 4, h - 4, Qt.AlignCenter, self._curstr)


class CollimatorTable(NicosWidget, QWidget):

    designer_description = 'SANS-1 collimator table'

    def __init__(self, parent, designMode=False):
        self._curstr = ''
        self._curstatus = OK

        QWidget.__init__(self, parent)
        NicosWidget.__init__(self)

    properties = {
        'dev':       PropDef(str, ''),
        'options':   PropDef('QStringList', QStringList()),
        'height':    PropDef(int, 4),
        'width':     PropDef(int, 10),
        'name':      PropDef(str, ''),
    }

    def registerKeys(self):
        self.registerDevice(self.props['dev'])

    def sizeHint(self):
        return QSize(self._scale * self.props['width'],
                     self._scale * 2.5 * self.props['height'] +
                     (self.props['name'] and 2.5 * self._scale or 0))

    def on_devValueChange(self, dev, value, strvalue, unitvalue, expired):
        self._curstr = strvalue
        self.update()

    def on_devStatusChange(self, dev, code, status, expired):
        self._curstatus = code
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        h = self._scale * 2.5 * self.props['height']
        w = self._scale * self.props['width']

        if self.props['name']:
            painter.setFont(self.font())
            if self._curstatus != OK:
                painter.fillRect(0, 0, w, self._scale * 2.5,
                                 statusbrush[self._curstatus])
            painter.drawText(0, 0, w, self._scale * 2.5,
                             Qt.AlignCenter, self.props['name'])
            yoff = self._scale * 2.5
        else:
            yoff = 0

        painter.setBrush(_blue)
        y = h * 0.5 + yoff
        painter.drawLine(0, y, w, y)
        painter.drawLine(0, y+1, w, y+1)
        painter.drawLine(0, y+2, w, y+2)

        painter.setBrush(statusbrush[self._curstatus])
        try:
            p = self.props['options'].index(self._curstr)
        except ValueError:
            p = len(self.props['options']) // 2 + 0.5

        painter.setFont(self.valueFont)

        h0 = max(2 * self._scale, 2 * self._scale + 4)
        painter.setClipRect(0, yoff, w, h)
        for i, t in enumerate(self.props['options']):
            y = h * 0.5 + yoff + h0 * (p - i - 0.45)
            painter.drawRect(5, y + 2, w - 10, h0 - 4 )
            painter.drawText(5, y + 2, w - 10, h0 - 4,
                             Qt.AlignCenter, t)
