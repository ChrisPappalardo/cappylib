##############################################################################################
# HEADER
#
# cappylib/log.py - defines a log class with methods for output to various media
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

import socket, os, datetime
from general import *
from amqp import *

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# log class - simple internal logging class; supports output to other media
class Log:

    # define log levels
    class levels:
        NAMES = ['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        NONE = 0
        CRITICAL = 1
        ERROR = 2
        WARNING = 3
        INFO = 4
        DEBUG = 5

    # data attributes
    __settings = {
        'timestamp': True,
        'utc': True,
        'logLevel': levels.DEBUG,
        'logStdout': levels.NONE,
        'logAmqp': None,  # dict of amqp info (amqpUser, amqpPass, etc.)
        'logFile': None   # list of tuples (logLevel, fileName)
        }
    __ID = ''
    __template = ''
    __eventLog = None     # list of tuples (logLevel, event)

    # constructor method - import settings and create log template string
    def __init__(self, ID, **settings):

        # import settings; overwrite defaults
        self.__settings = dict(self.__settings.items() + settings.items())

        # initialize ID, logAmqp, logFile, and eventLog
        self.__ID = ID
        if self.__settings['logAmqp'] is None: self.__settings['logAmqp'] = dict()
        if self.__settings['logFile'] is None: self.__settings['logFile'] = list()
        self.__eventLog = list() 

    # logEvent method - generates a log entry
    def logEvent(self, logLevel, event):

        # create log template string
        logTemplate = '' if not self.__template else self.__template
        if not logTemplate:
            logTemplate = ' '.join(['{0}', socket.gethostname(), str(os.getpid()), 
                                    self.__ID, '({1}): {2}'])

        # apply template to event message
        d_t = datetime.datetime
        dt = d_t.utcnow() if self.__settings['utc'] else d_t.now()
        levelName = Log.levels.NAMES[logLevel]
        event = logTemplate.format(dt.isoformat(), levelName, event)

        # save event to internal log if meets logLevel requirement
        if int(logLevel) <= int(self.__settings['logLevel']): 
            self.__eventLog.append((logLevel, event))

        # print event to stdout, if enabled and meets logLevel requirement
        if int(logLevel) <= int(self.__settings['logStdout']): print event
        
        # save event in logFiles, if any
        for (fileLevel, file) in self.__settings['logFile']:
            if int(logLevel) <= int(fileLevel):
                with open(file, "a") as fh:
                    fh.write(event + '\n')

        # send event to amqp server, if enabled
        if self.__settings['logAmqp']:
            ex = {'exchange': 'Ex', 'exchange_type': 'fanout', 'passive': False, 
                  'durable': False, 'auto_delete': True, 'nowait': False}
            Amqp(self.__settings['logAmqp']).publish(ex, event, '')

        # return formatted event message
        return event

##############################################################################################
# TESTING #
##############################################################################################

if __name__ == '__main__':

    try:

        # log test
        amqpTestConfig = {
            'username': 'guest',
            'password': 'guest',
            'host': 'localhost',
            'port': 5672,
            'virtual_host': '/'
            }
        log = Log('test', logAmqp=amqpTestConfig, logFile=[(Log.levels.DEBUG, 'test.log')])
        print 'Log...', log.logEvent(Log.levels.DEBUG, 'test log event')

    except error as e: print e.error
