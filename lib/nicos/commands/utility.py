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
#   Georg Brandl <georg.brandl@frm2.tum.de>
#   Björn Pedersen <bjoern.pedersen@frm2.tum.de>
#
# *****************************************************************************

"""Module for utility user commands.

    This module contains utility functions that are of general
    interesst for user scripts, e.g different list generators
    and other helper functions.
"""

from __future__ import with_statement



import math
import numpy
from nicos.core import UsageError
from nicos.commands import usercommand, helparglist

def RangeListByStep(start, end=None, inc=None):
    """Generate a list of points within [from;to]

     A range function, that does accept float increments...

     usage example:
     l1 = RangeList(1,2,0.5)

     l1 will be:  [1., 1.5, 2.]
     """

    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = math.copysign(1., end - start)

    if inc == 0.0:
        raise UsageError('Increment needs to differ from zero')

    if math.copysign(1.0, inc) != math.copysign(1.0, (end - start)):
        raise UsageError('Start/end points and increment are inconsistent')

    res = []
    while 1:
        nextval = start + len(res) * inc
        # break, if less then 0.5 full steps remain to the endpoint
        if inc > 0 and nextval > end - (0.001 * inc):
            res.append(end)
            break
        elif inc < 0 and nextval < end - (0.001 * inc):
            res.append(end)
            break
        res.append(nextval)

    return res

def RangeListByCount(start, end=None, num=2):
    """Generate a list of points within [from;to] with num points

     A range function, that gives evenly spaced points.
     Uses simply the numpy.linspace function

     usage example:
     l1 = RangeList(1,2,3)

     l1 will be:  [1., 1.5, 2.]
     """
    if end is None:
        end , start = start, 0.0
    return numpy.linspace(start, end, num)

@usercommand
@helparglist('start, end, [step | num]')
def floatrange(start, end, step=None, **kw):
    """ Generate a linear range of values

    Generate a linear range of values from start to end,
    with either a specified step width or number of values

    start, end are the start- and end values
    step is the stpewidth and shall always be positive
    num is the number of values desired

    Examples:
    floatrange(1,2,step = 0.1) = [1, 1.1, 1.2 ... 1.9, 2.0]
    floatrange(2,1,step = 0.1) = [2, 1.9, 1.8 ... 1.1, 1.0]
    floatrange(1,2,num = 3) = [1, 1.5, 2]
    """
    start = float(start)
    end = float(end)
    # case 1: stepwidth given
    if step is not None:
        if kw.get('num') is not None:
            raise UsageError('Both step and num given, only one is allowed.')
        if step <= 0.0:
            raise UsageError('Increment has to be positive and gretaer than zero.')
        step = math.copysign(float(step), (end - start))
        return RangeListByStep(start, end, step)
    else:
        num = int(kw.get('num'))
        if num is None:
            raise UsageError('Please give either step or num.')
        if num < 2:
            raise UsageError('The number of steps should be greater than 1.')
        return RangeListByCount(start, end, num)

@usercommand
def RangeListLog(start, end, num=10):
    """ Generate a log spaced list with specified number of steps

    Example:
        l3 = RangeListLog(1., 2., 3)
        l3 is [1.0, 1.4142135623730949, 2.0]
    """
    if start < 0 or end < 0:
        raise UsageError('Log spacing is only defined for positive values')


    res = numpy.logspace(math.log10(start), math.log10(end), num)
    return res

def identity(x):
    ''' Identity function '''
    return x

@usercommand
def RangeListGeneral(start, end, num=10, func = identity, funcinv = None):
    ''' Generate a list spaced evenly in arbitrary functions

    func: a function taking one argument for the values should be spaced evenly,
          can also be a lambda function.
    funcinv: the inverse function to func, can be omitted if identical to func

    his function does less error checking  and will raise an error on wrong
    input values (e.g. outside the domain of the used function)


    Examples:
     evenly spaced points on a sine
     x=RangeListGeneral(0,math.pi/2,5,math.sin,math.asin)
         [0.0 0.252680255142 0.523598775598 0.848062078981 1.57079632679]
     evenly spaced in 1/x:
     x=RangeListGeneral(1,100,10,lambda(x):1/x)
        [1.0 1.12359550562 1.28205128205 1.49253731343 1.78571428571
         2.22222222222 2.94117647059 4.34782608696 8.33333333333 100.0]

    '''
    start = float(start)
    end = float(end)
    try:
        s1 = func(start)
        s2 = func(end)
        res = numpy.linspace(s1, s2, num)
        if funcinv is None:
            funcinv = func
        ufuncinv = numpy.frompyfunc(funcinv,1,1)
        res = ufuncinv(res).astype(numpy.float64)
        return res
    except Exception, e:
        raise RuntimeError(str(e))
