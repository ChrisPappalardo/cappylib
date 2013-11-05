##############################################################################################
# HEADER
#
# cappylib/prontab - defines a crontab-style class for running automated processes in python
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

import datetime, os, time
from cappylib.general import *
#import sys, re, mysql.connector, socket, os, pika, logging, ast, time
#from mysql.connector import errorcode
#from datetime import datetime, timedelta

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# ProntabSet - defines a set class for Prontab that matches any and every time element
class ProntabSet(set):
    """a set for Prontab that matches any and every time element, e.g. *"""
    def __contains__(self, item): return True

# ProntabEvent - defines a class that describes prontab events
class ProntabEvent(object):
    """class that describes events in cron-style scheduler class for python"""

    @staticmethod
    def toSet(obj):
        """static Prontab method to convert arg to set"""

        if isinstance(obj, (int, long)):
            return set([obj]) # single item
        if not isinstance(obj, set):
            return set(obj) # force to set
        return obj

    @staticmethod
    def parseStr(obj, t):
        """static Prontab method to convert string objects '*/n' to a set of t time units; 
           where obj is arbitrary and t is a range of time units"""

        # if obj is a string and meets the parse criteria, convert to a set
        if isinstance(obj, str) and re.search('^\*\/(\d{1,})$', obj):
            n = re.search('^\*\/(\d{1,})$', obj).group(1)
            return set([i for i in t if i%n == 0])
        # otherwise, pass s through
        else:
            return obj

    def __init__(self, action, minute=ProntabSet(), hour=ProntabSet(), day=ProntabSet(), 
                 month=ProntabSet(), dow=ProntabSet(), args=(), kwargs={}):
        """create events from time args; time args can be numbers, sets of numbers, or 
           '*/n' where n is time interval count for arbitrary time units"""

        self.minute = ProntabEvent.toSet(ProntabEvent.parseStr(minute, range(0, 59)))
        self.hour = ProntabEvent.toSet(ProntabEvent.parseStr(hour, range(0, 23)))
        self.day = ProntabEvent.toSet(ProntabEvent.parseStr(day, range(1, 31)))
        self.month = ProntabEvent.toSet(ProntabEvent.parseStr(month, range(1, 12)))
        self.dow = ProntabEvent.toSet(ProntabEvent.parseStr(dow, range(0, 6)))
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def checkTime(self, t):
        """Returns True if timetuple t meets internal schedule criteria"""

        return ((t.tm_min     in self.minute) and
                (t.tm_hour    in self.hour) and
                (t.tm_mday    in self.day) and
                (t.tm_mon     in self.month) and
                (t.tm_wday    in self.dow))

# Prontab - cron-style scheduler class for python
class Prontab(object):
    """cron-style scheduler class for python"""

    def __init__(self, *events):
        """init with one or more ProntabEvent objects"""

        self.events = events
        for e in self.events: e.pid = 0  # store child pid in event object

    def run(self):
        """cycles through all events every second; if checkTime(), forks and calls
           action with args, storing child pid in event object; only calls action on 
           events with non-active child pids"""

        while True:

            # step through each event
            for e in self.events:

                # if current time meets event criteria and event isnt running
                if e.checkTime(datetime.datetime.now().timetuple()) and not e.pid:
                    # flush stdout/err, fork process, and have child call action with args
                    sys.stdout.flush()
                    sys.stderr.flush()
                    e.pid = os.fork()
                    if not e.pid:
                        try:
                            e.action(*e.args, **e.kwargs)
                            exit(0)
                        except error as err:
                            sys.stderr.write(err.error + os.linesep)
                            exit(1)
                            
                # update child pids, reset any finished/terminated to 0
                (pid, status) = os.waitpid(e.pid, os.WNOHANG | os.WUNTRACED)
                if pid > 0:
                    e.pid = 0
                    # if child did not exit cleanly, throw an error
                    if status != 0: 
                        err = 'child (pid={0}) exited with status {1}'
                        raise error('Prontab', 'error', err.format(pid, status))

            time.sleep(1)

##############################################################################################
# TESTING #
##############################################################################################

def main():

    # prontab test
    def prontabTask(i, *args):
        if i == 3: raise error(*args)
    print 'prontab.run()...'
    try:
        p = Prontab(ProntabEvent(prontabTask, args=[1]),
                    ProntabEvent(prontabTask, args=[2]),
                    ProntabEvent(prontabTask, args=[3, 'test','term - ','prontab finished 3 tasks']))
        p.run()
    except error as e: print ' ...Done(', e.error, ')'

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
