#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

from nicos.core import Override
from nicos.devices.generic import ScanningDetector as NicosScanDet



class ScanningDetector(NicosScanDet):
    """Reseda scanning detector."""

    parameter_overrides = {
        'positions' : Override(settable=True),
    }

    def _processDataset(self, dataset):
        return []  # implement in subclass if necessary

    def valueInfo(self):
        if self.readresult:
            raise NotImplementedError('Result processing implemented, but '
                                      'valueInfo missing')
        else:
            return ()
