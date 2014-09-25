.. _monitor:

The NICOS status monitor
========================

The NICOS status monitor is an application that displays current values of
instrument positions and parameters obtained from the :ref:`cache <cache>`.  It
supports several backends, such as a GUI and an HTML backend.


Invocation
----------

The status monitor is invoked with the ``nicos-monitor`` script.

It is configured, like all other components, using a setup file.

A device named ``Monitor`` is expected in the setup.

.. The file must be named either ``monitor.py`` or :file:`{SETUPNAME}.py`, where
   ``SETUPNAME`` is a user-defined name.

On startup, the setup loaded is either ``monitor.py`` if started with no arguments,
or ``SETUPNAME.py`` if the setup is given via the ``-S`` or ``--setup`` option.

There are several command-line options that allow to display the same monitor
setup on the personal screen, and on a big dedicated status display with bigger
font.

-h, --help                            show the help message and exit
-d, --daemon                          daemonize the monitor process (only useful for non-GUI versions)
-s size, --fontsize=size              select the base font size.
-p padding, --padding=padding         select the padding between blocks.
-S SETUPNAME, --setup=SETUPNAME       name of the setup, default is 'monitor'
-g geom, --geometry=geom              select the window geometry with a string 'WxH+X+Y' or 'fullscreen'

The Qt monitor supports two key bindings: press ``q`` to exit and ``f`` to
toggle full-screen mode.


Setup file
----------

A simple setup file for the monitor could look like this::

  # this is not a setup with instrument devices
  group = 'special'

  # these are helper functions to make the configuration look more intuitive
  Row = Column = Block = BlockRow = lambda *args: args
  Field = lambda *args, **kwds: args or kwds

  expcolumn = Column(
    Block('Experiment',   # block name
      # a list of rows in that block
      [BlockRow(Field(name='Proposal', key='exp/proposal', width=7),
                Field(name='Title',    key='exp/title',    width=20,
                      istext=True, maxlen=20),
                Field(name='Current status', key='exp/action', width=30,
                      istext=True),
                Field(name='Last file', key='filesink/lastfilenumber'))]
    ),
  )

  devcolumn = Column(
    Block('Axes',
      [BlockRow(Field('mth'), Field('mtt')),
       BlockRow(Field('psi'), Field('phi')),
       BlockRow(Field('ath'), Field('att'))],
    # setup that must be loaded for this block to be shown
    'tas'),

    Block('Detector',
      [BlockRow(Field(name='timer', dev='timer'),
                Field(name='ctr1',  dev='ctr1'),
                Field(name='ctr2',  dev='ctr2')),
      ],
    'detector'),

    Block('Triple-axis',
      [BlockRow(Field(dev='tas', item=0, name='H', format='%.3f', unit=' '),
                Field(dev='tas', item=1, name='K', format='%.3f', unit=' '),
                Field(dev='tas', item=2, name='L', format='%.3f', unit=' '),
                Field(dev='tas', item=3, name='E', format='%.3f', unit=' ')),
       BlockRow(Field(key='tas/scanmode', name='Mode'),
                Field(dev='mono', name='ki'),
                Field(dev='ana', name='kf'),
                Field(key='tas/energytransferunit', name='Unit')),
      ],
    'tas'),
  )

  devices = dict(
      Monitor = device('nicos.services.monitor.qt.Monitor',
                       title = 'My status monitor',
                       cache = 'localhost:14869',
                       layout = [Row(expcolumn), Row(devcolumn)]),
  )

The layout of the status monitor consists of nested vertical and horizontal
stacks of displayed units:

* At the top level, there are rows.  The ``layout`` parameter of the Monitor
  device is a list of rows.

* Each row consists of a number of columns.

* Each column consists of a number of blocks.  Each block has a title and a
  number of rows ("block rows") in it.  A block can have an associated setup
  name, which means that it will only be shown if that setup is loaded in the
  NICOS :term:`master`.  See the "Axes" block in the example.

* Each block row consists of a number of fields.

* A field has a name and a value.

The configuration for a Field is either a simple string naming a device (see the
"Axes" block above) a dictionary with more detailed configuration what is
displayed and how.

