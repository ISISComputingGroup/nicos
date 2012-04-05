#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

"""Analysator stuff for PANDA"""

__version__ = "$Revision$"

from nicos import status
from nicos.core import Param, tacodev, usermethod, Moveable
from nicos.generic.axis import Axis

from IO import DigitalOutput

from wechsler import Beckhoff


class AnaBlocks( Moveable ):
    attached_devices = {
        'beckhoff': (Beckhoff,'X'),
    }
    parameters = {
        'powertime':   Param('How long to power pushing down blocks', type=int, default=10, settable=True),
        'unit': Param('unit = ""', type=str, default='', settable=False),
    }

    @property
    def bhd(self):  # BeckHoffDevice
        return self._adevs['beckhoff']

    def doInit(self):
        self._timer=None
        # disable beckhoff watchdog
        self.bhd.WriteWordOutput(0x1120,0)
        # XXX TODO: init KL3202 channel 0 to 0..1.2KOhm or to read PT1000
    
        #~ self.bhd.WriteReg( 4, 31, 0x1235)   # enable user regs
        #~ assert( self.bhd.ReadReg( 4, 31 ) == 0x1235 ) # make sure it has worked, or bail out early!

        #~ self.bhd.WriteReg( 4, 32, self.bhd.ReadReg( 4, 32 ) | 4 ) # disable watchdog

    # define a input helper
    def input2(self, which ):
        try:
            return ''.join( [ str(i) for i in self.bhd.ReadBitsOutput( which, 2) ] )
        except:
            return ''.join( [ str(i) for i in self.bhd.ReadBitsOutput( which, 2) ] )

    def output2( self, where, what ):
        if what in ['00', 0]:
            self.bhd.WriteBitsOutput( where, [0,0])     # both coils off
        elif what in ['10', 1]:
            self.bhd.WriteBitsOutput( where, [0,1])     # move down
        elif what in ['01', 2]:
            self.bhd.WriteBitsOutput( where, [1,0])     # move up
        elif what in ['11', 3]:
            self.bhd.WriteBitsOutput( where, [1,1])     # both coils energized, AVOID THIS!
    
    def myread( self ):
        return ''.join([ '1' if self.bhd.ReadBitOutput( i ) else '0' for i in range(34,-2,-2) ])
        
    def doRead( self ):
        return int(eval( '0b'+self.myread() ))
    
    def doStatus( self ):
        r=''
        for i in range(0,36,2):
            j= self.bhd.ReadBitOutput(i)+2*self.bhd.ReadBitOutput(i+1)
            r= ['_','1','0','X' ][j] + r
        return status.OK, 'idle: ' + r
    
    def doStart( self, pattern ):
        if self._timer:
            try:
                self._timer.cancel()
            except:
                pass
            try:
                self._timer.join(0.1)
            except:
                pass
            self._timer=None
        old=self.doRead()
        for i in range(18):
            # try to be clever: only activate/deactivate bits which differ from current status....
            if (pattern >> i) & 1 == (old >> i) & 1:
                continue        # skip equal bits
            if (pattern >> i) &1:   # bit is set:
                self.log.debug('block %d is going up'%(i+1))
                self.output2( 2*i, '01' )
            else:
                self.log.debug('block %d is going down'%(i+1))
                self.output2( 2*i, '10' )
        if self.powertime>=1:
            import threading
            self._timer=threading.Timer( self.powertime, self.powersaver )
            self._timer.start()  # switch off down's after powertime seconds

    def powersaver( self ):
        for i in range(0,36,2):
            #~ self.log.debug('Checking block %d'%(i/2+1))
            if self.input2(i)=='01':
                self.log.debug('Save Power in AnaBlock %d'%(i/2+1))
                self.output2(i,0)
        #~ self.log.debug('Saved power')
    
class ATT_Axis(Axis):
    attached_devices = {
        'anablocks': (AnaBlocks,'AnaBlocks-device'),
    }

    parameters = {
        'windowsize':   Param('Window size', default=11.5, unit='deg'),
        'blockwidth':   Param('Block width', default=15.12, unit='deg'),
        'blockoffset':  Param('Block offset', default=-7.7, unit='deg'),
    }

    def doInit(self):
        Axis.doInit(self)

    def _duringMoveAction(self, position):
        self._move_blocks(position)

    def _postMoveAction(self):
        self._move_blocks(self.read())

    def doReset(self):
        Axis.doReset(self)
        self._move_blocks(self.read())

    def _move_blocks(self, pos):
        # calculate new block positions
        code=0
        uwl = pos + self.windowsize/2.0
        lwl = pos - self.windowsize/2.0
        for j in range(18):
            lbl = self.blockwidth*(8-j) + self.blockoffset
            ubl = self.blockwidth*(9-j) + self.blockoffset
            blockup = 0
            if ubl >= lwl:  # block is not left to window
                if lbl <= uwl:  # block is not right to window
                    blockup = 1
            code+= blockup<< j
        self._adevs['anablocks'].start( code )

    @usermethod
    def allblocksdown(self):
        self._adevs['anablocks'].start( 0 )

    @usermethod
    def doorblocksup(self):
        self._adevs['anablocks'].start( 63 | self._adevs['anablocks'].target )

    @usermethod
    def doorblocksdown(self):
        self._move_blocks( self.target )

    @usermethod
    def allblocksup(self):
        self._adevs['anablocks'].start( 0x3ffff )   # all 18 blocks up

    @usermethod
    def printstatusinfo(self):
        blocks = bin( self._adevs['anablocks'].read() )[2:]
        # fill up to 18 chars
        blocks = '0' * (18 - len(blocks)) + blocks
        self.log.info('blocks up: %s' % blocks)

