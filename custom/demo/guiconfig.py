#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2014 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS GUI default configuration."""

from nicos.clients.gui.config import vsplit, window, panel, tool, docked, \
    tabbed, setups

main_window = docked(
    vsplit(
        panel('status.ScriptStatusPanel'),
        # panel('watch.WatchPanel'),
        panel('console.ConsolePanel'),
    ),
    ('NICOS devices',
     panel('nicos.clients.gui.panels.devices.DevicesPanel',
           icons=True, dockpos='right',
          )
    ),
    ('Experiment Information and Setup',
     panel('nicos.clients.gui.panels.expinfo.ExpInfoPanel',
           sample_panel=tabbed(
               ('Sample changer', panel('nicos.sans1.gui.samplechanger.SamplechangerSetupPanel',
                                       image = 'custom/sans1/lib/gui/sampleChanger11.png',
                                       positions = 11), setups('sans')),
               ('TAS sample', panel('nicos.clients.gui.panels.setup_panel.TasSamplePanel'), setups('tas')),
           )
       )),
)

windows = [
    window('Editor', 'editor',
        vsplit(
            panel('scriptbuilder.CommandsPanel'),
            panel('editor.EditorPanel',
              tools = [
                  tool('Scan Generator', 'nicos.clients.gui.tools.scan.ScanTool')
              ]))),
    window('Scans', 'plotter', panel('scans.ScansPanel')),
    window('History', 'find', panel('history.HistoryPanel')),
    window('Logbook', 'table', panel('elog.ELogPanel')),
    window('Log files', 'table', panel('logviewer.LogViewerPanel')),
    window('Errors', 'errors', panel('errors.ErrorPanel')),
    # window('Downtime', 'mail', panel('nicos.clients.gui.tools.downtime.DownTimeTool')),
    # window('Live data', 'live', panel('live.LiveDataPanel')),
]

tools = [
    tool('Downtime report', 'downtime.DownTimeTool',
#        receiver='f.carsughi@fz-juelich.de',
         receiver='jens.krueger@frm2.tum.de, enrico.faulhaber@frm2.tum.de',
         mailserver='smtp.frm2.tum.de',
         sender='demo@frm2.tum.de',
        ),
    tool('Calculator', 'calculator.CalculatorTool'),
    tool('Neutron cross-sections', 'website.WebsiteTool',
         url='http://www.ncnr.nist.gov/resources/n-lengths/'),
    tool('Neutron activation', 'website.WebsiteTool',
         url='http://www.frm2.tum.de/intranet/activation/'),
    tool('Neutron calculations',
         'nicos.clients.gui.tools.website.WebsiteTool',
         url='http://www.frm2.tum.de/intranet/neutroncalc/'),
    tool('Report NICOS bug', 'website.WebsiteTool',
         url='http://trac.frm2.tum.de/redmine/projects/nicos/issues/new'),
    tool('Emergency stop button', 'estop.EmergencyStopTool',
         runatstartup=False),
]
