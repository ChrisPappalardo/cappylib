cappylib
========

Chris Pappalardo's python library - defines useful classes and functions for Python scripts 
and implements other useful Python modules with simple interfaces.

This package includes:

  * MySQL database interface using the MySQL Connector for Python
  * AMQP interface using the Pika BlockingConnection library
  * Cron-style Python scheduler
  * Levels-based logger to queue, file, and/or stdout
  * Date and time series generator
  * Command-line argument parser
  * Cubic-spline interpolator

MySQL and MySQL Connector/Python are Copyright (C) Oracle and/or its affiliates and are 
licensed under the GNU GPLv2 (with FOSS License Exception).  Visit 
http://dev.mysql.com/doc/connector-python/en/index.html for additional information.

Pika is Copyright (C) Gavin M. Roy and is licensed under the MPL v1.1 and GPL v2.0 or newer.  
Visit https://pika.readthedocs.org for additional information.

## Installation

This package requires the following:

  * Python 2.x
  * mysql-connector-python v1.0.12 or later
  * pika v0.9.14p0 or later

Begin by ensuring you have the appropriate version of python installed and install the 
third-party modules, as follows:

1.  Follow the installation instructions for mysql-connector-python for your particular 
    platform as outlined at 
    http://dev.mysql.com/doc/connector-python/en/connector-python-installation.html.

2.  Follow the installation instructions for pika as outlined in the documentation linked 
    in the README.md file at https://github.com/pika/pika/.

3.  Install cappylib, which is available from PyPl, using easy_install (from a *nix shell):

    $ easy_install cappylib

    or pip:

    $ pip install cappylib

    You can also clone the repo from github:

    $ git clone https://github.com/ChrisPappalardo/cappylib.git

    and from the source dir run the following as root:

    $ python setup.py install

## Documentation

I included docstrings with all cappylib classes, methods, and functions.  I also included 
unit tests for all classes, methods, and functions as main() in each respective module.

To review docstring-based documentation, use Python in calculator mode, and execute the following:

```python
import cappylib
help(cappylib)
```

for a list of modules contained in cappylib.  Execute the following:

```python
import cappylib.<module>
help(cappylib.<module>)
```

for docstrings associated with \<module\>.

## Usage and Examples

To import all cappylib modules directly into your scripts symbol table, use:

```python
from cappylib import *
```

(You can replace * with \<module\>)

Or you can import a specific module into the cappylib namespace using:

```python
import cappylib.<module>
```

Available modules are as follows:

  * amqp
  * date_time
  * db
  * financial
  * general
  * log
  * prontab

To see examples of class instantiation and class method and function usage, simply review the 
unit testing code at the end of each module .py file under the "TESTING" header.  
Module files can be found in the cappylib dir in your default package installation directory 
(/usr/local/lib/python2.7/dist-packages/cappylib on my system).  Unit testing code is 
contained in the function main() in each module.

You can run the unit tests yourself using:

    $ python -m cappylib.<module>

Or all unit tests using:

   $ python -m cappylib
