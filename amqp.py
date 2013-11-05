##############################################################################################
# HEADER
#
# cappylib/amqp.py - defines amqp classes/functions for simple implementation of pika
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
# pika is Copyright (C) 2009-2011 VMWare, Inc. and Tony Garnock-Jones.  Use, modification, and
# distribution is subject to the Mozilla Public License, Version 1.1, which can be obtained 
# from http://www.mozilla.org/MPL/
#
##############################################################################################

##############################################################################################
# IMPORTS 
##############################################################################################

import pika, logging
from general import *

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# amqp class - amqp connection and interface
class Amqp:

    # data attributes
    persistent = False  # connection persistence
    username = ''
    password = ''
    params = None
    conn = None
    channel = None
    exchanges = None
    queues = None

    # constructor method - create amqp connection and initialize exchange and queue dicts
    def __init__(self, amqp):
        """create AMQP connection and initialize exchange and queue attributes"""

        # create exchange and queue dicts
        self.exchanges = dict()
        self.queues = dict()

        # separate out amqp parameters from credentials
        excludeKeys = ['username','password','persistent']
        self.params = dict(filter(lambda (k, v): k not in excludeKeys, amqp.items()))
        self.persistent = False if 'persistent' not in amqp.keys() else amqp['persistent']
        self.username = 'guest' if 'username' not in amqp.keys() else amqp['username']
        self.password = 'guest' if 'password' not in amqp.keys() else amqp['password']

        # create logging handler for pika warnings
        logging.basicConfig()

    # connect method - connects to amqp server
    def connect(self):
        """connects to amqp server using internal credentials, params, and conn object"""

        try:
            c = pika.PlainCredentials(self.username, self.password)
            p = pika.ConnectionParameters(credentials=c, **self.params)
            self.conn = pika.BlockingConnection(p)
            self.channel = self.conn.channel()
        except pika.exceptions as e:
            raise error('Amqp.connect', 'error', ' '.join([str(a) for a in e.args]))

    # exDeclare method - declares an exchange
    def exDeclare(self, exName, exParams):
        """declares an exchange"""

        if self.conn is None or self.conn.is_closed: self.connect()
        self._Amqp__exDeclare(exName, exParams)
        if not self.persistent: self.close()

    # __exDeclare method - declares an exchange (private) ; assumes amqp connected state
    def __exDeclare(self, exName, exParams):
        """declares an exchange (private)"""

        try:
            # declare and save the exchange, if not already declared and saved
            if exName not in self.exchanges.keys():
                self.channel.exchange_declare(exchange=exName, **exParams)
                self.exchanges[exName] = exParams
        except pika.exceptions as e:
            raise error('Amqp.exDeclare', 'error', ' '.join([str(a) for a in e.args]))

    # qDeclare method - declares and binds a queue to an exchange
    def qDeclare(self, qName, exName, qParams, key):
        """declares and binds a queue to an exchange"""

        if self.conn is None or self.conn.is_closed: self.connect()
        self._Amqp__qDeclare(qName, exName, qParams, key)
        if not self.persistent: self.close()

    # qDeclare method - declares and binds a queue to an exchange (private) ; assumes conn
    def __qDeclare(self, qName, exName, qParams, key):
        """declares and binds a queue to an exchange"""

        try:
            # declare, bind, and save the queue, if not already declared, bound, and saved
            if qName not in self.queues.keys():
                self.channel.queue_declare(queue=qName, **qParams)
                self.channel.queue_bind(queue=qName, exchange=exName, routing_key=key)
                self.queues[qName] = dict(qParams.items() + [('exchange', exName),
                                                             ('routing_key', key)])
        except pika.exceptions as e:
            raise error('Amqp.qDeclare', 'error', ' '.join([str(a) for a in e.args]))

    # publish method - declares an exchange and publishes a message
    def publish(self, exchange, message='', key=''):
        """declares an exchange and publishes a message"""

        if self.conn is None or self.conn.is_closed: self.connect()

        # separate out exchange parameters
        exParams = dict(filter(lambda (k, v): k not in ['exchange'], exchange.items()))

        try:
            # declare the exchange and publish the message
            self._Amqp__exDeclare(exchange['exchange'], exParams)
            self.channel.basic_publish(exchange=exchange['exchange'], 
                                       routing_key=key, 
                                       body=message)
        except pika.exceptions as e:
            raise error('Amqp.publish', 'error', ' '.join([str(a) for a in e.args]))

        if not self.persistent: self.close()

    # consume method - declares an exchange and queue and returns a single message
    #                  NOTE: no_ack when True tells the broker to not expect a reply
    def consume(self, exchange, queue, key=None, no_ack=True):
        """declares an exchange and queue and returns a single message"""

        if self.conn is None or self.conn.is_closed: self.connect()

        # separate out exchange & queue parameters
        exParams = dict(filter(lambda (k, v): k not in ['exchange'], exchange.items()))
        qParams = dict(filter(lambda (k, v): k not in ['queue'], queue.items()))

        try:
            # declare the exchange, declare and bind the queue, and consume a single message
            self._Amqp__exDeclare(exchange['exchange'], exParams)
            self._Amqp__qDeclare(queue['queue'], exchange['exchange'], qParams, key)
            (frame, header, body) = self.channel.basic_get(queue=queue['queue'], 
                                                           no_ack=no_ack)
            # return the message body
            return body
        except pika.exceptions as e:
            raise error('Amqp.consume', 'error', ' '.join([str(a) for a in e.args]))

        if not self.persistent: self.close()

    # qStatus method - checks the status of a queue and returns a tuple (exists, msgCount)
    def qStatus(self, qName):
        """checks the status of a queue and returns message count"""

        result = (False, 0)

        if self.conn is None or self.conn.is_closed: self.connect()

        try:
            # declare queue passively to see if it exists and get message info
            status = self.channel.queue_declare(queue=qName, passive=True)
            result = (True, status.method.message_count)
        except pika.exceptions.ChannelClosed as e:
            # if error is other than 404 (queue doesn't exist), re-raise
            if len(e.args) and e.args[0] != 404: raise

        if not self.persistent: self.close()

        return result

    # qDelete method - unbinds, purges, and deletes one or all queues
    def qDelete(self, qName=None):
        """unbinds, purges, and deletes one or all queues"""

        if self.conn is None or self.conn.is_closed: self.connect()

        try:
            # step through queues and delete if the queue is named or no q name was passed
            for q in self.queues.keys():
                if qName == None or q == qName:
                    self.channel.queue_unbind(queue=q,
                                              exchange=self.queues[q]['exchange'],
                                              routing_key=self.queues[q]['routing_key'])
                    self.channel.queue_purge(queue=q, nowait=False)
                    self.channel.queue_delete(queue=q, if_unused=False, if_empty=False, 
                                              nowait=False)
                    del self.queues[q]
        except pika.exceptions as e:
            raise error('Amqp.qDelete', 'error', ' '.join([str(a) for a in e.args]))

        if not self.persistent: self.close()

    # exDelete method - deletes one or all exchanges
    def exDelete(self, exName=None):
        """deletes one or all exchanges"""

        if self.conn is None or self.conn.is_closed: self.connect()

        try:
            # step through exchanges and delete if the ex is named or no ex name was passed
            for ex in self.exchanges.keys():
                if exName == None or ex == exName:
                    self.channel.exchange_delete(exchange=ex, if_unused=False, nowait=False)
                    del self.exchanges[ex]
        except pika.exceptions as e:
            raise error('Amqp.exDelete', 'error', ' '.join([str(a) for a in e.args]))

        if not self.persistent: self.close()

    # close method - closes the amqp connection
    def close(self, delete=False):
        """closes the amqp connection"""

        if delete:
            self.qDelete()
            self.exDelete()

        try:
            if self.channel and self.channel.is_open: self.channel.close()
            if self.conn and self.conn.is_open: self.conn.close()
            self.channel = None
            self.conn = None
        except pika.exceptions as e:
            raise error('Amqp.close', 'error', ' '.join([str(a) for a in e.args]))

