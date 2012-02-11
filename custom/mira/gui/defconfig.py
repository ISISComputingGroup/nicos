# Default MIRA GUI config

from nicos.gui.config import vsplit, hsplit, panel, window, tool

maint_commands = [
    ('Restart NICOS poller',
     'ssh maint@mira1 sudo /etc/init.d/nicos-system restart poller'),
    ('Restart NICOS daemon',
     'ssh maint@mira1 sudo /etc/init.d/nicos-system restart daemon'),
    ('Restart MIRA1 TACO servers',
     'ssh maint@mira1 sudo /usr/local/bin/taco-system restart'),
]


MIEZE_settings = [
    '46_69',
#    '65_97p5',
#    '74_111',
    '72_108',
#    '103_154p5',
    '99_148p5',
    '138_207',
    '139_208p5_BS',
    '200_300',
    '200_300_BS',
    '279_418p5_BS',
    '280_420',
]

default_profile_uid = '07139e62-d244-11e0-b94b-00199991c246'
default_profile_config = ('Default', [
    vsplit(
        hsplit(
            panel('nicos.gui.panels.status.ScriptStatusPanel'),
            panel('nicos.gui.panels.watch.WatchPanel')),
        panel('nicos.gui.panels.console.ConsolePanel'),
        ),
    window('Errors/warnings', 'errors', True,
           panel('nicos.gui.panels.errors.ErrorPanel')),
    window('Editor', 'editor', False,
           panel('nicos.gui.panels.editor.EditorPanel')),
    window('Live data', 'live', True,
           panel('nicos.mira.gui.live.LiveDataPanel')),
    window('Scans', 'plotter', True,
           panel('nicos.gui.panels.scans.ScansPanel')),
    window('History', 'find', True,
           panel('nicos.gui.panels.history.HistoryPanel')),
    window('Logbook', 'table', True,
           panel('nicos.gui.panels.elog.ELogPanel')),
    ], [
        tool('Maintenance',
             'nicos.gui.tools.commands.CommandsTool',
             commands=maint_commands),
        tool('Calculator',
             'nicos.gui.tools.calculator.CalculatorTool',
             mieze=MIEZE_settings),
    ]
)
