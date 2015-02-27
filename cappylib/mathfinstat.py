##############################################################################################
# HEADER
#
# cappylib/mathfinstat.py - defines useful math, financial, and statistical classes and 
#                           functions for python scripts
#
# Copyright (C) 2008-2015 Chris Pappalardo <cpappala@yahoo.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this 
# software and associated documentation files (the "Software"), to deal in the Software 
# without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
# to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
#
##############################################################################################

##############################################################################################
# IMPORTS 
##############################################################################################

from __future__ import division  # this fixes 1 / 2 = 0 problem
from cappylib.general import *

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# MATH

def acct(st1, yt1, t):
    """returns smoothed accumulation for a t-period total and incremental value"""

    return st1 - st1 / t + yt1

def avg(y):
    """returns simple average of list"""
    
    return sum(y) / len(y)

def ema(l, a=None):
    """returns exponential moving average for a list of values, with optional coefficient"""

    r = 0.0

    for i in range(0, len(l)):
        r = emat(r, l[i], len(l), a)

    return r

def emat(st1, yt, t, a=None):
    """
    returns exponential moving average for a t-period EMA and incremental value
    where st1 is the previous average, yt is the incr value, and t is the size of the avg
          a can optionally be overridden with a specific coefficient, else 2/(t-1) is used
    """

    # St = a * Yt + (1 - a) * St-1
    # where:
    #   St-1 = last St (i.e. St from t-1)
    #   Yt = data point for t
    #   a = alpha factor from 0.0 - 1.0, but 2 / (N + 1) gives 86% weighting with large N's
    # see http://en.wikipedia.org/wiki/Moving_average

    a = 2.0 / (t + 1.0) if a == None else a
    return a * yt + (1.0 - a) * st1

def mmat(st1, yt, t):
    """returns modified moving average for a t-period MMA and incremental value"""

    return (st1 * (t - 1) + yt ) / t

##############################################################################################
# TESTING
##############################################################################################

def main():

    # acct test
    a = acct(14, 2.75, 14)
    print aColor('BLUE') + "acct... ", aColor('OFF'), True if a == 15.75 else a
    # ema tests
    a = ema([1 - 2 / (11 + 1), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print aColor('BLUE') + "ema... ", aColor('OFF'), True if round(a, 6) == 0.022431 else a
    a = emat(0.026917597, 0, 11)
    print aColor('BLUE') + "emat... ", aColor('OFF'), True if round(a, 6) == 0.022431 else a
    # mmat test
    a = mmat(16, 32, 14)
    print aColor('BLUE') + "emat... ", aColor('OFF'), True if round(a, 2) == 17.14 else a

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
