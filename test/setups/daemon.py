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

description = 'setup for the execution daemon'
group = 'special'

import hashlib

devices = dict(
    Auth   = device('services.daemon.auth.ListAuthenticator',
                    passwd = [('guest', '', 'guest'),
                              ('user', hashlib.sha1('user').hexdigest(), 'user'),
                              ('admin', hashlib.sha1('admin').hexdigest(),
                               'admin')]),
    Daemon = device('services.daemon.NicosDaemon',
                    server = 'localhost:14874',
                    loglevel = 'debug',
                    authenticators = ['Auth']),
)
