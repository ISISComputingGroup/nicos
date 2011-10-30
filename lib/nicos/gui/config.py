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

"""NICOS GUI config helpers."""

__version__ = "$Revision$"


class window(tuple):
    def __new__(cls, title, icon, unique, child):
        return tuple.__new__(cls, (title, icon, unique, child))

class hsplit(tuple):
    def __new__(cls, *children):
        return tuple.__new__(cls, children)

class vsplit(tuple):
    def __new__(cls, *children):
        return tuple.__new__(cls, children)

class panel(tuple):
    def __new__(cls, type, **settings):
        return tuple.__new__(cls, (type, settings))

class tool(tuple):
    def __new__(cls, name, type, **settings):
        return tuple.__new__(cls, (name, type, settings))
