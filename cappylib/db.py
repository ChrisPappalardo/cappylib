##############################################################################################
# HEADER
#
# cappylib/db.py - defines functions for interfacing python scripts with databases
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

##############################################################################################
# IMPORTS 
##############################################################################################

import mysql.connector
from cappylib.general import *

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# queryMysql - executes mysql query using a query template and inputs dict, returns list;
#              if '__debug' == True in inputs, print debug information to stdout
def queryMysql(db, query, **inputs):
    """
    queries db using a key-based query template and inputs by key, returns list of dicts;
    if '__debug' key is set to True in inputs, query debug information will print to stdout; 
    '__debug' is a reserved key and cannot be used in queries
    """

    result = []
    debug = [query, str(inputs)] if '__debug' in inputs and inputs['__debug'] else None
    
    try:

        # validate db type
        cType = mysql.connector.connection.MySQLConnection
        if not (type(db) == dict or type(db) == cType): 
            raise error('queryMysql', 'error', 'db arg is an invalid type')

        # convert input parameters passed as a list into individual keys and anchors
        for k in inputs.keys():
            if type(inputs[k]) == list:
                n = len(inputs[k])
                # if list is empty, replace with an empty string and continue
                if not n:
                    inputs[k] = ''
                    continue
                # otherwise, create new keys using __{oldKey}{elementNo} format
                newKeys = ['__{0}{1}'.format(k, i) for i in range(0, n)]
                newDict = dict([(newKeys[i], inputs[k][i]) for i in range(0, n)])
                # delete list from inputs and replace with generated key/value pairs
                del inputs[k]
                inputs = dict(inputs.items() + newDict.items())
                # replace the old key anchor with new key anchors
                query = query.replace('%({0})s'.format(k), 
                                      '%({0})s'.format(')s, %('.join(newKeys)))

        # connect to database; if db is already a mysql connection type, use that instead
        c = mysql.connector.connect(**db) if not type(db) == cType else db
        cursor = c.cursor()

        # execute query and build result
        cursor.execute(query, inputs)
        if debug: debug.append(cursor.statement)
        for row in cursor: result.append(dict(zip(cursor.column_names, row)))

        # commit changes to db and close the db cursor/connection (but only if we opened it)
        c.commit()  # this is required to write to MySQL InnoDB tables
        cursor.close()
        if type(db) == dict: c.close()

        # if debug, print debug data and the last MySQL statement executed
        if debug: print str(debug)

        return result

    # catch KeyErrors when input keys dont match template and mysql errors
    except (KeyError, IndexError) as e:
        raise error('queryMysql', 'error', 'inputs do not match template: {0}'.format(str(e)))
    except mysql.connector.Error as e:
        raise error('queryMysql', 'error', str(e))

##############################################################################################
# TESTING #
##############################################################################################

def main():

    # queryMysql test
    db = {
        'user': 'devtest',
        'password': 'devtest',
        'host': 'localhost',
        'database': 'devtest'
        }
    queryMysql(db, 'DROP TABLE IF EXISTS devtest')
    queryMysql(db, ('CREATE TABLE IF NOT EXISTS devtest (' + 
                    'id INT(9) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
                    'a INT(6) UNSIGNED ZEROFILL, b VARCHAR(60), ' + 
                    'c TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)'))
    for i in range(0, 50): 
        queryMysql(db, 'INSERT INTO devtest(a, b) VALUES(%(a)s, %(b)s)', a=(i * i), 
                   b='index was {0}'.format(i))
    print aColor('BLUE') + 'queryMysql...', aColor('OFF'), \
        queryMysql(db, 'SELECT * FROM devtest WHERE id=%(id)s', id=20)

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
