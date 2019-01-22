description = 'Email and SMS notifiers'

group = 'lowlevel'

devices = dict(
    email = device('nicos.devices.notifiers.Mailer',
        sender = 'kws3@frm2.tum.de',
        copies = [
            ('g.brandl@fz-juelich.de', 'all'),
            ('v.pipich@fz-juelich.de', 'all'),
        ],
        subject = '[KWS-3]',
        mailserver = 'mailhost.frm2.tum.de',
    ),
    smser = device('nicos.devices.notifiers.SMSer',
        server = 'triton.admin.frm2',
        receivers = [],
    ),
)
