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

"""Utilities for the electronic logbook daemon."""

__version__ = "$Revision$"

import math
import time
from cgi import escape
from logging import DEBUG, INFO, WARNING, ERROR, FATAL

from nicos.loggers import INPUT, OUTPUT, ACTION


levels = {DEBUG: 'DEBUG', INFO: 'INFO', WARNING: 'WARNING',
          ERROR: 'ERROR', FATAL: 'FATAL'}


def format_time(timeval):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timeval))

def formatMessage(message):
    cls = 'out'
    levelno = message[2]
    if levelno == ACTION:
        return ''
    if message[0] == 'nicos':
        name = ''
    else:
        name = '%-10s: ' % message[0]
    name = message[5] + name
    if levelno <= DEBUG:
        text = name + message[3]
        cls = 'debug'
    elif levelno <= OUTPUT:
        text = name + message[3]
    elif levelno == INPUT:
        return '<span class="input">' + escape(message[3]) + '</span>'
    elif levelno <= WARNING:
        text = levels[levelno] + ': ' + name + message[3]
        cls = 'warn'
    else:
        text = '%s [%s] %s%s' % (levels[levelno], format_time(message[1]),
                                 name, message[3])
        cls = 'err'
    #if message[4]:
    #    # XXX handle traceback info
    return '<span class="%s">%s</span>' % (cls, escape(text))


def pretty1(value):
    try:
        return '%.3f' % value
    except (ValueError, TypeError):
        return value


def pretty2(value1, value2):
    try:
        ldiff = math.log10(abs(value2 - value1))
        ncomma = 3 - int(ldiff)
        return '%.*f - %.*f' % (ncomma, value1, ncomma, value2)
    except (ValueError, TypeError):
        return '%s - %s' % (value1, value2)
