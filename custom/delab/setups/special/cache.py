description = 'setup for the cache server'
group = 'special'

devices = dict(
    DB     = device('services.cache.server.FlatfileCacheDatabase',
                    storepath = '/data/cache',
                    loglevel = 'info',
                   ),

    Server = device('services.cache.server.CacheServer',
                    db = 'DB',
                    server = '0.0.0.0',
                    loglevel = 'info',
                   ),
)
