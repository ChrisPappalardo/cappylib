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
    h_us_nyse_amclosed = 1
    h_us_nyse_pmclosed = 2
    h_us_weekend = 4
    h_us_newyearsday = 8
    h_us_mlkday = 16
    h_us_presidentsday = 32
    h_us_goodfriday_halfday = 64
    h_us_eastersunday = 128
    h_us_memorialday = 256
    h_us_independenceday = 512
    h_us_laborday = 1024
    h_us_columbusday = 2048
    h_us_veteransday = 4096
    h_us_thanksgiving = 8192
    h_us_christmas = 16384
    h_us_all = reduce(lambda x, y: x | y, [1 << x for x in range(1, 16)])
#65536
#131072
#262144
#524288
#1048576
#2097152
#4194304
#8388608
#16777216
#33554432
#67108864
#134217728
#268435456
#536870912
#1073741824
#2147483648

    @staticmethod
    def check(_dt, h):
        """static method to check if holiday h resolves to datetime _dt"""

        result = False  # default result is False
        dow = enum.weekdays

        # Before the NYSE opening bell
        if h & holiday.h_us_nyse_amclosed:
            result = result | (_dt.time() < dt.time(9, 30))

        # On or after the NYSE closing bell
        if h & holiday.h_us_nyse_pmclosed:
            result = result | (_dt.time() >= dt.time(16, 0))

        # Weekends
        if h & holiday.h_us_weekend:
            result = result | (_dt.weekday() in (dow.SATURDAY, dow.SUNDAY))

        # New Year's Day:  Fri Dec 31, Jan 1, and Mon Jan 2
        if h & holiday.h_us_newyearsday:
            nyDec31 = _dt.month == 12 and _dt.day == 31 and _dt.weekday() == dow.FRIDAY
            nyJan1 = _dt.month == 1 and _dt.day == 1
            nyJan2 = _dt.month == 1 and _dt.day == 2 and _dt.weekday() == dow.MONDAY
            result = result | (nyDec31 or nyJan1 or nyJan2)

        # Martin Luther King Day:  3rd Mon in Jan
        if h & holiday.h_us_mlkday:
            result = result | (_dt.date() == nthWeekday(_dt.year, 1, 3, dow.MONDAY).date())

        # Presidents' Day:  3rd Mon in Feb
        if h & holiday.h_us_presidentsday:
            result = result | (_dt.date() == nthWeekday(_dt.year, 2, 3, dow.MONDAY).date())

        # Good Friday:  the Fri before Easter Sun is a half-day on the US:NYSE
        if h & (holiday.h_us_goodfriday_halfday | holiday.h_us_eastersunday):
            year = _dt.year
            a = year % 19 # % is modulo operator, like division but returns remainder
            b = year // 100
            c = year % 100
            d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
            e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
            f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
            month = f // 31
            day = f % 31 + 1
            if h & holiday.h_us_eastersunday:
                result = result | (_dt.date() == dt.datetime(year, month, day).date())
            elif h & holiday.h_us_goodfriday_halfday:
                d = previousWeekday(dt.datetime(year, month, day), dow.FRIDAY)
                result = result | (_dt.date() == d.date() and _dt.time() >= dt.time(13, 00))

        # Memorial Day:  last Mon in May
        if h & holiday.h_us_memorialday:
            result = result | (_dt.date() == previousWeekday(dt.datetime(_dt.year,5,31),
                                                             dow.MONDAY).date())

        # Independence Day:  Jul 4
        if h & holiday.h_us_independenceday:
            result = result | (_dt.month == 7 and _dt.day == 4)

        # Labor Day:  1st Mon of Sep
        if h & holiday.h_us_laborday:
            result = result | (_dt.date() == nthWeekday(_dt.year, 9, 1, dow.MONDAY).date())

        # Columbus Day:  2nd Mon of Oct
        if h & holiday.h_us_columbusday:
            result = result | (_dt.date() == nthWeekday(_dt.year, 10, 2, dow.MONDAY).date())

        # Veterans' Day:  Nov 11
        if h & holiday.h_us_veteransday:
            result = result | (_dt.month == 11 and _dt.day == 11)

        # Thanksgiving Day:  4th Thu of Nov
        if h & holiday.h_us_thanksgiving:
            result = result | (_dt.date() == nthWeekday(_dt.year, 11, 4, dow.THURSDAY).date())

        # Christmas Day:  Dec 25
        if h & holiday.h_us_christmas:
            result = result | (_dt.month == 12 and _dt.day == 25)

        return result

    def __init__(self):
        pass

