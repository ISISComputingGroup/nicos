# -*- coding: utf-8 -*-

__author__  = "Christian Felder <c.felder@fz-juelich.de>"
__date__    = "2014-04-28"
__version__ = "0.1.0"


description = "ZEA-2 counter card test setup"
group = "optional"

_TANGO_SRV = "phys.biodiff.frm2:10000"
_TANGO_URL = "tango://" + _TANGO_SRV + "/biodiff/count/"

devices = dict(
               fpga = device("biodiff.fpga.FPGATimerChannel",
                             description = "ZEA-2 counter card",
                             tangodevice = _TANGO_URL + '0',
                             ),
               )
