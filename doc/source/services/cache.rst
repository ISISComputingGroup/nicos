.. _cache:

The Cache daemon
================

The NICOS cache is a service that collects all values and parameters read from
NICOS devices, so that individual components do not need to access the hardware
too often.  It also serves as an archival system for the instrument status.

For situation where excessive caching is not wanted, NICOS can also run without
the cache component.  However, several other services such as the electronic
logbook and the watchdog depend on a running cache, as it is their means of
inter-process data exchange.


Invocation
----------

The cache is invoked by the ``nicos-cache`` script.  It should normally be
started by the :ref:`init script <initscript>`.

There are no special command-line arguments.  The cache expects a setup file
named ``cache.py`` with a device named ``Server``.


Setup file
----------

A simple setup file for the cache could look like this::

  description = 'setup for the cache server'
  group = 'special'

  devices = dict(
      DB     = device('services.cache.server.FlatfileCacheDatabase',
                      storepath = 'data/cache',
                     ),

      Server = device('services.cache.server.CacheServer',
                      db = 'DB',
                      server = 'localhost',
                     ),
  )

The main device ("Server") has a ``server`` parameter that defines the network
address (``host:port`` with the default port being 14869) on which the cache
listens.

There is an attached device for the server, the cache database.  There are
several classes that can be used here:

.. module:: nicos.services.cache.database

.. autoclass:: FlatfileCacheDatabase()

.. autoclass:: MemoryCacheDatabase()

.. autoclass:: MemoryCacheDatabaseWithHistory()


For a documentation of the network protocol of the cache, please see
:doc:`/protocols/cache`.
