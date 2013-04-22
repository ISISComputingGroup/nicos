description = 'setup for the NICOS watchdog'
group = 'special'

# The entries in this list are dictionaries. Possible keys:
#
# 'setup' -- setup that must be loaded (default '' to mean all setups)
# 'condition' -- condition for warning (a Python expression where cache keys
#    can be used: t_value stands for t/value etc.
# 'gracetime' -- time in sec allowed for the condition to be true without
#    emitting a warning (default 5 sec)
# 'message' -- warning message to display
# 'priority' -- 1 or 2, where 2 is more severe (default 1)
# 'action' -- code to execute if condition is true (default no code is executed)

watchlist = [
      dict(condition = 'ch_value < 140',
           message = 'Choppers are down! DO SOMETHING!',
      ),
#     dict(condition = 'cooltemp_value > 300',
#          message = 'Cooling water temperature exceeds 30 C',
#          priority = 2,
#     ),
#     dict(condition = 'psdgas_value == "empty"',
#          message = 'PSD gas is empty, change bottle!',
#          priority = 2,
#          setup = 'cascade',
#     ),
]


# The Watchdog device has two lists of notifiers, one for priority 1 and
# one for priority 2.

devices = dict(
    email    = device('devices.notifiers.Mailer',
                      sender = 'wiebke.lohstroh@frm2.tum.de',
                      receivers = ['wiebke.lohstroh@frm2.tum.de',
                                   'giovanna.simeoni@frm2.tum.de'],
                      subject = 'TOFTOF Warning',
                     ),

#   smser    = device('devices.notifiers.SMSer',
#                     server = 'triton.admin.frm2',
#                     receivers = ['01719251564', '01782979497'],
#                    ),

    Watchdog = device('services.watchdog.Watchdog',
                      cache = 'tofhw.toftof.frm2:14869',
                      notifiers_1 = ['email'],
                      notifiers_2 = ['email',
#                                    'smser',
                                    ],
                      watch = watchlist,
                     ),
)
