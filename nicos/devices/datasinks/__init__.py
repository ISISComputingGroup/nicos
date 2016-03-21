#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2015 by the NICOS contributors (see AUTHORS)
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

"""Data sink classes (new API) for NICOS."""

from nicos.devices.datasinks.file import FileSink
from nicos.devices.datasinks.scan import ConsoleScanSink, AsciiScanfileSink
from nicos.devices.datasinks.special import SerializedSink, DaemonSink, \
    LiveViewSink
from nicos.devices.datasinks.image import ImageSink
from nicos.devices.datasinks.fits import FITSImageSink
from nicos.devices.datasinks.tiff import TIFFImageSink
from nicos.devices.datasinks.livepng import PNGLiveFileSink
from nicos.devices.datasinks.raw import SingleRawImageSink, RawImageSink
