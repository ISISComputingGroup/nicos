description = 'Email and SMS notifiers'

group = 'lowlevel'

devices = dict(
    email  = device('nicos.devices.notifiers.Mailer',
                    description = 'Reports via email',
                    lowlevel = True,
                    mailserver = 'mailhost.frm2.tum.de',
                    sender = 'panda@frm2.tum.de',
                    copies = [('pcermak@frm2.tum.de', 'important')],
                    subject = '[PANDA]',
                   ),
    email1   = device('nicos.devices.notifiers.Mailer',
                      mailserver = 'mailhost.frm2.tum.de',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['pcermak@frm2.tum.de', 'andreas.frick@frm2.tum.de', 'astrid.schneidewind@frm2.tum.de'],
                      subject = '[PANDA warning]',
                      lowlevel = True,
                     ),

    email2  = device('nicos.devices.notifiers.Mailer',
                      mailserver = 'mailhost.frm2.tum.de',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['pcermak@frm2.tum.de'],
                      subject = '[PANDA]',
                      lowlevel = True,
                     ),

    email3  = device('nicos.devices.notifiers.Mailer',
                      mailserver = 'mailhost.frm2.tum.de',
                      sender = 'panda@frm2.tum.de',
                      receivers = ['astrid.schneidewind@frm2.tum.de'],
                      subject = '[PANDA]',
                      lowlevel = True,
                     ),

    smser    = device('nicos.devices.notifiers.SMSer',
                      server = 'triton.admin.frm2',
                      receivers = ['017697526049', '015788490767'],
                      lowlevel = True,
                     ),

    smspetr    = device('nicos.devices.notifiers.SMSer',
                      server = 'triton.admin.frm2',
                      receivers = ['017697526049'],
                      lowlevel = True,
                     ),
)