#  -*- coding: utf-8 -*-
# *****************************************************************************
# Module:
#   $Id$
#
# Author:
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# NICOS-NG, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
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
# *****************************************************************************

"""
NICOS Resi Experiment.
"""

__author__  = "$Author$"
__date__    = "$Date$"
__version__ = "$Revision$"

import os
from os import path

from nicos.utils import disableDirectory, enableDirectory, ensureDirectory
from nicos.device import Param
from nicos.errors import UsageError
from nicos.experiment import Experiment, queryCycle


class ResiExperiment(Experiment):

    parameters = {
        'cycle': Param('Current reactor cycle', type=str, settable=True),
    }

    def _expdir(self, suffix):
        return path.join(self.datapath[0], suffix)

    def new(self, proposal, title=None, **kwds):
        # Resi-specific handling of proposal number
        if isinstance(proposal, int):
            proposal = 'p%s' % proposal
        if proposal in ('template', 'current'):
            raise UsageError(self, 'The proposal names "template" and "current"'
                             ' are reserved and cannot be used')

        try:
            old_proposal = os.readlink(self._expdir('current'))
        except Exception:
            if path.exists(self._expdir('current')):
                self.log.error('"current" link to old experiment dir exists '
                                'but cannot be read', exc=1)
            else:
                self.log.warning('no old experiment dir is currently set',
                                  exc=1)
        else:
            if old_proposal.startswith('p'):
                disableDirectory(self._expdir(old_proposal))
            os.unlink(self._expdir('current'))

        # query new cycle
        if 'cycle' not in kwds:
            if self._propdb:
                cycle, _started = queryCycle(self._propdb)
                kwds['cycle'] = cycle
            else:
                self.log.error('cannot query reactor cycle, please give a '
                                '"cycle" keyword to this function')
        self.cycle = kwds['cycle']

        # checks are done, set the new experiment
        Experiment.new(self, proposal, title)

        # fill proposal info from database
        if proposal.startswith('p'):
            try:
                propnumber = int(proposal[1:])
            except ValueError:
                pass
            else:
                self._fillProposal(propnumber)

        # create new data path and expand templates
        exp_datapath = self._expdir(proposal)
        ensureDirectory(exp_datapath)
        enableDirectory(exp_datapath)
        os.symlink(proposal, self._expdir('current'))

        ensureDirectory(path.join(exp_datapath, 'scripts'))
        self.scriptdir = path.join(exp_datapath, 'scripts')

        self._handleTemplates(proposal, kwds)

        self.datapath = [
            self.datapath[0], exp_datapath
        ]

    def _handleTemplates(self, proposal, kwds):
        pass

    def finish(self):
        pass
