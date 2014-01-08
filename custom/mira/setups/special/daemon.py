description = 'setup for the daemon'
group = 'special'

devices = dict(
    Auth   = device('services.daemon.auth.ListAuthenticator',
                    hashing = 'md5',
                    passwd = [('admin', 'cf5bdfb40421ac1f30cc4d45b66b5a81', 'admin'),
                              ('', '', 'user')]),
    Daemon = device('services.daemon.NicosDaemon',
                    server = 'mira1',
                    loglevel = 'info',
                    authenticators = ['Auth']),
)
