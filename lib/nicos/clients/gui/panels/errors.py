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

"""NICOS GUI error and warning window."""

from logging import WARNING

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialogButtonBox

from nicos.clients.gui.utils import loadUi, showTraceback, setBackgroundColor
from nicos.clients.gui.panels import Panel


class ErrorPanel(Panel):
    panelName = 'Error window'

    def __init__(self, parent, client):
        Panel.__init__(self, parent, client)
        loadUi(self, 'errpanel.ui', 'panels')

        self.buttonBox.addButton('Clear', QDialogButtonBox.ResetRole)

        if client.connected:
            self.on_client_connected()
        self.connect(self.client, SIGNAL('connected'), self.on_client_connected)
        self.connect(self.client, SIGNAL('message'), self.on_client_message)

    def setCustomStyle(self, font, back):
        self.outView.setFont(font)
        setBackgroundColor(self.outView, back)

    def on_client_connected(self):
        messages = self.client.ask('getmessages', '10000')
        self.outView.clear()
        self.outView.addMessages([msg for msg in messages if msg[2] >= WARNING])
        self.outView.scrollToBottom()

    def on_client_message(self, message):
        if message[2] >= WARNING:  # show if level is warning or higher
            self.outView.addMessage(message)

    def on_outView_anchorClicked(self, url):
        """Called when the user clicks a link in the out view."""
        url = str(url.toString())
        if url.startswith('trace:'):
            showTraceback(url[6:], self, self.outView)

    def on_buttonBox_clicked(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.ResetRole:
            self.outView.clear()
        else:
            self.parentwindow.close()
