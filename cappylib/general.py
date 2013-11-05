##############################################################################################
# HEADER
#
# cappylib/general.py - defines useful functions for python scripts
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

import sys, re, ast

##############################################################################################
# GLOBAL VARS 
##############################################################################################

##############################################################################################
# MAIN CODE
##############################################################################################

# enumerations class
class enum:

    # days of the week
    class weekdays:
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

# error class - extends base exception class with a string
class error(BaseException):

    error = ''

    def __init__(self, location, eType, *messages):
        self.error = '{0}: {1} {2}'.format(location, eType, ' '.join(messages))

# aColor - returns ANSI codes for a given set of formats
def aColor(codeString):
    """returns ANSI encoded string for a given set of ; separated format codes"""

    # define ANSI codes
    ansiCodeMask = '\033[{0}m'
    ansiColorCodes = {
        'OFF': 0,
        'BOLD': 1,
        'ITALIC': 3,
        'UNDERLINE': 4,
        'BLINK': 5,
        'BLACK': 30,
        'RED': 31,
        'GREEN': 32,
        'YELLOW': 33,
        'BLUE': 34,
        'MAGENTA': 35,
        'CYAN': 36,
        'WHITE': 37,
        'B': 10, # background code offset
        'I': 60  # intensity code offset
        }
    
    # create ANSI encoded string from format codeString
    offset = 0
    codes = []
    for c in codeString.split(';'):
        if c in ('B','I'):
            offset += ansiColorCodes[c]
        else:
            codes.append(offset + ansiColorCodes[c])
            offset = 0

    # return ANSI string
    return ''.join([ansiCodeMask.format(c) for c in codes])

# argParse - map CLI args to a keyMap and optionally parse for a key/value
def argParse(keyMap=None, keySearch=None, valueSearch=None):
    """map CLI args to a keyMap an optionally parse for a key/value"""

    args = sys.argv[1:] if len(sys.argv) > 1 else []
    keyMap = keyMap if keyMap else []

    # step through a copy of args and extract any --<var>='<value>' elements
    keyValuePairs = {}
    for arg in list(args):
        r = re.search('--(.+?)=[\'"]{0,1}(.*)[\'"]{0,1}', arg, (re.MULTILINE | re.DOTALL))
        if r:
            args.remove(arg)
            keyValuePairs[r.group(1)] = r.group(2)

    # if --ast_eval=True was passed, call ast eval on each value in keyValuePairs
    if 'ast_eval' in keyValuePairs and keyValuePairs['ast_eval']:
        keyValuePairs = dict([(key, ast.literal_eval(keyValuePairs[key]))
                              for key in keyValuePairs.keys()])

    # map keyMap to args, adding filename
    mappedArgs = dict(zip(['__file'] + keyMap, [sys.argv[0]] + args))

    # merge key mapped dict with key value pairs dict
    mappedArgs = dict(mappedArgs.items() + keyValuePairs.items())
    
    # ensure all kepMap keys have a value
    for key in keyMap:
        if key not in mappedArgs:
            mappedArgs[key] = None

    # if valueSearch, return true if value in args|mappedArgs, else false
    if valueSearch:
        found = valueSearch in args or valueSearch in mappedArgs.values()
        return True if found else False

    # if keySearch, return value if key is defined, else false
    if keySearch:
        return mappedArgs[keySearch] if keySearch in mappedArgs else False

    # if a keyMap or keyValuePairs were passed, return mappedArgs, else args
    return mappedArgs if (keyMap or keyValuePairs) and mappedArgs else args

##############################################################################################
# TESTING
##############################################################################################

def main():

    # argParse test
    print 'argParse()... ', argParse()
    print 'argParse(keyMap=[one, two, three])... ', argParse(keyMap=['one','two','three'])
    print 'argParse(keyMap=[one, two, three],keySearch=one)... ', \
        argParse(keyMap=["one","two","three"], keySearch='one')
    print 'argParse(valueSearch="2")... ', argParse(valueSearch='2')
        
    # error test
    try:
        raise error('test', 'error', 'fi', 'fo', 'fum')
    except error as e: print 'error... ', e.error

    # color test
    print 'aColor... ' + aColor('BOLD;B;I;GREEN') + '1' + aColor('OFF')

if __name__ == '__main__':

    try:
        main()
    except error as e: print e.error
