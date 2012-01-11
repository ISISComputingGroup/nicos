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

import sys, os
from os import path

if path.isdir('.git'):
    current_version = os.popen('git describe --always').read().strip()
else:
    sys.path.insert(0, 'lib')
    current_version = __import__('nicos').nicos_version

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith('.py'):
            fpath = path.join(root, file)
            contents = open(fpath, 'r').read()
            new_contents = contents.replace('$Revision$', current_version)
            if contents != new_contents:
                open(fpath, 'w').write(new_contents)
