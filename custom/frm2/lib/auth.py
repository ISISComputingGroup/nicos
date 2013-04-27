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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#
# *****************************************************************************

"""NICOS FRM II specific authentication."""

from nicos.core import USER
from nicos.services.daemon.auth import User, Authenticator, AuthenticationError
from nicos.frm2.proposaldb import queryUser


class Frm2Authenticator(Authenticator):
    """
    Authenticates against the FRM-II user office database.
    """

    def pw_hashing(self):
        return 'md5'

    def authenticate(self, username, password):
        try:
            uid, passwd = queryUser(username)
            if passwd != password:
                raise AuthenticationError('wrong password')
            return User(username, USER)
        except AuthenticationError:
            raise
        except Exception, err:
            raise AuthenticationError('exception during authenticate(): %s'
                                      % err)
