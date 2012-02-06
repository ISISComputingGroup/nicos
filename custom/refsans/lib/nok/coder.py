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
#   Jens Krüger <jens.krueger@frm2.tum.de>
#
# *****************************************************************************

"""Taco coder class for NICOS."""

__version__ = "$Revision$"

import sys
from Encoder import Encoder

from nicos.core import Readable, Moveable, Override, status, oneofdict, \
    oneof, Param
from nicos.abstract import Coder as BaseCoder
from nicos.taco.io import AnalogInput

class Coder(BaseCoder):
    """NOK coder implementation class.
    """

    attached_devices = {
        'port' : (AnalogInput, 'analog input device'),
        'ref' : (AnalogInput, 'referencing analog input device'),
    }

    parameters = {
        'refhigh' : Param('High reference', 
                          type = float,
                          default = 19.8, # 2 * 9.9
                         ),
        'refwarn' : Param('Reference warning',
                          type = float,
                          default = 18.0, # 9.0 * 2
                         ),
        'reflow'  : Param('Low reference',
                          type = float,
                          default = 17.0, # 8.0 * 2
                         ),
        'corr'     : Param('Correction type',
                          type = oneof('none', 'mul', 'table'),
                          default = 'mul',
                         ),
        'tabfile' : Param('Correction table file',
                          type = str,
                          mandatory = False,
                         ),
        'mul'     : Param('Multiplier',
                          type = float,
                          default = 1.0,
                         ),
        'off'     : Param('Offset',
                          type = float,
                          default = 0.0,
                         ),
        'snr'    : Param('Serial number',
                          type = int,
                          mandatory = True,
                         ),
        'length'  : Param('Potionmeter length',
                          type = float,
                          mandatory = True,
                         ),
        'sensitivity' : Param('Sensitivity',
                              type = float,
                              mandatory = True,
                             ),
        'position' : Param('Position',
                           type = oneofdict({'top' : -1, 'bottom' : 1}),
                           mandatory = True,
                           default = 'bottom',
                          ),
    }

#   valuetype = oneofdict({-1: 'top', 1: 'bottom'})

    def doSetPosition(self, target):
        self._taco_guard(self._dev.setpos, target)

    avg     = 1
    avgwait = 0.1

    def doInit(self) :
        pass

    def doGetPar (self,lable,Logging=True):
        try:        val = getattr(self,lable)
        except: 
            try:    val = getattr(self,'_'+lable)
            except: 
                try:    val = getattr(self,'_cl_poti__'+lable)
                except: raise Error('no such Parameter: >'+lable+'<')
        try:    return float(val)
        except: return val

    #---------------------------------------------------------------------------
    def doSetPar (self,lable,Value):
        #print 'V',self.doGetPar(lable)
        try:        
                    val = setattr(self,lable,Value)
        except: 
            try:    val = setattr(self,'_'+lable,Value)
            except: 
                try:    val = setattr(self,'_cl_poti__'+lable,Value)
                except: raise Error('no such Parameter: >'+lable+'<')
        #print 'N',self.doGetPar(lable)
        
    #---------------------------------------------------------------------------
    def __formula(self, data, direction):
        """the only positon for calculation
        direction = True:  get the position for raw and ref
        direction = False: get new parameter for mul and off
        """
        self.log.debug(self, '%f %f', (data[0], data[1]))
        E = self.position / self.sensitivity * 1000
        self.log.debug(self, 'E = %f' % (E, ))
        tmp = E * data[0] / data[1]
        lkorr = self.corr
        if lkorr == 'table':
            lkorr = 'mul'
        if direction: 
            if lkorr ==  'mul':     
                tmp *= self.mul
            return tmp + self.off
        else:
            if   lkorr == 'none': 
                tmp = data[0] # /E
            elif lkorr ==  'mul': 
                tmp = self.mul * data[0] #/E
            return (tmp, self.off + data[1])
    #---------------------------------------------------------------------------
    def correction(self, data):
        return self.__formula(data, False)
    #---------------------------------------------------------------------------
    def doRead (self, typ='POS') :
        """Plausibilitaet:
        1. ref must be in a given range (depend on ADC)
        2. RAWvalue must be in a given range (depend on NOK)
        """
        
        self.log.debug(self, 'poti read')
        Status = ''
        ref    = 0
        RAWValue = 0
        lkorr = self.corr
        # avg = int(self.avg) #ohne bedeutung!!!! 26.10.2009 15:09:30
        # AVGref = cl_auto_avg(0.001)
        # AVGraw = cl_auto_avg(0.001)
        self.log.debug(self, 'poti read enter while')
        while True:
            exit = True
            # read ref      ----------------------------------------------------
            try:        
                ref = 2.0 * self._adevs['ref'].read() # wegen der Resistoren
            except:     
                try:    
                    ref = float(self._adevs['ref'].read())*2.0 #wegen der Resistoren
                except: 
                    self.log.warning(self,  'readerror REF 2. (1/2));') #18.06.2009 07:38:57
                    exit = False
            try:        
                RAWValue = float(self._adevs['port'].read()) #so lassen #Die Dose muss gehen
            except: 
                try:    
                    RAWValue = float(self._adevs['port'].read()) #so lassen #Die Dose muss gehen
                except: 
                    self.log.warning('readerror RAWVALUE 2. (2/2);') #18.06.2009 07:39:53
                    exit = False
            if exit:
                break
        self.log.debug(self, '%f %f', (RAWValue, ref))
        # Range of RAWValue, if it is outside of expection, the cable may be broken
        # test range of ref lack of resolution 9.5 < ref > 10 clip!
        if abs(ref) >= self.refhigh :
            self.log.warning(self,  'REFhigh; ')
        if   abs(ref) <  self.reflow:
            self.log.warning(self, 'REFlow; ')
        elif abs(ref) <  self.refwarn: 
            self.log.warning(self, 'REFwarn; ')

        try:    
            Position = self.__formula([RAWValue, ref], True)
            if lkorr ==  'tabelle':
                try:    
                    p = self.korrtable[Position]
                    Position = p
                except: 
                    lkorr = 'mul'
        except: 
            self.log.error(self, 'calc.Error : %s' % (str(sys.exc_info()[1])))

        # Summarize Result
        if len(Status) == 0: 
            self.log.debug(self, 'okay')

        if 'OFF'       == typ.upper(): 
            return {'off':-RAWValue/ref}
        if 'POS'       == typ.upper(): 
#            return {'Position':Position,'korr':lkorr}
             return Position
        if 'PARAMETER' == typ.upper(): 
            return {'korr':lkorr,'off':self.__off,'Empfindlichkeit':self.Empfindlichkeit,'mul':self.__mul,'avg':'auto'}#self.avg}
        else:                          
            return {'korr':lkorr,'RAWValue':RAWValue,'ref':ref,'Position':Position,'Status':Status}

