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

"""Status code definitions."""

# The status constants are ordered by ascending "severity": this way the status
# constant for a combined device is very easily determined as the maximum of the
# subordinate device values.
OK = 100
BUSY = 101
PAUSED = 102
NOTREACHED = 103
ERROR = 104
UNKNOWN = 999

# dictionary mapping all status constants to their names
statuses = dict((v, k.lower()) for (k, v) in globals().iteritems()
                if isinstance(v, int))
