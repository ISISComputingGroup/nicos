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
#
# *****************************************************************************

"""Dialog for entering authentication data."""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QSize

from nicos.protocols.daemon import DEFAULT_PORT
from nicos.clients.gui.utils import loadUi


class ConnectionDialog(QDialog):
    """A dialog to request connection parameters."""

    @classmethod
    def getConnectionData(cls, parent, connpresets, lastpreset, lastdata):
        self = cls(parent, connpresets, lastpreset, lastdata)
        ret = self.exec_()
        if ret != QDialog.Accepted:
            return None, None, None, None
        new_addr = str(self.presetOrAddr.currentText())
        new_data = {}
        new_name = preset_name = ''
        if new_addr in connpresets:
            cdata = connpresets[new_addr]
            new_name = new_addr
            new_data['host'] = str(cdata[0])
            new_data['port'] = int(cdata[1])
            if self.userName.text() == '':
                new_data['login'] = str(cdata[2])
            else:
                new_data['login'] = str(self.userName.text())
        else:
            try:
                host, port = new_addr.split(':')
                port = int(port)
            except ValueError:
                host = new_addr
                port = DEFAULT_PORT
            new_data['host'] = host
            new_data['port'] = port
            new_data['login'] = str(self.userName.text())
        passwd = str(self.password.text())
        if not new_name:
            preset_name = str(self.newPresetName.text())
        return new_name, new_data, passwd, preset_name

    def __init__(self, parent, connpresets, lastpreset, lastdata):
        QDialog.__init__(self, parent)
        loadUi(self, 'auth.ui', 'dialogs')
        self.connpresets = connpresets

        self.presetOrAddr.addItems(list(connpresets))
        self.presetOrAddr.setEditText(lastpreset)
        if not lastpreset:
            # if we have no stored last preset connection, put in the raw data
            self.presetOrAddr.setEditText(
                '%s:%s' % (lastdata['host'], lastdata['port']))
        if lastdata['login']:
            self.userName.setText(lastdata['login'])
        self.password.setFocus()
        self.presetFrame.hide()
        self.resize(QSize(self.width(), self.minimumSize().height()))

    def on_presetOrAddr_editTextChanged(self, text):
        if str(text) in self.connpresets:
            conn = self.connpresets[str(text)]
            self.userName.setText(conn[2])
            self.presetFrame.hide()
        else:
            self.presetFrame.show()
