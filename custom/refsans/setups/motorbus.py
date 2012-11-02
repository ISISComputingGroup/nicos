
description = 'IPC Motor bus device configuration'

includes = []

nethost = '//refsanssrv.refsans.frm2/'

devices = dict(
	motorbus = device('devices.vendor.ipc.IPCModBusTaco', 
			tacodevice = nethost + 'test/ipcsms/1', 
                        loglevel = 'info',
                        timeout = 0.5,
			),
	motorbus2 = device('devices.vendor.ipc.IPCModBusTaco', 
                        tacodevice = nethost + 'test/ipcsms/2',
                        loglevel = 'info',
                        timeout = 0.5,
			),
	motorbus3 = device('devices.vendor.ipc.IPCModBusTaco', 
                        tacodevice = nethost + 'test/ipcsms/3',
                        loglevel = 'info',
                        timeout = 0.5,
			),
	motorbus4 = device('devices.vendor.ipc.IPCModBusTaco', 
                        tacodevice = nethost + 'test/ipcsms/4',
                        loglevel = 'info',
                        timeout = 0.5,
			),
        )
