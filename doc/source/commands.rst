User Commands
=============

Getting help
------------

.. autofunction:: nicos.commands.basic.help
.. autofunction:: nicos.commands.basic.ListCommands
.. autofunction:: nicos.commands.device.ListDevices
.. autofunction:: nicos.commands.device.ListParams
.. autofunction:: nicos.commands.device.ListMethods
.. autofunction:: nicos.commands.device.version

Output commands
---------------

These commands can be used from user scripts to print information to the output
and the logfile.

.. module:: nicos.commands.output

.. autofunction:: printinfo
.. autofunction:: printdebug
.. autofunction:: printwarning
.. autofunction:: printerror
.. autofunction:: printexception

Setup-related commands
----------------------

.. module:: nicos.commands.basic

.. autofunction:: NewSetup
.. autofunction:: AddSetup
.. autofunction:: RemoveSetup
.. autofunction:: ListSetups
.. autofunction:: CreateDevice
.. autofunction:: CreateAllDevices
.. autofunction:: DestroyDevice
.. autofunction:: SetMode

Experiment-related commands
---------------------------

.. autofunction:: NewExperiment
.. autofunction:: AddUser
.. autofunction:: NewSample
.. autofunction:: Remark
.. autofunction:: LogEntry
.. autofunction:: LogAttach
.. autofunction:: Remember
.. autofunction:: FinishExperiment

Script-related commands
-----------------------

Do not use these commands from the GUI client, rather use its editor which
provides Run and Simulate commands.

.. autofunction:: edit
.. autofunction:: run

Simulation mode commands
------------------------

.. autofunction:: sim
.. autofunction:: sync

Notification commands
---------------------

.. autofunction:: notify
.. autofunction:: SetMailReceivers
.. autofunction:: SetSMSReceivers

Miscellaneous commands
----------------------

.. autofunction:: sleep
.. .. autofunction:: Keep
.. autofunction:: ClearCache
.. autofunction:: UserInfo
.. autofunction:: SaveSimulationSetup
.. autofunction:: SetSimpleMode

Device commands
---------------

.. module:: nicos.commands.device

.. autofunction:: read
.. autofunction:: status

.. autofunction:: move
.. autofunction:: wait
.. autofunction:: maw
.. autofunction:: stop
.. autofunction:: reset
.. autofunction:: info

.. autofunction:: limits
.. autofunction:: resetlimits

.. autofunction:: fix
.. autofunction:: release

.. autofunction:: adjust
.. autofunction:: reference

.. autofunction:: history

.. autofunction:: getall
.. autofunction:: setall

Measuring commands
------------------

.. module:: nicos.commands.measure

.. autofunction:: count
.. autofunction:: preset
.. autofunction:: SetDetectors
.. autofunction:: SetEnvironment
.. autofunction:: AddDetector
.. autofunction:: AddEnvironment
.. autofunction:: ListDetectors
.. autofunction:: ListEnvironment
.. autofunction:: avg
.. autofunction:: minmax

Scanning commands
-----------------

.. module:: nicos.commands.scan

.. autofunction:: scan
.. autofunction:: cscan
.. autofunction:: timescan
.. autofunction:: sweep
.. autofunction:: contscan

.. autofunction:: manualscan

On-line analysis commands
-------------------------

.. module:: nicos.commands.analyze

.. autofunction:: center_of_mass
.. autofunction:: root_mean_square
.. autofunction:: fwhm
.. autofunction:: poly
.. autofunction:: gauss
.. autofunction:: findpeaks
.. autofunction:: center
.. autofunction:: checkoffset

Triple-axis commands
--------------------

To use these commands, add ``'nicos.commands.tas'`` to the ``modules`` list of
one of your loaded setups.

.. module:: nicos.commands.tas

.. autofunction:: Q
.. autofunction:: qscan
.. autofunction:: qcscan
.. autofunction:: calpos
.. autofunction:: pos
.. autofunction:: rp
.. autofunction:: checkalign

.. autofunction:: alu
.. autofunction:: copper
.. autofunction:: ho_spurions
.. autofunction:: acc_bragg
