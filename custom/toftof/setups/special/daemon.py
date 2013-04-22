description = 'setup for the execution daemon'

group = 'special'

import hashlib

devices = dict(
    UserDB = device('frm2.auth.Frm2Authenticator'),
    Auth   = device('services.daemon.auth.ListAuthenticator',
                    hashing = 'md5',
                    # first entry is the user name, second the hashed password, third the user level
                    passwd = [('guest', '', 'guest'),
                              ('user', hashlib.md5('user').hexdigest(), 'user'),
                              ('root', 'f88868f6f9fe65b21dadc685ef6ad99f', 'admin'),
                             ],
                   ),
    Daemon = device('services.daemon.NicosDaemon',
                    server = 'tofhw.toftof.frm2',
                    authenticators = ['UserDB', 'Auth'], # or ['UserDB', 'Auth']
                    loglevel = 'info',
                   ),
)
