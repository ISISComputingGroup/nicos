description = 'piezo motor slit'

group = 'optional'

tango_base = 'tango://phys.kws1.frm2:10000/kws1/FZJS7/'

devices = dict(
    piezo_left = device('nicos.devices.tango.Motor',
        description = 'Left blade of slit 1',
        tangodevice = tango_base + 'piezo_left',
        unit = 'mm',
        precision = 0.01,
        fmtstr = '%.2f',
        lowlevel = False,
    ),
    piezo_right = device('nicos.devices.tango.Motor',
        description = 'Right blade of piezo slit',
        tangodevice = tango_base + 'piezo_right',
        unit = 'mm',
        precision = 0.01,
        fmtstr = '%.2f',
        lowlevel = False,
    ),
    piezo_bottom = device('nicos.devices.tango.Motor',
        description = 'Bottom blade of piezo slit',
        tangodevice = tango_base + 'piezo_bottom',
        unit = 'mm',
        precision = 0.01,
        fmtstr = '%.2f',
        lowlevel = False,
    ),
    piezo_top = device('nicos.devices.tango.Motor',
        description = 'Left blade of piezo slit',
        tangodevice = tango_base + 'piezo_top',
        unit = 'mm',
        precision = 0.01,
        fmtstr = '%.2f',
        lowlevel = False,
    ),
    piezo_slit = device('nicos.devices.generic.Slit',
        description = 'Piezo Slit',
        left = 'piezo_left',
        right = 'piezo_right',
        bottom = 'piezo_bottom',
        top = 'piezo_top',
        opmode = 'centered',
#        coordinates = 'opposite',
    ),
)

extended = dict(
    representative = 'piezo_slit',
)
