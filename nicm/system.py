#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Description:
#   NICOS System device
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#   $Author$
#
#   The basic NICOS methods for the NICOS daemon (http://nicos.sf.net)
#
#   Copyright (C) 2009 Jens Krüger <jens.krueger@frm2.tum.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# *****************************************************************************

"""
NICOS system device.
"""

__date__   = "$Date$"
__version__= "$Revision$"


from nicm.device import Configurable


class System(Configurable):
    """A special device that serves for global configuration of
    the whole NICM system.
    """

    parameters = {
        'histories': ([], False, 'Global history managers for all devices.'),
    }


class User(Configurable):
    """A special device that represents a user."""

    parameters = {
        'name': ('', True, 'User name.'),
        'affiliation': ('FRM II', False, 'User affiliation.'),
    }
