description = 'Email and SMS notifier examples'

group = 'lowlevel'

devices = dict(
    # Configure source and copy addresses to an existing address.
    email = device('nicos.devices.notifiers.Mailer',
        sender = 'nobody@frm2.tum.de',
        copies = [
            ('nobody@frm2.tum.de', 'all'),   # gets all messages
            ('nobody@frm2.tum.de', 'important'), # gets only important messages
        ],
        mailserver = 'mailserver.host',  # please adopt !
        subject = 'NICOS',
        lowlevel = True,
    ),

    # Configure SMS receivers if wanted and registered with IT.
    smser = device('nicos.devices.notifiers.SMSer',
        server = 'triton.admin.frm2',
        receivers = [],
        lowlevel = True,
    ),
)