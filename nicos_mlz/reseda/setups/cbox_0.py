#  -*- coding: utf-8 -*-

description = 'Capacity box 0'
group = 'optional'

tango_base = 'tango://resedahw2.reseda.frm2:10000/reseda'

devices = dict(
    osci_pk2pk_1 = device('nicos.devices.tango.AnalogInput',
        description = 'Osci at coil, peak to peak measurement',
        tangodevice = '%s/cbox_0/osci_pk2pk_1' % tango_base,
        tangotimeout = 5,
        pollinterval = 5,
        maxage = 12,
    ),
    osci_pk2pk_2 = device('nicos.devices.tango.AnalogInput',
        description = 'Osci at coil, peak to peak measurement',
        tangodevice = '%s/cbox_0/osci_pk2pk_1' % tango_base,
        tangotimeout = 5,
        pollinterval = 5,
        maxage = 12,
    ),
    cbox_0_freq = device('nicos.devices.tango.RampActuator',
        description = 'Frequency generator frequency',
        tangodevice = '%s/cbox_0/fg_freq' % tango_base,
        pollinterval = 3,
        fmtstr = '%.3g',
        precision = 0.5,
    ),
    cbox_0_amp = device('nicos.devices.tango.RampActuator',
        description = 'Frequency generator amplitude',
        tangodevice = '%s/cbox_0/fg_amplitude' % tango_base,
        pollinterval = 3,
        precision = 0.01,
    ),
    cbox_0_fwdp = device('nicos.devices.tango.AnalogInput',
        description = 'Power amplifier forward power',
        tangodevice = '%s/cbox_0/pa_fwdp' % tango_base,
        pollinterval = 3,
    ),
    cbox_0_revp = device('nicos.devices.tango.AnalogInput',
        description = 'Power amplifier reverse power',
        tangodevice = '%s/cbox_0/pa_revp' % tango_base,
        pollinterval = 3,
    ),
    cbox_0_gain = device('nicos.devices.tango.RampActuator',
        description = 'Power amplifier gain',
        tangodevice = '%s/cbox_0/pa_gain' % tango_base,
        pollinterval = 3,
        precision = 0.1,
    ),
    cbox_0 = device('nicos_mlz.reseda.devices.cbox.CBoxResonanceFrequency',
        pollinterval = 3,
        description = 'CBox',
        unit = 'Hz',
        power_divider = device('nicos.devices.tango.DigitalOutput',
            description = 'Power divider to split the power for both coils',
            tangodevice = '%s/cbox_0/plc_power_divider' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        highpass = device('nicos.devices.tango.DigitalOutput',
            description = 'Highpass filter to smooth the signal',
            tangodevice = '%s/cbox_0/plc_highpass' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        pa_fwdp = 'cbox_0_fwdp',
        pa_revp = 'cbox_0_revp',
        fg = 'cbox_0_freq',
        coil_amp = '%cbox_0_coil_amp',
        diplexer = device('nicos.devices.tango.DigitalOutput',
            description =
            'Lowpass filter to smooth the signal (enable for low frequency, disable for high frequency)',
            tangodevice = '%s/cbox_0/plc_diplexer' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil1_c1 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 1: Capacitor bank 1',
            tangodevice = '%s/cbox_0/plc_a_c1' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil1_c2 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 1: Capacitor bank 2',
            tangodevice = '%s/cbox_0/plc_a_c2' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil1_c3 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 1: Capacitor bank 3',
            tangodevice = '%s/cbox_0/plc_a_c3' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil1_c1c2serial = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 1: Use c1 and c2 in serial instead of parallel',
            tangodevice = '%s/cbox_0/plc_a_c1c2serial' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil1_transformer = device('nicos.devices.tango.DigitalOutput',
            description =
            'Coil 1: Used to manipulate the coil resistance to match the power amplifier resistance',
            tangodevice = '%s/cbox_0/plc_a_transformer' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil2_c1 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 2: Capacitor bank 1',
            tangodevice = '%s/cbox_0/plc_b_c1' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil2_c2 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 2: Capacitor bank 2',
            tangodevice = '%s/cbox_0/plc_b_c2' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil2_c3 = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 2: Capacitor bank 3',
            tangodevice = '%s/cbox_0/plc_b_c3' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil2_c1c2serial = device('nicos.devices.tango.DigitalOutput',
            description = 'Coil 2: Use c1 and c2 in serial instead of parallel',
            tangodevice = '%s/cbox_0/plc_b_c1c2serial' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
        coil2_transformer = device('nicos.devices.tango.DigitalOutput',
            description =
            'Coil 2: Used to manipulate the coil resistance to match the power amplifier resistance',
            tangodevice = '%s/cbox_0/plc_b_transformer' % tango_base,
            lowlevel = False,  # temporary due to inaccurate auto tune
        ),
    ),
)
