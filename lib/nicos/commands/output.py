#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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

"""Module for output/logging user commands."""

__version__ = "$Revision$"

from nicos import session
from nicos.commands import usercommand


@usercommand
def printdebug(*msgs, **kwds):
    session.log.debug(*msgs, **kwds)

@usercommand
def printinfo(*msgs, **kwds):
    session.log.info(*msgs, **kwds)

@usercommand
def printwarning(*msgs, **kwds):
    session.log.warning(*msgs, **kwds)

@usercommand
def printerror(*msgs):
    session.log.error(*msgs)

@usercommand
def printexception(*msgs):
    session.log.exception(*msgs)