# amqpPublish - publishes an amqp message
def amqpPublish(amqp, ex, key='', message=''):
    """publishes an amqp message to exchange using amqp config and routing key"""

    try:

        # separate out amqp parameters from credentials and exchange name from parameters
        amqpParams = dict(filter(lambda (k, v): k not in ['username','password','nameRoot'], 
                                 amqp.items()))
        exParams = dict(filter(lambda (k, v): k not in ['exchange'], ex.items()))
        
        # attach nameRoot to exchange name and routing key
        exchange = amqp['nameRoot'] + ex['exchange']
        routingKey = amqp['nameRoot'] + key
        
        # connect to AMQP server with passed credentials and parameters
        c = pika.PlainCredentials(username, password)
        p = pika.ConnectionParameters(credentials=c, **amqpParams)
        amqpConn = pika.BlockingConnection(p)

        # declare exchange and publish message
        channel = amqpConn.channel()
        channel.exchange_declare(exchange=exchange, **exParams)
        channel.basic_publish(exchange, routingKey, message)

        # disconnect from AMQP server
        amqpConn.close()

    except pika.exceptions as e:
        raise error('amqpPublish', 'error', str(e.message))

##############################################################################################
# TESTING
##############################################################################################

if __name__ == '__main__':

    try:

        # amqp test
        amqp = {'username':'guest', 'password':'guest', 'host':'localhost', 'port':5672, 
                'virtual_host':'/'}
        ex = {'exchange':'testEx', 'exchange_type':'direct', 'passive':False, 'durable':False,
              'auto_delete':False, 'nowait':False}
        q = {'queue':'testQ', 'passive':False, 'durable':False, 'exclusive':False, 
             'auto_delete':False, 'nowait':False}
        a = Amqp(amqp)
        a.consume(exchange=ex, queue=q, key=q['queue'])  # creates exchange and queue
        a.publish(exchange=ex, message='test', key=q['queue'])
        status = a.qStatus(qName=q['queue'])
        message = Amqp(amqp).consume(exchange=ex, queue=q, key=q['queue'])
        print aColor('BLUE') + 'Amqp.publish/qStatus/consume...', aColor('OFF'), message, status
        print aColor('BLUE') + 'Amqp.qStatus...', aColor('OFF'), a.qStatus(qName='blahblah')

    except error as e: print e.error
