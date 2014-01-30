#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
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

"""
Base class for NICOS UI widgets.
"""

from copy import copy

from PyQt4.QtGui import QFont, QFontMetrics
from PyQt4.QtCore import QString, QStringList, SIGNAL, \
    pyqtProperty, pyqtWrapperType

from nicos.utils import lazy_property
from nicos.core.status import OK
from nicos.protocols.daemon import DAEMON_EVENTS
from nicos.pycompat import add_metaclass, iteritems, text_type

# Import resources file
import nicos.guisupport.gui_rc  #pylint: disable=W0611


class NicosListener(object):
    """Base mixin class for an object that can receive cache events."""

    def setSource(self, source):
        self._source = source
        self._devmap = {}
        self.devinfo = {}
        self.registerKeys()

    def registerDevice(self, dev, valueindex=-1, unit='', fmtstr=''):
        # value, valueindex, strvalue, strvalue with unit,
        # status, strvalue, fmtstr, unit, fixed, changetime, min, max,
        # expired?, device (not single key)?
        self.devinfo[dev] = ['-', valueindex, '-', '-',
                             (OK, ''), fmtstr or '%s', unit, '', 0,
                             None, None, True, True]
        self._devmap[self._source.register(self, dev+'/value')] = dev
        self._devmap[self._source.register(self, dev+'/status')] = dev
        self._devmap[self._source.register(self, dev+'/fixed')] = dev
        self._devmap[self._source.register(self, dev+'/warnlimits')] = dev
        if not unit:
            self._devmap[self._source.register(self, dev+'/unit')] = dev
        if not fmtstr:
            self._devmap[self._source.register(self, dev+'/fmtstr')] = dev

    def registerKey(self, valuekey, statuskey='', valueindex=-1,
                    unit='', fmtstr=''):
        # value, valueindex, strvalue, strvalue with unit,
        # status, strvalue, fmtstr, unit, fixed, changetime, min, max,
        # expired?, device (not single key)?
        self.devinfo[valuekey] = ['-', valueindex, '-', '-',
                                  (OK, ''), fmtstr or '%s', unit, '', 0,
                                  None, None, True, False]
        self._devmap[self._source.register(self, valuekey)] = valuekey
        if statuskey:
            self._devmap[self._source.register(self, statuskey)] = valuekey

    def registerKeys(self):
        """Register any keys that should be watched."""
        raise NotImplementedError('Implement registerKeys() in %s' %
                                  self.__class__)

    def on_keyChange(self, key, value, time, expired):
        """Default handler for changing keys.

        The default handler handles changes to registered devices.
        """
        if key not in self._devmap:
            return
        devinfo = self.devinfo[self._devmap[key]]
        if devinfo[12]:
            if key.endswith('/status'):
                if value is None:
                    value = devinfo[4]
                    expired = True
                devinfo[4] = value
                devinfo[8] = time
                self.on_devStatusChange(self._devmap[key],
                                        value[0], value[1], expired)
                return
            elif key.endswith('/fixed'):
                devinfo[7] = value
                self.on_devMetaChange(self._devmap[key], devinfo[5],
                                      devinfo[6], devinfo[7], devinfo[9],
                                      devinfo[10])
                return
            elif key.endswith('/warnlimits'):
                if value is not None:
                    devinfo[9], devinfo[10] = value
                    self.on_devMetaChange(self._devmap[key], devinfo[5],
                                          devinfo[6], devinfo[7], devinfo[9],
                                          devinfo[10])
                return
            elif key.endswith('/fmtstr'):
                devinfo[5] = value
                fvalue = devinfo[0]
                if fvalue is None:
                    strvalue = '----'
                else:
                    if isinstance(fvalue, list):
                        fvalue = tuple(fvalue)
                    try:
                        strvalue = devinfo[5] % fvalue
                    except Exception:
                        strvalue = str(fvalue)
                devinfo[3] = (strvalue + ' ' + (devinfo[6] or '')).strip()
                if devinfo[2] != strvalue:
                    devinfo[2] = strvalue
                    self.on_devValueChange(self._devmap[key], fvalue, strvalue,
                                           devinfo[3], expired)
                self.on_devMetaChange(self._devmap[key], devinfo[5],
                                      devinfo[6], devinfo[7], devinfo[9],
                                      devinfo[10])
                return
            elif key.endswith('/unit'):
                devinfo[6] = value
                self.on_devMetaChange(self._devmap[key], devinfo[5],
                                      devinfo[6], devinfo[7], devinfo[9],
                                      devinfo[10])
                return
        # it's either /value, or any key registered as value
        # first, apply item selection
        if devinfo[1] >= 0 and value is not None:
            try:
                fvalue = value[devinfo[1]]
            except Exception:
                fvalue = value
        else:
            fvalue = value
        devinfo[0] = fvalue
        if fvalue is None:
            strvalue = '----'
        else:
            if isinstance(fvalue, list):
                fvalue = tuple(fvalue)
            try:
                strvalue = devinfo[5] % fvalue
            except Exception:
                strvalue = str(fvalue)
        devinfo[8] = time
        devinfo[3] = (strvalue + ' ' + (devinfo[6] or '')).strip()
        if devinfo[2] != strvalue or devinfo[11] != expired:
            devinfo[2] = strvalue
            devinfo[11] = expired
            self.on_devValueChange(self._devmap[key], fvalue, strvalue,
                                   devinfo[3], expired)

    def on_devValueChange(self, dev, value, strvalue, unitvalue, expired):
        pass

    def on_devStatusChange(self, dev, code, status, expired):
        pass

    def on_devMetaChange(self, dev, fmtstr, unit, fixed, minval, maxval):
        pass


