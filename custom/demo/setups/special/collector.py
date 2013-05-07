description = 'setup for the NICOS collector'
group = 'special'

devices = dict(
    Global    = device('services.collector.GlobalCache',
                       cache = 'localhost:14716',
                       prefix = 'nicos/demosys/',
                      ),

    Collector = device('services.collector.Collector',
                       cache = 'localhost:14869',
                       globalcache = 'Global',
                      ),
)
