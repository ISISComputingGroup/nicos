description = 'Motor bus 3'
group = 'lowlevel'

devices = dict(
    motorbus3 = device('devices.vendor.ipc.IPCModBusTaco',
                       tacodevice = 'puma/rs485/s42',
                       tacotimeout = 0.5,
                       lowlevel = True,
                       ),
)
