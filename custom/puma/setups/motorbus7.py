description = 'Motor bus 7'
group = 'lowlevel'

devices = dict(
    motorbus7 = device('devices.vendor.ipc.IPCModBusTaco',
                       tacodevice = 'puma/rs485/s23',
                       bustimeout = 0.1,
                       lowlevel = True,
                       ),
)