The recognized keys are:

* ``dev`` -- set this field up for displaying the current value of a device.

* ``key`` -- this can be set alternatively to ``dev`` to display arbitrary cache
  keys.  This is useful to display device parameters: see the "Triple Axis"
  block in the example configuration.  The current scanmode (``tas.scanmode`` in
  NICOS) is displayed with the key ``tas/scanmode``.

* ``name`` -- if given, sets a new name for the field (by default, it is the
  ``dev`` or ``key``).

* ``item`` -- if given, and the value is a tuple or list, only the specified
  item of the value is displayed.  See the "Triple Axis" block above: the
  current Q/E space position (which is a ``(h, k, l, E)`` tuple in NICOS) is
  displayed in four different fields.

* ``width`` -- controls the width of the field, as a number of characters.

* ``istext`` -- if true, the value is displayed using a proportional font
  instead of a monospaced font that is used for numeric values.

* ``maxlen`` -- most useful for string values, can be used to cut the value
  after a certain number of characters.

* ``min`` and ``max`` -- if set, the field will be marked in red if the value is
  below/above the given value.  This is only for display purposes; device limits
  should be enforced in NICOS.  These are now obsolete since every device has a
  parameter named ``warnlimits`` (a tuple of ``(min, max)`` values) which is
  used by the monitor.

* ``unit`` -- if set, it overrides the displayed unit (normally, the unit of the
  device is used).  For example, in the "Triple Axis" block above, the unit for
  H/K/L and E is set to a space (empty string would mean the default unit) to
  avoid displaying redundant "rlu".

* ``format`` -- if set, it overrides the format string of the displayed value
  (normally the foramt string of the device is used).  This is also useful for
  values with a ``key`` (which have no default format string) or ``item`` (where
  the devices' format string does not apply), see the "Triple Axis" block above.

Special widgets
^^^^^^^^^^^^^^^

The Qt status monitor supports adding custom widgets and widget panels.  One of
them is the "trend plot" widget, which is selected by giving a ``plot`` key:

* ``plot`` -- if set, the value is not displayed as a number, but as a plot.
  This currently only works in the Qt backend.

  The value for this key is an identifier for the plot.  Multiple values can be
  plotted in the same plot if they have the same identifier.

  The ``width`` property can be given for plots too, in the same unit as for
  other values (characters).

* ``height`` -- controls the minimum height of the plotting widget, as a number
  of characters.

* ``plotwindow`` -- a number of seconds, which specifies how far back in time the
  plot X axis will go (default is 1 hour).  For example, ::

    ...
    Field('TA', plot='temps', plotwindow=7200),
    Field('TB', plot='temps', plotwindow=7200),
    ...

  will plot the ``TA`` and ``TB`` device values for the last 2 hours.

Other widgets have to be specified by a key named ``widget``:

* ``widget`` -- if set, this names a class (with fully-qualified module name)
  such as ``nicos.demo.monitorwidgets.VTas`` that takes over the display for
  this field.  The additional accepted keys are defined by the widget.

Another possibility is to use Qt Designer to create a custom widget layout and
use this in the monitor.  For this there exists a key:

* ``gui`` -- if set, the field will be loaded from a Qt Designer ``.ui`` file
  with the given file name.

Use the ``bin/designer-nicos`` executable to start the designer.  Then you will
have NICOS specific widgets available that automatically show values from the
cache, such as a value display (label/value combination) and a trend plot.


Backends
--------

In the example setup above, the Monitor device is confiugred with the class
``nicos.services.monitor.qt.Monitor``.  This selects the Qt backend, which
displays the monitor as a window using the Qt GUI toolkit.  Another backend
exists:

* ``nicos.services.monitor.html.Monitor`` -- writing a HTML file periodically.
  You have to configure two additional parameters:

  - ``filename``: the filename for the HTML file
  - ``interval``: the period, in seconds

  The HTML monitor only supports the standard value display and the trend plot
  widget, but no custom widgets (yet).


Warnings
--------

The status monitor automatically displays the current warnings displayed by the
:ref:`watchdog` daemon.  If there are any warnings, the title label turns red,
and display alternates between a list of warnings and normal values.