class PropDef(object):
    all_types = [
        str, float, int,
        'bool',  # only works as C++ type name
    ]

    def __init__(self, ptype, default, doc=''):
        if ptype is bool:
            ptype = 'bool'
        if ptype not in self.all_types:
            if not (isinstance(ptype, str) and ptype.startswith('Q')):
                raise Exception('invalid property type: %r' % ptype)
        self.ptype = ptype
        self.default = default
        self.doc = doc

    @staticmethod
    def convert(value):
        if isinstance(value, QString):
            return text_type(value)
        if isinstance(value, QStringList):
            return [text_type(s) for s in value]
        if isinstance(value, QFont):
            # QFont doesn't like to be copied with copy()...
            return QFont(value)
        return copy(value)


class AutoPropMeta(pyqtWrapperType):
    """Works similar to the DeviceMeta in that properties are automatically
    inherited, and PyQt getters/setters/resetters are generated.
    """

    def __new__(mcs, name, bases, attrs):  # pylint: disable=C0202
        newtype = pyqtWrapperType.__new__(mcs, name, bases, attrs)
        newprops = {}
        for base in reversed(bases):
            if hasattr(base, 'properties'):
                newprops.update(base.properties)
        newprops.update(attrs.get('properties', {}))
        newtype.properties = newprops

        for prop, pdef in sorted(iteritems(newprops)):
            def getter(self, prop=prop):
                return self.props[prop]
            def setter(self, value, prop=prop):
                value = PropDef.convert(value)
                self.props[prop] = value
                self.propertyUpdated(prop, value)
            def resetter(self, prop=prop):
                if callable(pdef.default):
                    setattr(self, prop, pdef.default(self))
                else:
                    setattr(self, prop, pdef.default)
            setattr(newtype, prop,
                    pyqtProperty(pdef.ptype, getter, setter, resetter,
                                 doc=pdef.doc))
        return newtype


@add_metaclass(AutoPropMeta)
class NicosWidget(NicosListener):
    """Base mixin class for a widget that can receive cache events.

    This class can't inherit directly from QObject because Python classes
    can only derive from one PyQt base class, and that base class will be
    different for different widgets.
    """

    # source for cache keys
    _source = None
    # daemon-client object, only present when used in the GUI client
    _client = None

    # set this to a description of the widget for the Qt designer
    designer_description = ''
    # set this to an icon name for the Qt designer
    designer_icon = None

    # define properties
    properties = {
        'valueFont': PropDef('QFont', QFont('monospace')),
    }

    # dictionary for storing current property values
    @lazy_property
    def props(self):
        return {}

    def __init__(self):
        for prop, pdef in iteritems(self.properties):
            if prop not in self.props:
                if callable(pdef.default):
                    self.props[prop] = PropDef.convert(pdef.default(self))
                else:
                    self.props[prop] = PropDef.convert(pdef.default)
        self._scale = QFontMetrics(self.valueFont).width('0')
        self.connect(self, SIGNAL('keyChange'), self.on_keyChange)
        self.initUi()

    def initUi(self):
        """Create user interface if necessary."""

    def propertyUpdated(self, pname, value):
        """Called when a property in self.properties has been updated."""
        if pname == 'valueFont':
            self._scale = QFontMetrics(value).width('0')
        self.update()

    def setClient(self, client):
        self.setSource(client)
        self._client = client
        # auto-connect client signal handlers
        for signal in DAEMON_EVENTS:
            if hasattr(self, 'on_client_' + signal):
                self.connect(self._client, SIGNAL(signal),
                             getattr(self, 'on_client_' + signal))
