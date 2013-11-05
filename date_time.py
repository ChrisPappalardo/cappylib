##############################################################################################
# HEADER
#
# cappylib/date_time - defines useful date and time functions for python scripts
#
# Copyright (C) 2008-2013 Chris Pappalardo <cpappala@yahoo.com>
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
#
# MySQL and all related client libraries, including the MySQL Connector/Python, are
# Copyright (C) Oracle Corporation and its affiliated companies ("Oracle").  Use and
# distribution in this case is permitted under Oracle's Free and Open Source Software
# ("FOSS") License Exception, which allows developers of FOSS applications (including those
# licensed under the MIT License as of the original copyright date) to include Oracle's MySQL
# Client Libraries with their FOSS applications.  MySQL Client Libraries are typically
# licensed pursuant to version 2 of the General Public License ("GPL"), but this exception
# permits distribution of certain MySQL Client Libraries with a developer's FOSS applications
# licensed under the terms of another FOSS license, even though such other FOSS license may
# be incompatible with the GPL.
#
##############################################################################################
#
# pika is Copyright (C) 2009-2011 VMWare, Inc. and Tony Garnock-Jones.  Use, modification, and
# distribution is subject to the Mozilla Public License, Version 1.1, which can be obtained 
# from http://www.mozilla.org/MPL/
#
##############################################################################################

##############################################################################################
# IMPORTS 
##############################################################################################

import datetime
from general import *

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# calcTimeseries - calculates a time series based on inputs
def calcTimeseries(count, days=0, mins=0, secs=0, dateStart=datetime.datetime.utcnow(),
                   dateEnd=datetime.datetime(1970, 1, 1), type=None,
                   dateCheck=lambda *x, **y: True):
    """calculates a time series for an interval, count, and start/stop dates;
       optionally checks generated dates against a passed dateCheck function"""

    result = []
    interval = datetime.timedelta(days=days, minutes=mins, seconds=secs)

    # generate dates going back by interval from dateStart until count is hit
    while len(result) < count:
        
        # add date if dateCheck returns True
        if dateCheck(date=dateStart, type=type):
            result.append(dateStart.strftime("%Y-%m-%d %H:%M:%S"))
            
        # if dateEnd is reached, break
        if dateStart <= dateEnd:
            break

        dateStart -= interval

    return result

# isBusinessDate - returns true of datetime is a business datetime
def isBusinessDate(datetime, type=None):
    pass

# nthWeekday - finds the nth weekday for a given month and day
def nthWeekday(year, month, nth, weekday):
    """finds nth weekday for a given month and day"""

    d_t = datetime
    result = d_t.datetime(year, month, 1)
    counts = dict([(x, 0) for x in range(0, 7)])

    # step through each day in year/month and count each day of week
    while result < d_t.datetime(year, month, 1) + d_t.timedelta(days=31):

        counts[result.weekday()] += 1;

        # if nth weekday is reached, return result
        if counts[weekday] >= nth:
            return result

        result += d_t.timedelta(days=1)

    # if nth weekday is never reached, return False
    return False

# previousWeekday - finds the weekday previous to date
def previousWeekday(date, weekday):
    """finds the weekday previous to date"""

    # step back by day until day of week is reached
    while date >= datetime.datetime(date.year, date.month, 1):

        if date.weekday() == weekday:
            return date

        date -= datetime.timedelta(days=1)

    # if weekday is never reached in month, return False
    return False

##############################################################################################
# TESTING #
##############################################################################################

if __name__ == '__main__':

    try:

        # date function tests
        d_t = datetime.datetime
        print aColor('BLUE') + 'calcTimeseries(count=10, mins=5, dateStart=now())...', \
            aColor('OFF'), calcTimeseries(10, mins=5, dateStart=d_t.now())
        print aColor('BLUE') + 'nthWeekday(year=2012, month=1, nth=3, weekday=MONDAY)...', \
            aColor('OFF'), nthWeekday(2012, 1, 3, enum.weekdays.MONDAY)
        print aColor('BLUE') + 'previousWeekday(date=5/31/12, weekday=MONDAY)...', \
            aColor('OFF'), previousWeekday(d_t(2012, 5, 31), enum.weekdays.MONDAY)

    except error as e: print e.error