# dateCheck - returns true if datetime _dt is in allow list or not in deny list, else false
def dateCheck(_dt, allow=None, deny=None):
    """returns true if datetime _dt is in allow list or not in deny list, false otherwise"""

    allow = [] if allow == None else allow
    deny = [] if deny == None else deny

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
    print aColor('BLUE') + 'calcTimeseries(count=10, mins=5, dateStart=now())...', \
        aColor('OFF'), calcTimeseries(10, mins=5, dateStart=dt.datetime.now())
    print aColor('BLUE') + 'nthWeekday(year=2012, month=1, nth=3, weekday=MONDAY)...', \
        aColor('OFF'), nthWeekday(2012, 1, 3, enum.weekdays.MONDAY)
    print aColor('BLUE') + 'previousWeekday(date=5/31/12, weekday=MONDAY)...', \
        aColor('OFF'), previousWeekday(dt.datetime(2012, 5, 31), enum.weekdays.MONDAY)
    h = {'nyse_amclosed': (holiday.h_us_nyse_amclosed, dt.datetime(2013,12,16,9,29)),
         'nyse_pmclosed': (holiday.h_us_nyse_pmclosed, dt.datetime(2013,12,16,16,00)),
         'weekend': (holiday.h_us_weekend, dt.datetime(2013,12,15)),
         'newyearsday': (holiday.h_us_newyearsday, dt.datetime(2012,1,2)),
         'mlkday': (holiday.h_us_mlkday, dt.datetime(2014,1,20)),
         'presidentsday': (holiday.h_us_presidentsday, dt.datetime(2014,2,17)),
         'goodfriday_halfday': (holiday.h_us_goodfriday_halfday, dt.datetime(2013,3,29,13,1)),
         'memorialday': (holiday.h_us_memorialday, dt.datetime(2013,5,27)),
         'independenceday': (holiday.h_us_independenceday, dt.datetime(2013,7,4)),
         'laborday': (holiday.h_us_laborday, dt.datetime(2013,9,2)),
         'columbusday': (holiday.h_us_columbusday, dt.datetime(2013,10,14)),
         'veteransday': (holiday.h_us_veteransday, dt.datetime(2013,11,11)),
         'thanksgiving': (holiday.h_us_thanksgiving, dt.datetime(2013,11,28)),
         'christmas': (holiday.h_us_christmas, dt.datetime(2013,12,25)),
         'us_all': (holiday.h_us_all, dt.datetime(2013,12,25))}
    for k in h.keys():
        print aColor('BLUE') + 'holiday.check({0}, {1})...'.format(k,h[k][1]), \
            aColor('OFF'), holiday.check(h[k][1], h[k][0])
    h = [holiday.h_us_nyse_amclosed, holiday.h_us_nyse_pmclosed, holiday.h_us_christmas]
    print aColor('BLUE') + 'dateCheck(12/24/13-12:00,deny=[amclosed,pmclosed,christmas])...', \
        aColor('OFF'), dateCheck(dt.datetime(2013,12,24,12,0), deny=h)
    print aColor('BLUE') + 'dateCheck(12/24/13-12:00,allow=[amclosed,pmclosed,christmas])...',\
        aColor('OFF'), dateCheck(dt.datetime(2013,12,24,12,0), allow=h)

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
