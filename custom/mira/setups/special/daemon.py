description = 'setup for the daemon'
group = 'special'

devices = dict(
    Daemon = device('services.daemon.NicosDaemon',
                    server = 'mira1',
                    startupsetup = 'base',
                    loglevel = 'debug',
                    authenticator = None),
)
