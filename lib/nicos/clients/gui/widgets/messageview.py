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

"""A text control to display logging messages of the daemon."""

import re
from time import strftime, localtime
from logging import DEBUG, INFO, WARNING, ERROR, FATAL

from PyQt4.QtGui import QTextCharFormat, QBrush, QColor, QFont, QTextBrowser, \
     QTextCursor, QMainWindow, QTextEdit
from PyQt4.QtCore import Qt, QRegExp

from nicos.utils.loggers import INPUT, ACTION


levels = {DEBUG: 'DEBUG', INFO: 'INFO', WARNING: 'WARNING',
          ERROR: 'ERROR', FATAL: 'FATAL'}

# text formats for the output view

std = QTextCharFormat()

grey = QTextCharFormat()
grey.setForeground(QBrush(QColor('grey')))

red = QTextCharFormat()
red.setForeground(QBrush(QColor('red')))

magenta = QTextCharFormat()
magenta.setForeground(QBrush(QColor('#C000C0')))

bold = QTextCharFormat()
bold.setFontWeight(QFont.Bold)

redbold = QTextCharFormat()
redbold.setForeground(QBrush(QColor('red')))
redbold.setFontWeight(QFont.Bold)

# REs for hyperlinks

command_re = re.compile(r'>>> \[([^ ]+) .*?\]  (.*?)\n')
script_re = re.compile(r'>>> \[([^ ]+) .*?\] -{20} ?(.*?)\n')
update_re = re.compile(r'UPDATE \[([^ ]+) .*?\] -{20} ?(.*?)\n')

# time formatter

def format_time_full(timeval):
    return strftime(' [%Y-%m-%d %H:%M:%S] ', localtime(timeval))

def format_time(timeval):
    return strftime('[%H:%M:%S] ', localtime(timeval))


class MessageView(QTextBrowser):

    def __init__(self, parent):
        QTextBrowser.__init__(self, parent)
        self._messages = []
        self._actionlabel = None
        self._currentuser = None

    def setActionLabel(self, label):
        self._actionlabel = label

    def clear(self):
        QTextBrowser.clear(self)
        self._messages = []

    def scrollToBottom(self):
        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())

    def formatMessage(self, message, actions=True):
        # message is a sequence:
        # (logger, time, levelno, message, exc_text, prefix)
        fmt = None
        levelno = message[2]
        if message[0] == 'nicos':
            name = ''
        else:
            name = '%-10s: ' % message[0]
        name = message[5] + name
        if levelno == ACTION:
            if actions and self._actionlabel:
                action = message[3].strip()
                if action:
                    self._actionlabel.setText('Status: ' + action)
                    self._actionlabel.show()
                else:
                    self._actionlabel.hide()
            return '', None
        elif levelno <= DEBUG:
            text = name + message[3]
            fmt = grey
        elif levelno <= INFO:
            if message[3].startswith('  > '):
                fmt = QTextCharFormat()
                fmt.setFontWeight(QFont.Bold)
                fmt.setAnchor(True)
                fmt.setAnchorHref('exec:' + message[3][4:].strip())
                return name + message[3], fmt
            text = name + message[3]
        elif levelno == INPUT:
            m = command_re.match(message[3])
            if m:
                fmt = QTextCharFormat()
                fmt.setFontWeight(QFont.Bold)
                fmt.setAnchor(True)
                fmt.setAnchorHref('exec:' + m.group(2))
                if m.group(1) != self._currentuser:
                    fmt.setForeground(QBrush(QColor('#0000C0')))
                return message[3], fmt
            m = script_re.match(message[3])
            if m:
                fmt = QTextCharFormat()
                fmt.setFontWeight(QFont.Bold)
                if m.group(2):
                    fmt.setAnchor(True)
                    fmt.setAnchorHref('edit:' + m.group(2))
                if m.group(1) != self._currentuser:
                    fmt.setForeground(QBrush(QColor('#0000C0')))
                return message[3], fmt
            m = update_re.match(message[3])
            if m:
                fmt = QTextCharFormat()
                fmt.setFontWeight(QFont.Bold)
                if m.group(2):
                    fmt.setAnchor(True)
                    fmt.setAnchorHref('edit:' + m.group(2))
                if m.group(1) != self._currentuser:
                    fmt.setForeground(QBrush(QColor('#006090')))
                else:
                    fmt.setForeground(QBrush(QColor('#00A000')))
                return message[3], fmt
            return message[3], bold
        elif levelno <= WARNING:
            text = levels[levelno] + ': ' + name + message[3]
            fmt = magenta
        else:
            text = levels[levelno] + format_time_full(message[1]) + \
                name + message[3]
            fmt = redbold
        if message[4] and fmt:
            # don't show traceback info by default, but on click
            fmt.setAnchor(True)
            fmt.setAnchorHref('trace:' + message[4])
        return text, fmt

    def addText(self, text, fmt=None):
        textcursor = self.textCursor()
        textcursor.movePosition(QTextCursor.End)
        textcursor.setCharFormat(fmt or std)
        textcursor.insertText(text.decode('utf8', 'replace'))

    def addMessage(self, message):
        bar = self.verticalScrollBar()
        prevmax = bar.maximum()
        prevval = bar.value()

        text, fmt = self.formatMessage(message)
        if text:  # not for ACTIONs
            self.addText(format_time(message[1]), grey)
            self.addText(text, fmt)
            self._messages.append(message)

        # only scroll to bottom if we were there already
        if prevval >= prevmax - 5:
            self.scrollToBottom()

    def addMessages(self, messages):
        textcursor = self.textCursor()
        textcursor.movePosition(QTextCursor.End)
        formatter = self.formatMessage
        for message in messages:
            text, fmt = formatter(message, actions=False)
            if text:
                textcursor.setCharFormat(grey)
                textcursor.insertText(format_time(message[1]))
                textcursor.setCharFormat(fmt or std)
                textcursor.insertText(text)
                self._messages.append(message)

    def getOutputString(self):
        return self.toPlainText()

    def findNext(self, what, regex=False):
        cursor = self.textCursor()
        if regex:
            rx = QRegExp(what, Qt.CaseInsensitive)
            newcurs = self.document().find(rx, cursor)
        else:
            newcurs = self.document().find(what, cursor)
        self.setTextCursor(newcurs)
        return not newcurs.isNull()

    def occur(self, what, regex=False):
        if regex:
            fltargs = QRegExp(what, Qt.CaseInsensitive),
        else:
            fltargs = what, Qt.CaseInsensitive
        content = self.toPlainText().split('\n').filter(*fltargs).join('\n')
        window = QMainWindow(self)
        window.resize(600, 800)
        window.setWindowTitle('Lines matching %r' % str(what))
        widget = QTextEdit(window)
        widget.setFont(self.font())
        window.setCentralWidget(widget)
        widget.setText(content)
        window.show()
