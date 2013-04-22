.. _poller:

The Poller daemon
=================

The poller is a service that queries volatile information such as current sensor
and motor readings from all devices in the instrument setup, and pushes updates
to the NICOS cache.

The main poller process is a supervisor that manages a bunch of subprocesses,
one for each setup that is polled.  When one of the subprocesses dies
unexpectedly, it is restarted automatically.  Within the subprocess, each
device is polled in its own thread.


Invocation
----------

The poller is invoked by the ``nicos-poller`` script.  It should normally be
started by the :ref:`init script <initscript>`.

There are no special command-line arguments.  The poller expects a setup file
named ``poller.py`` with a device named ``Poller``.


Setup file
----------

A simple setup file for the poller could look like this::

  description = 'setup for the poller'
  group = 'special'

  sysconfig = dict(
    cache = 'localhost'
  )

  devices = dict(
      Poller = device('services.poller.Poller',
                      autosetup = True,
                      poll = [],
                      alwayspoll = ['reactor'],
                      neverpoll = ['detector'],
                      blacklist = [],
                     ),
  )

The cache to connect to must be given in the ``sysconfig`` dictionary.

The poller device has several parameters, none of which must be specified.
These are:

**autosetup**
  If true (the default), the poller automatically starts subprocesses for each
  setup loaded in the NICOS :term:`master`.  If false, no processes are started
  unless configured with ``poll`` or ``alwayspoll``.

**poll**
  A list of setups whose devices should be polled, if loaded in the NICOS
  master.

**alwayspoll**
  A list of setups whose devices should be polled regardless of what is loaded
  in the NICOS master.

**neverpoll**
  A list of setups whose devices should not be polled, even if ``autosetup`` is
  true and the setups are loaded in the master.

**blacklist**
  A list of **devices** that should never be polled even if the setups they
  appear in are polled.

  This should be used for devices that do not allow concurrent connections from
  the NICOS master and the poller processes.  (Although the master should use
  the values acquired by the poller via cache instead of asking the hardware,
  this may not always work due to timing.)
