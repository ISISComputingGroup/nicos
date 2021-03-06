#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2020 by the NICOS contributors (see AUTHORS)
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

from __future__ import absolute_import, division, print_function

import socket
import time

import pytest

from nicos.clients.base import ConnectionData, NicosClient
from nicos.protocols.daemon import STATUS_IDLE, STATUS_IDLEEXC
from nicos.utils import parseConnectionString, tcpSocket

from test.utils import daemon_addr, killSubprocess, startSubprocess


def daemon_wait_cb():
    start = time.time()
    wait = 10
    s = None
    while time.time() < start + wait:

        try:
            s = tcpSocket(daemon_addr, 0)
        except socket.error:
            time.sleep(0.02)
        else:
            s.close()
            break
        finally:
            if s:
                s.close()
    else:
        raise Exception('daemon failed to start within %s sec' % wait)


@pytest.fixture(scope='function')
def daemon():
    """Start a nicos daemon"""

    daemon = startSubprocess('daemon', wait_cb=daemon_wait_cb)
    yield
    killSubprocess(daemon)


class TestClient(NicosClient):
    def __init__(self):
        self._signals = []
        self._estatus = STATUS_IDLE
        self._disconnecting = False
        NicosClient.__init__(self, print)

    def signal(self, name, data=None, exc=None):  # pylint: disable=W0221
        if name == 'error':
            raise AssertionError('client error: %s (%s)' % (data, exc))
        if name == 'disconnected' and not self._disconnecting:
            raise AssertionError('client disconnected')
        if name == 'status':
            self._estatus = data[0]
        self._signals.append((name, data, exc))

    def iter_signals(self, startindex, timeout):
        starttime = time.time()
        while True:
            endindex = len(self._signals)
            for sig in self._signals[startindex:endindex]:
                yield sig
            startindex = endindex
            time.sleep(0.05)
            if time.time() > starttime + timeout:
                raise AssertionError('timeout in iter_signals')

    def wait_idle(self):
        while True:
            time.sleep(0.05)
            st = self.ask('getstatus')
            if st['status'][0] in (STATUS_IDLE, STATUS_IDLEEXC):
                break

    def run_and_wait(self, command, name=None, allow_exc=False):
        idx = len(self._signals)
        reqid = self.run(command, name)
        # wait for idle status
        processing = False
        for sig in self.iter_signals(idx, 5.0):
            if sig[0] == 'processing' and sig[1]['reqid'] == reqid:
                processing = True
            if processing and sig[0] == 'status' and \
               sig[1][0] in (STATUS_IDLE, STATUS_IDLEEXC):
                if sig[1][0] == STATUS_IDLEEXC and not allow_exc:
                    raise AssertionError('script failed with exception')
                break


@pytest.fixture(scope='function')
def client(daemon):
    """Create a nicos client session and log in"""
    client = TestClient()
    parsed = parseConnectionString('user:user@' + daemon_addr, 0)
    client.connect(ConnectionData(**parsed))
    assert ('connected', None, None) in client._signals

    # wait until initial setup is done
    client.wait_idle()

    yield client

    if client.isconnected:
        client._disconnecting = True
        client.disconnect()


@pytest.fixture(scope='function')
def adminclient(daemon):
    """Create a nicos admin client session and log in"""
    adminclient = TestClient()
    parsed = parseConnectionString('admin:admin@' + daemon_addr, 0)
    adminclient.connect(ConnectionData(**parsed))
    assert ('connected', None, None) in adminclient._signals

    # wait until initial setup is done
    adminclient.wait_idle()

    yield adminclient

    if adminclient.isconnected:
        adminclient._disconnecting = True
        adminclient.disconnect()
