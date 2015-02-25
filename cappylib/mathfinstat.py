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

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

def emat(a, yt, st1):
    """calculates and returns exponential moving average for an alpha, value, and prior ema"""

    # St = a * Yt + (1 - a) * St-1
    # where:
    #   a = alpha factor from 0.0 - 1.0, but 2 / (N + 1) gives 86% weighting with large N's
    #   Yt = data point for t
    #   St-1 = last St (i.e. St from t-1)
    # see http://en.wikipedia.org/wiki/Moving_average

    return a * yt + (1.0 - a) * st1

def ema(l, a=None):
    """calcualtes and returns exponential moving average for a list of values"""

    r = 0.0
    a = 2.0 / (len(l) + 1.0) if a == None else a  # see emai comments

    for i in range(0, len(l)):
        r = emat(a, l[i], r)

    return r

##############################################################################################
# TESTING
##############################################################################################

def main():

    # ema tests
    a = emat( 2.0 / (11.0 + 1.0), 1.0 - ( 2 / (11.0 + 1.0)), 0)
    print "emat... ", True if round(a, 6) == 0.138889 else a
    b = ema([1.0 - 2.0 / (11.0 + 1.0), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print "ema... ", True if round(b, 6) == 0.022431 else b

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
