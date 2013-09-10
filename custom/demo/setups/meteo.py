# -*- coding: utf-8 -*-

__author__  = "Christian Felder <c.felder@fz-juelich.de>"
__date__    = "2013-07-11"
__version__ = "0.1.0"

_TEMP_AIR      = "temperature/air"
_TEMP_WET_BULB = "temperature/wet_bulb"
_DEWPOINT      = "dewpoint"
_HUMIDITY      = "humidity"
_WIND_SPEED    = "wind/speed"

description = "weather measuring stations provided by LMU"
group = "optional"

devices = { "T_out": device("jcns.meteo.MeteoStation",
                            description="Outdoor air temperature",
                            query=_TEMP_AIR,
                            location="Garching",
                            unit='C'),
            "T_out_5": device("jcns.meteo.MeteoStation",
                              description=("T_out (Outdoor air temperature)" +
                                           "at 5m height"),
                              query=_TEMP_AIR, height=5.0,
                              unit='C'),
            "phi": device("jcns.meteo.MeteoStation",
                          description="humidity",
                          query="humidity",
                          location="Garching",
                          fmtstr="%d",
                          unit='%'),
            "v_wind": device("jcns.meteo.MeteoStation",
                             description="wind speed",
                             query=_WIND_SPEED,
                             unit="m/s")
           }
