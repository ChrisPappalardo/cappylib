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

##############################################################################################
# IMPORTS 
##############################################################################################

import datetime
from cappylib.general import *
dt = datetime

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# nthWeekday - finds the nth weekday for a given month and day
def nthWeekday(year, month, nth, weekday):
    """finds nth weekday for a given month and day"""

    result = dt.datetime(year, month, 1)
    counts = dict([(x, 0) for x in range(0, 7)])

    # step through each day in year/month and count each day of week
    while result < dt.datetime(year, month, 1) + dt.timedelta(days=31):

        counts[result.weekday()] += 1;

        # if nth weekday is reached, return result
        if counts[weekday] >= nth:
            return result

        result += dt.timedelta(days=1)

    # if nth weekday is never reached, return False
    return False

# previousWeekday - finds the weekday previous to date
def previousWeekday(date, weekday):
    """finds the weekday previous to date"""

    # step back by day until day of week is reached
    while date >= dt.datetime(date.year, date.month, 1):

        if date.weekday() == weekday:
            return date

        date -= dt.timedelta(days=1)

    # if weekday is never reached in month, return False
    return False

# holiday - a class with static elements for defining and checking special dates and times
class holiday(object):
    """a class with static elements for defining and checking special dates and times"""

    none = 0
    weekday = 1
    w_us_time_nyse = 2
    h_all_weekend = 4
    h_us_time_nyseam = 8
    h_us_time_nysepm = 16
    h_us_newyearsday = 32
    h_us_mlkday = 64
    h_us_presidentsday = 128
    h_us_goodfriday = 256
    h_us_memorialday = 512
    h_us_independenceday = 1024
    h_us_laborday = 2048
    h_us_columbusday = 4096
    h_us_veteransday = 8192
    h_us_thanksgiving = 16384
    h_us_christmas = 32768

    @staticmethod
    def check(holiday, _dt):
        """static method to check if holiday resolves to datetime _dt"""

        return True

    def __init__(self):
        pass

# dateCheck - returns true if datetime _dt is in allow list or not in deny list, false otherwise
def dateCheck(_dt, allow=None, deny=None):
    """returns true if datetime _dt is in allow list or not in deny list, false otherwise"""

    for allowed in [allow] if type(allow) != list else allow:
        if holiday.check(_dt, allowed): return True
    for denied in [deny] if type(deny) != list else deny:
        if holiday.check(_dt, denied): return False
    return True

# calcTimeseries - calculates a time series based on inputs
def calcTimeseries(count, days=0, mins=0, secs=0, dateStart=datetime.datetime.utcnow(),
                   dateEnd=datetime.datetime(1970, 1, 1), dateCheck=lambda *x, **y: True, 
                   criteria=None):
    """calculates a time series for an interval, count, and start/stop dates;
       optionally checks generated dates against a passed dateCheck function"""

    result = list()
    interval = datetime.timedelta(days=days, minutes=mins, seconds=secs)

    # generate dates going back by interval from dateStart until count is hit
    while len(result) < count:
        
        # add date if dateCheck returns True
        if dateCheck(datetime=dateStart, criteria=criteria):
            result.append(dateStart.strftime("%Y-%m-%d %H:%M:%S"))
            
        # if dateEnd is reached, break
        if dateStart <= dateEnd:
            break

        dateStart -= interval

    return result

##############################################################################################
# TESTING #
##############################################################################################

def main():

    # date function tests
    d_t = datetime.datetime
    print aColor('BLUE') + 'calcTimeseries(count=10, mins=5, dateStart=now())...', \
        aColor('OFF'), calcTimeseries(10, mins=5, dateStart=d_t.now())
    print aColor('BLUE') + 'nthWeekday(year=2012, month=1, nth=3, weekday=MONDAY)...', \
        aColor('OFF'), nthWeekday(2012, 1, 3, enum.weekdays.MONDAY)
    print aColor('BLUE') + 'previousWeekday(date=5/31/12, weekday=MONDAY)...', \
        aColor('OFF'), previousWeekday(d_t(2012, 5, 31), enum.weekdays.MONDAY)
    print aColor('BLUE') + 'dateCheck(_dt=3/29/13 10:00:00, deny=goodfriday)...', \
        aColor('OFF'), dateCheck(dt.datetime(2013, 3, 29, 10, 0), holiday.h_us_goodfriday)

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
