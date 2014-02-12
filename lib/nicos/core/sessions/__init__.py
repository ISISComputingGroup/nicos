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
Contains the NICOS session classes, which contain all low-level global state of
the NICOS runtime.

Only for internal usage by functions and methods.
"""

import os
import sys
import inspect
import logging
from os import path

import numpy

from nicos.core.spm import SPMHandler
from nicos.core.data import DataSink
from nicos.core.device import Device
from nicos.core.errors import NicosError, UsageError, ModeError, \
     ConfigurationError, AccessError, CacheError
from nicos.devices.notifiers import Notifier
from nicos.utils import formatDocstring
from nicos.utils.loggers import initLoggers, NicosLogger, \
     ColoredConsoleHandler, NicosLogfileHandler
from nicos.devices.instrument import Instrument
from nicos.devices.cacheclient import CacheClient, CacheLockError, \
     SyncCacheClient
from nicos.protocols.cache import FLAG_NO_STORE
from nicos.core.sessions.utils import makeSessionId, sessionInfo, \
     NicosNamespace, SimClock, AttributeRaiser, EXECUTIONMODES, MASTER, SLAVE, \
     SIMULATION, MAINTENANCE
from nicos.pycompat import builtins, exec_, string_types, \
    itervalues, iteritems, listvalues, listitems


SETUP_GROUPS = set([
    'basic', 'optional', 'lowlevel', 'simulated', 'special'
])


class Session(object):
    """The Session class provides all low-level routines needed for NICOS
    operations and keeps the global state: devices, configuration, loggers.

    Within one NICOS process, there is only one singleton session object that is
    always importable using ::

        from nicos import session

    There are several specialized subclasses of `Session`; one of them will
    always be used in concrete applications.
    """

    autocreate_devices = True

    class config(object):
        """Singleton for settings potentially overwritten later."""
        user = None
        group = None
        umask = None
        control_path = path.join(path.dirname(__file__), '..', '..', '..', '..')
        setups_path  = 'setups'
        logging_path = 'log'
        simple_mode = False

    log = None
    name = 'session'
    cache_class = CacheClient

    def __str__(self):
        # used for cache operations
        return 'session'

    def __init__(self, appname, daemonized=False):
        self.appname = appname
        # create a unique session id
        self.sessionid = makeSessionId()
        # contains all created device objects
        self.devices = {}
        # contains the name of all explicitly created devices
        self.explicit_devices = set()
        # contains the configuration for all configured devices
        self.configured_devices = {}
        # contains the name of all loaded modules with user commands
        self.user_modules = set()
        # contains all loaded setups
        self.loaded_setups = set()
        # contains all setups excluded from the currently loaded
        self.excluded_setups = set()
        # contains all explicitly loaded setups
        self.explicit_setups = []
        # current "sysconfig" dictionary resulting from setup files
        self.current_sysconfig = {}
        # path to setup files
        self._setup_path = path.join(self.config.control_path,
                                     self.config.setups_path)
        if not path.isdir(self._setup_path) and path.isdir(
            path.join(self.config.control_path, 'custom/demo/setups')):
            self._setup_path = path.join(self.config.control_path,
                                         'custom/demo/setups')
        # devices failed and succeeded to create in the current setup process
        self._failed_devices = None
        self._success_devices = None
        # info about all loadable setups
        self._setup_info = {}
        # namespace to place user-accessible items in
        self.namespace = NicosNamespace()
        self.local_namespace = NicosNamespace()
        # contains all NICOS-exported names
        self._exported_names = set()
        # action stack for status line
        self._actionStack = []
        # execution mode; initially always slave
        self._mode = SLAVE
        # simulation clock
        self.clock = SimClock()
        # traceback of last unhandled exception
        self._lastUnhandled = None
        # SPM mode or not?
        self._spmode = False
        self._spmhandler = SPMHandler(self)
        self.setSPMode(self.config.simple_mode)
        # plug&play info cache
        self._pnp_cache = {'descriptions': {}}
        # intrinsic count pause request
        self.should_pause_count = None

        # sysconfig devices
        self._def_sysconfig = {
            'cache':      None,
            'instrument': AttributeRaiser(
                ConfigurationError,
                'You have not configured an instrument device in your sysconfig'
                ' dictionary; this action cannot be completed.'),
            'experiment': AttributeRaiser(
                ConfigurationError,
                'You have not configured an experiment device in your sysconfig'
                ' dictionary; this action cannot be completed.'),
            'datasinks':  [],
            'notifiers':  [],
        }
        self.__dict__.update(self._def_sysconfig)

        # set up logging interface
        self._initLogging(console=not daemonized)

        # set up initial namespace
        self.initNamespace()

    def setNamespace(self, ns):
        """Set the namespace to export commands and devices into."""
        self.namespace = ns
        self._exported_names = set()

    def initNamespace(self):
        # add some useful mathematical functions
        for name in [
            'pi', 'sqrt', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan',
            'exp', 'log', 'radians', 'degrees', 'ceil', 'floor']:
            self.namespace[name] = getattr(numpy, name)
        # remove interactive Python interpreter stuff
        for name in ['credits', 'copyright', 'license', 'exit', 'quit']:
            builtins.__dict__.pop(name, None)

    @property
    def mode(self):
        """The current :term:`execution mode` of the session."""
        return self._mode

    def setMode(self, mode):
        """Set a new mode for the session.

        This raises `.ModeError` if the new mode cannot be switched to at the
        moment (for example, if switching to master mode, but another master is
        already active).
        """
        mode = mode.lower()
        oldmode = self._mode
        cache = self.cache
        if mode == oldmode:
            return
        if mode not in EXECUTIONMODES:
            raise UsageError('mode %r does not exist' % mode)
        if oldmode in [SIMULATION, MAINTENANCE]:
            # no way to switch back from special modes
            raise ModeError('switching from %s mode is not supported' % oldmode)
        if mode == MASTER:
            # switching from slave to master
            if not cache:
                self.log.info('no cache present, switching to master anyway')
                #raise ModeError('no cache present, cannot get master lock')
            else:
                self.log.info('checking master status...')
                try:
                    cache.lock(MASTER)
                except CacheLockError as err:
                    raise ModeError('another master is already active: %s' %
                                    sessionInfo(err.locked_by))
                else:
                    cache._ismaster = True
                if set(self.explicit_setups) - set(['system', 'startup']):
                    cache.put(self, 'mastersetup', list(self.loaded_setups))
                    cache.put(self, 'mastersetupexplicit',
                              list(self.explicit_setups))
                    self.elog_event('setup', list(self.explicit_setups))
        else:
            # switching from master (or slave) to slave or to maintenance
            if cache and cache._ismaster:
                cache._ismaster = False
                try:
                    cache._unlock_master()
                except CacheError:
                    self.log.warning('could not release master lock')
            elif mode == MAINTENANCE:
                self.log.warning('Switching from slave to maintenance mode: '
                                 "I'll trust that you know what you're doing!")
        self._mode = mode
        if self._master_handler:
            self._master_handler.enable(mode == MASTER)
        # deactivate synchronized queue mode on the cache client to avoid lockups
        # after forking in simulation mode
        if mode == SIMULATION and cache:
            cache._sync = False
        # switch mode, taking care to switch "higher level" devices before
        # "lower level" (because higher level devices may need attached devices
        # still working in order to read out their last value)
        devs = listvalues(self.devices)
        switched = set()
        while devs:
            for dev in devs[:]:
                if dev._sdevs <= switched:
                    switched.add(dev.name)
                    dev._setMode(mode)
                    devs.remove(dev)
        if mode == SIMULATION:
            if cache:
                cache.doShutdown()
                self.cache = None
            # reset certain global state
            self._manualscan = None
            self._currentscan = None
        self.log.info('switched to %s mode' % mode)

    def setSPMode(self, on):
        """Switch simple parameter mode on or off."""
        self._spmode = on

    @property
    def spMode(self):
        return self._spmode

    def simulationSync(self):
        """Synchronize device values and parameters from current cached values.
        """
        if self._mode != SIMULATION:
            raise NicosError('must be in simulation mode')
        if not self.current_sysconfig.get('cache'):
            raise NicosError('no cache is configured')
        client = SyncCacheClient('Syncer', cache=self.current_sysconfig['cache'],
                                 prefix='nicos/', lowlevel=True)
        try:
            db = client.get_values()
        finally:
            client.doShutdown()
        setups = db.get('session/mastersetupexplicit')
        if setups is not None and set(setups) != set(self.explicit_setups):
            self.unloadSetup()
            self.loadSetup(setups)
        # cache keys are always lowercase, while device names can be mixed,
        # so we build a map once to get fast lookup
        lowerdevs = dict((d.name.lower(), d) for d in itervalues(self.devices))
        umethods_to_call = []
        for key, value in iteritems(db):
            if key.count('/') != 1:
                continue
            dev, param = key.split('/')
            if dev not in lowerdevs:
                continue
            dev = lowerdevs[dev]
            if param == 'value':
                dev._sim_value = value
                dev._sim_min = dev._sim_max = dev._sim_old_value = None
            # "status" is ignored: simulated devices are always "OK"
            elif param in dev.parameters:
                dev._params[param] = value
                umethod = getattr(dev, 'doUpdate' + param.title(), None)
                if umethod:
                    umethods_to_call.append((umethod, value))
        for umethod, value in umethods_to_call:
            umethod(value)
        self.log.info('synchronization complete')

    def setSetupPath(self, path):
        """Set the path to the setup files.

        Normally, the setup path is given in nicos.conf and does not need to be
        set explicitly.
        """
        self._setup_path = path
        self.readSetups()

    def getSetupPath(self):
        """Return the current setup path."""
        return self._setup_path

    def readSetups(self):
        """Read information of all existing setups, and validate them.

        Setup modules are looked for in the directory given by the "setups_path"
        entry in nicos.conf, or by "control_path"/setups.
        """
        self._setup_info.clear()
        for root, _, files in os.walk(self._setup_path, topdown=False):
            for filename in files:
                if not filename.endswith('.py'):
                    continue
                modname = filename[:-3]
                try:
                    with open(path.join(root, filename), 'r') as modfile:
                        code = modfile.read()
                except IOError as err:
                    self.log.exception('Could not read setup '
                                       'module %r: %s' % (modname, err))
                    self._setup_info[modname] = None
                    continue
                # device() is a helper function to make configuration prettier
                ns = {
                    'device': lambda cls, **params: (cls, params),
                    'setupname': modname,
                }
                try:
                    exec_(code, ns)
                except Exception as err:
                    self.log.exception('An error occurred while processing '
                                       'setup %s: %s' % (modname, err))
                    continue
                info = {
                    'description': ns.get('description', modname),
                    'group': ns.get('group', 'optional'),
                    'sysconfig': ns.get('sysconfig', {}),
                    'includes': ns.get('includes', []),
                    'excludes': ns.get('excludes', []),
                    'modules': ns.get('modules', []),
                    'devices': ns.get('devices', {}),
                    'startupcode': ns.get('startupcode', ''),
                    'extended': ns.get('extended', {}),
                    'filename': path.join(root, filename),
                }
                if info['group'] not in SETUP_GROUPS:
                    self.log.warning('Setup %s has an invalid group (valid groups '
                        'are: %s)' % (modname, ', '.join(SETUP_GROUPS)))
                    info['group'] = 'optional'
                if modname in self._setup_info:
                    # setup already exists; override/extend with new values
                    oldinfo = self._setup_info[modname] or {}
                    oldinfo['description'] = ns.get('description',
                                                    oldinfo['description'])
                    oldinfo['group'] = ns.get('group', oldinfo['group'])
                    oldinfo['sysconfig'].update(info['sysconfig'])
                    oldinfo['includes'].extend(info['includes'])
                    oldinfo['excludes'].extend(info['excludes'])
                    oldinfo['modules'].extend(info['modules'])
                    oldinfo['devices'].update(info['devices'])
                    # remove devices overridden by "None" entries completely
                    for devname, value in listitems(oldinfo['devices']):
                        if value is None:
                            del oldinfo['devices'][devname]
                    oldinfo['startupcode'] += '\n' + info['startupcode']
                    oldinfo['extended'].update(info['extended'])
                    oldinfo['filename'] = path.join(root, filename)
                    self.log.debug('%r setup partially merged with version '
                                   'from parent directory' % modname)
                else:
                    self._setup_info[modname] = info
        # check if all includes exist
        for name, info in iteritems(self._setup_info):
            if info is None:
                continue  # erroneous setup
            for include in info['includes']:
                if not self._setup_info.get(include):
                    self.log.error('Setup %s includes setup %s which does not '
                                   'exist or has errors' % (name, include))
                    self._setup_info[name] = None

    def getSetupInfo(self):
        """Return information about all existing setups.

        This is a dictionary mapping setup name to another dictionary.  The keys
        of that dictionary are those present in the setup files: 'description',
        'group', 'sysconfig', 'includes', 'excludes', 'modules', 'devices',
        'startupcode', 'extended'.

        If a setup file could not be read or parsed, the value for that key is
        ``None``.
        """
        return self._setup_info.copy()

    def _nicos_import(self, modname, member='*'):
        try:
            mod = __import__('nicos.' + modname, None, None, [member])
        except ImportError as err1:
            try:
                mod = __import__(modname, None, None, [member])
            except ImportError as err2:
                # handle ImportError due to missing dependencies of the
                # requested module smartly: if the module name starts with
                # "nicos.", the more useful exception is the second one,
                # otherwise it's the first
                if modname.startswith('nicos.'):
                    raise err2
                raise err1
        if member == '*':
            return mod
        return getattr(mod, member)

    def loadSetup(self, setupnames, allow_special=False, raise_failed=False,
                  autocreate_devices=None, autoload_system=True,
                  allow_startupcode=True):
        """Load one or more setup modules given in *setupnames* and set up
        devices accordingly.

        If *allow_special* is true, special setups (with group "special") are
        allowed, otherwise `.ConfigurationError` is raised.  If *raise_failed*
        is true, errors when creating devices are re-raised (otherwise, they are
        reported as warnings).
        """
        if not self._setup_info:
            self.readSetups()

        if isinstance(setupnames, string_types):
            setupnames = [setupnames]
        else:
            setupnames = list(setupnames)

        for setupname in setupnames[:]:
            if setupname in self.loaded_setups:
                self.log.warning('setup %s is already loaded, use '
                                 'NewSetup() without arguments to reload' %
                                 setupname)
                setupnames.remove(setupname)
            elif self._setup_info.get(setupname, Ellipsis) is None:
                raise ConfigurationError(
                    'Setup %s exists, but could not be read (see above); '
                    'please fix the file and try again'
                    % setupname)
            elif setupname not in self._setup_info:
                raise ConfigurationError(
                    'Setup %s does not exist (setup path is %s)' %
                    (setupname, path.normpath(self._setup_path)))

        from nicos.commands import usercommandWrapper
        failed_devs = []

        def load_module(modname):
            if modname in self.user_modules:
                return
            self.user_modules.add(modname)
            self.log.info('importing module %s... ' % modname)
            try:
                mod = self._nicos_import(modname)
            except Exception as err:
                self.log.error('Exception importing %s: %s' % (modname, err))
                return
            for name, command in iteritems(mod.__dict__):
                if getattr(command, 'is_usercommand', False):
                    if name.startswith('_') and command.__name__ != name:
                        # it's a usercommand, but imported under a different
                        # name to be used by another module, don't export it
                        continue
                    self.export(name, usercommandWrapper(command))
                elif getattr(command, 'is_userobject', False):
                    self.export(name, command)

        def inner_load(name):
            if name in self.loaded_setups:
                return
            info = self._setup_info[name]
            if info is None:
                raise ConfigurationError(
                    'Setup %s exists, but could not be read; '
                    'please fix the file and try again'
                    % setupname)
            if name not in setupnames:
                self.log.debug('loading include setup %r (%s)' %
                               (name, info['description']))
            if name in self.excluded_setups:
                raise ConfigurationError('Cannot load setup %r, it is excluded '
                                         'by one of the current setups' % name)

            if info['group'] == 'special' and not allow_special:
                raise ConfigurationError('Cannot load special setup %r' % name)
            if info['group'] == 'simulated' and self._mode != SIMULATION:
                raise ConfigurationError('Cannot load simulation setup %r in '
                                         'non-simulation mode' % name)
            for exclude in info['excludes']:
                if exclude in self.loaded_setups:
                    raise ConfigurationError('Cannot load setup %r when setup '
                        '%r is already loaded' % (name, exclude))

            self.loaded_setups.add(name)
            self.excluded_setups.update(info['excludes'])

            sysconfig = {}
            devlist = {}
            startupcode = []

            for include in info['includes']:
                ret = inner_load(include)
                if ret:
                    sysconfig.update(ret[0])
                    devlist.update(ret[1])
                    startupcode.extend(ret[2])

            for modname in info['modules']:
                load_module(modname)

            self.configured_devices.update(info['devices'])

            sysconfig.update(iteritems(info['sysconfig']))
            devlist.update(iteritems(info['devices']))
            startupcode.append(info['startupcode'])

            return sysconfig, devlist, startupcode

        sysconfig, devlist, startupcode = self.current_sysconfig, {}, []
        load_setupnames = setupnames[:]
        if autoload_system and 'system' in self._setup_info and \
           'system' not in self.loaded_setups:
            load_setupnames.insert(0, 'system')
        for setupname in load_setupnames:
            self.log.info('loading setup %r (%s)' %
                (setupname, self._setup_info[setupname]['description']))
            ret = inner_load(setupname)
            if ret:
                sysconfig.update(ret[0])
                devlist.update(ret[1])
                startupcode.extend(ret[2])

        # initialize the cache connection
        if sysconfig.get('cache') and self._mode != SIMULATION:
            self.cache = self.cache_class('Cache', cache=sysconfig['cache'],
                                          prefix='nicos/', lowlevel=True)
            # be notified about plug-and-play sample environment devices
            self.cache.addPrefixCallback('se/', self._pnpHandler)
            # be notified about watchdog events
            self.cache.addPrefixCallback('watchdog/', self._watchdogHandler)

        # validate and attach sysconfig devices
        sysconfig_items = [
            ('instrument', Instrument),
            ('experiment', Experiment),
            ('datasinks',  [DataSink]),
            ('notifiers',  [Notifier]),
        ]

        for key, devtype in sysconfig_items:
            if key not in sysconfig:
                continue
            value = sysconfig[key]
            if isinstance(devtype, list):
                if not isinstance(sysconfig[key], list):
                    raise ConfigurationError('sysconfig %s entry must be '
                                             'a list' % key)
                devs = []
                for name in value:
                    try:
                        dev = self.getDevice(name, devtype[0])
                    except Exception:
                        if raise_failed:
                            raise
                        self.log.exception('%s device %r failed to create' %
                                           (key, name))
                    else:
                        devs.append(dev)
                setattr(self, key, devs)
            else:
                if value is None:
                    dev = self._def_sysconfig[key]
                elif not isinstance(value, str):
                    raise ConfigurationError('sysconfig %s entry must be '
                                             'a device name' % key)
                elif key == 'experiment' and value not in (None, 'Exp'):
                    raise ConfigurationError('the experiment device must now '
                                             'be named "Exp", please fix your '
                                             'system setup')
                else:
                    try:
                        dev = self.getDevice(value, devtype)
                    except Exception:
                        if raise_failed:
                            raise
                        self.log.exception('%s device %r failed to create' %
                                           (key, value))
                        dev = None
                setattr(self, key, dev)

        # create all other devices
        if autocreate_devices is None:
            autocreate_devices = self.autocreate_devices
        if autocreate_devices:
            for devname, (_, devconfig) in sorted(iteritems(devlist)):
                if devconfig.get('lowlevel', False):
                    continue
                try:
                    self.createDevice(devname, explicit=True)
                except Exception:
                    if raise_failed:
                        raise
                    self.log.exception('device %r failed to create' % devname)
                    failed_devs.append(devname)

        # execute the startup code
        if allow_startupcode:
            for code in startupcode:
                if code:
                    try:
                        exec_(code, self.namespace)
                    except Exception:
                        self.log.exception('error running startup code, ignoring')

        if failed_devs:
            self.log.error('the following devices could not be created:')
            self.log.error(', '.join(failed_devs))
            self.log.info("use CreateDevice('device') or CreateAllDevices() "
                          "later to retry")

        for setupname in setupnames:
            if self._setup_info[setupname]['extended'].get('dynamic_loaded',False):
                continue
            self.explicit_setups.append(setupname)

        if self.mode == MASTER and self.cache:
            self.cache._ismaster = True
            self.cache.put(self, 'mastersetup', list(self.loaded_setups))
            self.cache.put(self, 'mastersetupexplicit',
                           list(self.explicit_setups))
            self.elog_event('setup', list(self.explicit_setups))

        self.setupCallback(list(self.loaded_setups),
                           list(self.explicit_setups))
        if setupnames:
            self.log.info('setups loaded: %s' % ', '.join(setupnames))

    def unloadSetup(self):
        """Unload the current setup.

        This shuts down all created devices and clears the NICOS namespace.
        """
        # shutdown according to device dependencies
        devs = listvalues(self.devices)
        already_shutdown = set()
        while devs:
            for dev in devs[:]:
                # shutdown only those devices that don't have remaining
                # dependencies
                if dev._sdevs <= already_shutdown:
                    already_shutdown.add(dev.name)
                    self.unexport(dev.name, warn=False)
                    try:
                        dev.shutdown()
                    except Exception:
                        dev.log.warning('exception while shutting down', exc=1)
                    devs.remove(dev)
        self.deviceCallback('destroy', list(already_shutdown))
        self.setupCallback([], [])
        self.devices.clear()
        self.configured_devices.clear()
        self.explicit_devices.clear()
        for name in list(self._exported_names):
            self.unexport(name, warn=False)
        if self.cache:
            self.cache.shutdown()
        self.cache = None
        self.instrument = self._def_sysconfig['instrument']
        self.experiment = self._def_sysconfig['experiment']
        self.datasinks = []
        self.notifiers = []
        self.current_sysconfig.clear()
        self.loaded_setups = set()
        self.excluded_setups = set()
        self.explicit_setups = []
        self.user_modules = set()
        for handler in self._log_handlers:
            self.log.removeHandler(handler)
        self._log_handlers = []

    def shutdown(self):
        """Shut down the session: unload the setup and give up master mode."""
        if self._mode == MASTER and self.cache:
            self.cache._ismaster = False
            try:
                self.cache._unlock_master()
            except CacheError:
                self.log.warning('could not release master lock', exc=1)
        self.unloadSetup()

    def export(self, name, obj):
        """Export an object *obj* into the NICOS namespace with given *name*."""
        if isinstance(self.namespace, NicosNamespace):
            self.namespace.setForbidden(name, obj)
            self.namespace.addForbidden(name)
            self.local_namespace.addForbidden(name)
        else:
            self.namespace[name] = obj
        self._exported_names.add(name)

    def unexport(self, name, warn=True):
        """Unexport the object with *name* from the NICOS namespace."""
        if name not in self.namespace:
            if warn:
                self.log.warning('unexport: name %r not in namespace' % name)
            return
        if name not in self._exported_names:
            if warn:
                self.log.warning('unexport: name %r not exported by NICOS' % name)
        if isinstance(self.namespace, NicosNamespace):
            self.namespace.removeForbidden(name)
            self.local_namespace.removeForbidden(name)
        del self.namespace[name]
        self._exported_names.discard(name)

    def getExportedObjects(self):
        """Return an iterable of all objects exported to the NICOS namespace."""
        for name in self._exported_names:
            if name in self.namespace:
                yield name, self.namespace[name]

    def handleInitialSetup(self, setup, mode=SLAVE):
        """Determine which setup to load, and try to become master.

        Called by sessions during startup.
        """
        # If simulation mode is wanted, we need to set that before loading any
        # initial setup.
        if mode == SIMULATION:
            self._mode = SIMULATION

        # Create the initial instrument setup.
        self.loadSetup(setup)

        if mode == SIMULATION:
            self.log.info('starting in simulation mode')
        elif mode == MAINTENANCE:
            self.setMode(MAINTENANCE)
        elif mode == SLAVE:
            # Try to become master if the setup didn't already switch modes.
            try:
                self.setMode(MASTER)
            except ModeError:
                self.log.info('could not enter master mode; remaining slave',
                              exc=True)
            except:
                self.log.warning('could not enter master mode', exc=True)
            if setup != 'startup' or not self.cache:
                return
            # If we became master, the user didn't select a specific startup
            # setup and a previous master setup was configured, re-use that.
            setups = self.cache.get(self, 'mastersetupexplicit')
            if not setups or setups == ['startup']:
                return
            self.log.info('loading previously used master setups: ' +
                          ', '.join(setups))
            self.unloadSetup()
            try:
                self.loadSetup(setups)
            except NicosError:
                self.log.warning('could not load previous setups, falling '
                                 'back to startup setup', exc=1)
                self.loadSetup(setup)

    def commandHandler(self, command, compiler):
        """This method is called when the user executes a simple command.  It
        should return a compiled code object that is then executed instead of
        the command.
        """
        if command.startswith('#'):
            return compiler('LogEntry(%r)' % command[1:].strip())
        if self._spmode:
            return compiler(self._spmhandler.handle_line(command))
        try:
            return compiler(command)
        except SyntaxError:
            # shortcut for integrated help
            if command.endswith('?') or command.startswith('?'):
                return compiler('help(%s)' % command.strip('?'))
            # shortcut for running commands in simple mode
            if command.startswith('.'):
                return compiler(self._spmhandler.handle_line(command[1:]))
            # shortcut for simulation mode
            if command.startswith(':'):
                return compiler('sim(%r)' % command[1:].rstrip())
            raise

    def scriptHandler(self, script, filename, compiler):
        """This method should be called to process/handle a script."""
        if filename.endswith('.txt') or \
                (self._spmode and not filename.endswith('.py')):
            return compiler(self._spmhandler.handle_script(script, filename))
        return compiler(script)

    def showHelp(self, obj=None):
        """Show help for the given object.

        Can be overwritten in a derived session to provide other means of
        displaying help.
        """
        if obj is None:
            from nicos.commands.basic import ListCommands
            ListCommands()
        elif isinstance(obj, Device):
            self.log.info('%s is a device of class %s.' %
                          (obj.name, obj.__class__.__name__))
            if obj.description:
                self.log.info('Device description: %s' % obj.description)
            if obj.__class__.__doc__:
                lines = obj.__class__.__doc__.strip().splitlines()
                self.log.info('Device class description: ' + lines[0])
                for line in lines[1:]:
                    self.log.info(line)
            from nicos.commands.device import ListMethods, ListParams
            ListMethods(obj)
            ListParams(obj)
        elif not inspect.isfunction(obj):
            builtins.help(obj)
        else:
            # for functions, print arguments and docstring
            real_func = getattr(obj, 'real_func', obj)
            if hasattr(real_func, 'help_arglist'):
                argspec = '(%s)' % real_func.help_arglist
            else:
                argspec = inspect.formatargspec(*inspect.getargspec(real_func))
            self.log.info('Usage: ' + real_func.__name__ + argspec)
            for line in formatDocstring(real_func.__doc__ or '', '   '):
                self.log.info(line)

    # -- Device control --------------------------------------------------------

    def startMultiCreate(self):
        """Store devices that fail to create so that they are not tried again
        and again during one setup process.
        """
        self._failed_devices = set()
        self._success_devices = []

    def endMultiCreate(self):
        """Mark the end of a multi-create."""
        self._failed_devices = None
        self.deviceCallback('create', self._success_devices)
        self._success_devices = None

    def getDevice(self, dev, cls=None, source=None, replace_classes=None):
        """Return a device *dev* from the current setup.

        If *dev* is a string, the corresponding device will be looked up or
        created, if necessary.

        *cls* gives a class, or tuple of classes, that *dev* needs to be an
        instance of.

        *replace_classes* can be used to replace configured device classes.
        If given, it is a tuple of ``(old_class, new_class, new_devconfig)``.
        """
        if isinstance(dev, str):
            if dev in self.devices:
                dev = self.devices[dev]
            elif dev in self.configured_devices:
                dev = self.createDevice(dev, replace_classes=replace_classes)
            else:
                raise ConfigurationError(source,
                    'device %r not found in configuration' % dev)
        if not isinstance(dev, cls or Device):
            def clsrep(cls):
                if isinstance(cls, tuple):
                    return ', '.join(clsrep(c) for c in cls)
                return cls.__name__
            if isinstance(cls, tuple):
                raise UsageError(source, 'device must be one of %s' % clsrep(cls))
            raise UsageError(source,
                             'device must be a %s' % (cls or Device).__name__)
        return dev

    def createDevice(self, devname, recreate=False, explicit=False,
                     replace_classes=None):
        """Create device given by a device name.

        If device exists and *recreate* is true, destroy and create it again.
        If *explicit* is true, the device is added to the list of "explicitly
        created devices".
        """
        if self._failed_devices and devname in self._failed_devices:
            raise NicosError('creation already failed once; not retrying')
        if devname not in self.configured_devices:
            found_in = []
            for sname, info in iteritems(self._setup_info):
                if info is None:
                    continue
                if devname in info['devices']:
                    found_in.append(sname)
            if found_in:
                raise ConfigurationError('device %r not found in configuration,'
                    ' but you can load one of these setups with AddSetup to '
                    'create it: %s' % (devname, ', '.join(map(repr, found_in))))
            raise ConfigurationError('device %r not found in configuration'
                                     % devname)
        if devname in self.devices:
            if not recreate:
                if explicit:
                    self.explicit_devices.add(devname)
                    self.export(devname, self.devices[devname])
                return self.devices[devname]
            self.destroyDevice(devname)
        devclsname, devconfig = self.configured_devices[devname]
        if 'description' in devconfig:
            self.log.info('creating device %r (%s)... ' %
                          (devname, devconfig['description']))
        else:
            self.log.info('creating device %r... ' % devname)
        modname, clsname = devclsname.rsplit('.', 1)
        try:
            devcls = self._nicos_import(modname, clsname)
        except (ImportError, AttributeError) as err:
            raise ConfigurationError('failed to import device class %r: %s'
                                     % (devclsname, err))
        if replace_classes is not None:
            for orig_class, replace_class, class_config in replace_classes:
                if issubclass(devcls, orig_class):
                    devcls = replace_class
                    devconfig = class_config
                    break
        try:
            dev = devcls(devname, **devconfig)
        except Exception:
            if self._failed_devices is not None:
                self._failed_devices.add(devname)
            raise
        if self._success_devices is not None:
            self._success_devices.append(devname)
        else:
            self.deviceCallback('create', [devname])
        if explicit:
            self.explicit_devices.add(devname)
            self.export(devname, dev)
        return dev

    def destroyDevice(self, devname):
        """Shutdown a device and remove it from the list of created devices."""
        if devname not in self.devices:
            self.log.warning('device %r not created' % devname)
            return
        self.log.info('shutting down device %r...' % devname)
        dev = self.devices[devname]
        try:
            dev.shutdown()
        except Exception:
            dev.log.warning('exception while shutting down', exc=1)
        self.deviceCallback('destroy', [devname])
        if devname in self.namespace:
            self.unexport(devname)

    def notifyConditionally(self, runtime, subject, body, what=None,
                            short=None, important=True):
        """Send a notification if the current runtime exceeds the configured
        minimum runtimer for notifications.
        """
        if self._mode == SIMULATION:
            return
        for notifier in self.notifiers:
            notifier.sendConditionally(runtime, subject, body, what,
                                       short, important)

    def notify(self, subject, body, what=None, short=None, important=True):
        """Send a notification unconditionally."""
        if self._mode == SIMULATION:
            return
        for notifier in self.notifiers:
            notifier.send(subject, body, what, short, important)

    # -- Special cache handlers ------------------------------------------------

    def _pnpHandler(self, key, value, time, expired=False):
        if self._mode != MASTER:
            return
        parts = key.split('/')
        self.log.debug('got PNP message: key %s, value %s' % (key, value))
        if key.endswith('/description'):
            self._pnp_cache['descriptions'][parts[1]] = value
            return
        elif key.endswith('/nicos/setupname'):
            setupname = value
            if (setupname in self._setup_info and
                self._setup_info[setupname] is not None and
                self._setup_info[setupname]['group'] == 'optional'):
                description = self._pnp_cache['descriptions'].get(parts[1])
                # an event is either generated if
                # - the setup is unloaded and the key was added
                if setupname not in self.loaded_setups and not expired:
                    self.pnpEvent('added', setupname, description)
                # - or the setup is loaded and the key has expired (the
                #   equipment has been removed)
                elif setupname in self.loaded_setups and expired:
                    self.pnpEvent('removed', setupname, description)

    def pnpEvent(self, event, setupname, description):
        if event == 'added':
            self.log.info('new sample environment detected: %s'
                          % (description or ''))
            self.log.info('load setup %r to activate' % setupname)
        elif event == 'removed':
            self.log.info('sample environment removed: %s'
                          % (description or ''))
            self.log.info('unload setup %r to clear its devices' % setupname)

    def _watchdogHandler(self, key, value, time, expired=False):
        """Handle a watchdog event."""
        # value[0] is a timestamp, value[1] a string
        if key.endswith(('/warning', '/action')):
            self.watchdogEvent(key.rsplit('/')[-1], value[0], value[1])
        elif key.endswith('/pausecount'):
            if self.experiment and self.mode == MASTER:
                self.experiment.pausecount = value
                if value:
                    self.should_pause_count = value

    def watchdogEvent(self, event, time, data):
        if event == 'warning':
            self.log.warning('WATCHDOG ALERT: %s' % data)
        elif event == 'action':
            self.log.warning('Executing watchdog action: %s' % data)

    # -- Logging ---------------------------------------------------------------

    def _initLogging(self, prefix=None, console=True):
        prefix = prefix or self.appname
        initLoggers()
        self._loggers = {}
        self._log_handlers = []
        self.createRootLogger(prefix, console)

    def createRootLogger(self, prefix='nicos', console=True):
        self.log = NicosLogger('nicos')
        self.log.setLevel(logging.INFO)
        self.log.parent = None
        log_path = path.join(self.config.control_path, self.config.logging_path)
        if console:
            self.log.addHandler(ColoredConsoleHandler())
        try:
            if prefix == 'nicos':
                self.log.addHandler(NicosLogfileHandler(
                    log_path, 'nicos', str(os.getpid())))
                # handler for master session only
                self._master_handler = NicosLogfileHandler(log_path)
                self._master_handler.disabled = True
                self.log.addHandler(self._master_handler)
            else:
                self.log.addHandler(NicosLogfileHandler(log_path, prefix))
                self._master_handler = None
        except (IOError, OSError) as err:
            self.log.error('cannot open log file: %s' % err)

    def getLogger(self, name):
        """Return a new NICOS logger for the specified device name."""
        if name in self._loggers:
            return self._loggers[name]
        logger = NicosLogger(name)
        logger.parent = self.log
        logger.setLevel(logging.DEBUG)
        self._loggers[name] = logger
        return logger

    def addLogHandler(self, handler):
        """Add a new logging handler to the list of handlers for all NICOS
        loggers.
        """
        self._log_handlers.append(handler)
        self.log.addHandler(handler)

    def logUnhandledException(self, exc_info=None, cut_frames=0, msg=''):
        """Log an unhandled exception (occurred during user scripts).

        The exception is logged using the originating device's logger, if that
        information is available.
        """
        if exc_info is None:
            exc_info = sys.exc_info()
        self._lastUnhandled = exc_info
        if isinstance(exc_info[1], NicosError):
            if exc_info[1].device and exc_info[1].device.log:
                exc_info[1].device.log.error(exc_info=exc_info)
                return
        if cut_frames:
            etype, evalue, tb = exc_info  # pylint: disable=W0633
            while cut_frames:
                tb = tb.tb_next
                cut_frames -= 1
            exc_info = (etype, evalue, tb)
        if msg:
            self.log.error(msg, exc_info=exc_info)
        else:
            self.log.error(exc_info=exc_info)

    def elog_event(self, eventtype, data):
        # NOTE: simulation mode is disconnected from cache, therefore no elog
        # events will be sent in simulation mode
        if self.cache:
            self.cache.put_raw('logbook/' + eventtype + FLAG_NO_STORE, data)

    # -- Action logging --------------------------------------------------------

    def beginActionScope(self, what):
        self._actionStack.append(what)
        joined = ' :: '.join(self._actionStack)
        self.log.action(joined)
        if self.cache:
            self.cache.put(self.experiment, 'action', joined, flag=FLAG_NO_STORE)

    def endActionScope(self):
        self._actionStack.pop()
        joined = ' :: '.join(self._actionStack)
        self.log.action(joined)
        if self.cache:
            self.cache.put(self.experiment, 'action', joined, flag=FLAG_NO_STORE)

    def action(self, what):
        joined = ' :: '.join(self._actionStack + [what])
        self.log.action(joined)
        if self.cache:
            self.cache.put(self.experiment, 'action', joined, flag=FLAG_NO_STORE)

    # -- Simulation support ----------------------------------------------------

    def runSimulation(self, code, wait=True, prefix='(sim) '):
        """Spawn a simulation of *code*.

        If *wait* is true, wait until the process is finished.  *prefix* is the
        prefix given to all log messages.
        """
        from nicos.utils.messaging import SimulationSupervisor
        if not self.cache:
            raise NicosError('cannot start simulation, no cache is configured')

        # read out last values of all devices
        for dev in self.devices.values():
            try:
                dev.read()  # cached value is okay
            except Exception:
                pass

        # create a thread that that start the simulation and forwards its
        # messages to the client(s)
        supervisor = SimulationSupervisor(self, code, prefix)
        supervisor.start()
        if wait:
            supervisor.join()

    # -- Session-specific behavior ---------------------------------------------

    def updateLiveData(self, tag, filename, dtype, nx, ny, nt, time, data):
        """Send new live data to clients.

        The parameters are:

        * tag - a string describing the type of data that is sent.  It is used
          by clients to determine if they can display this data.
        * filename - a string giving the filename of the data once measurement
          is finished.  Can be empty.
        * dtype - a string describing the data array in numpy style, if it is
          in array format.
        * nx, ny, nt - three integers giving the dimensions of the data array,
          if it is in array format.
        * time - the current measurement time, for determining count rate.
        * data - the actual data as a byte string.
        """

    def breakpoint(self, level):
        """Allow breaking or stopping the script at a well-defined time.

        *level* can be 1 to indicate a breakpoint "after current scan" or 2 to
        indicate a breakpoint "after current scan point".
        """

    def clearExperiment(self):
        """Reset experiment-specific data."""

    def checkAccess(self, required):
        """Check if the current user fulfills the requirements given in the
        *required* dictionary.  Raise `.AccessError` if check failed.

        This is called by the `.requires` decorator.
        """
        if 'mode' in required:
            if self.mode != required['mode']:
                raise AccessError('requires %s mode' % required['mode'])
        return True

    def clientExec(self, func, args):
        """Execute a function client-side."""
        raise NotImplementedError('clientExec is missing for this session')

    def deviceCallback(self, action, devnames):
        """Callback when devices were created or shut down."""

    def setupCallback(self, setupnames, explicit):
        """Callback when setups were loaded or unloaded."""

    def experimentCallback(self, proposal):
        """Callback when the experiment has been changed."""


# must be imported after class definitions due to module interdependencies
from nicos.devices.experiment import Experiment
