description = 'Motor bus 9'
group = 'lowlevel'

devices = dict(
    motorbus9 = device('nicos.devices.vendor.ipc.IPCModBusTaco',
                       tacodevice = 'puma/rs485/moxa2_1',
                       bustimeout = 0.1,
                       lowlevel = True,
                      ),
)