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
    http://dev.mysql.com/doc/connector-python/en/connector-python-installation.html.  For 
    example, on my Debian Linux server, I opted to downloaded the platform-independent source 
    code and ran "python setup.py install" as root from the extracted tarball.  This required 
    that I had Python setuptools installed beforehand ("apt-get install python-setuptools" as 
    root on my Debian system).

2.  Follow the installation instructions for pika as outlined in the documentation linked 
    in the README.md file at https://github.com/pika/pika/.  As an alternative to using pip 
    or easy_install, you can clone the repo from github and then run 
    "python setup.py install" as root.

3.  Install cappylib, which is available from PyPl, using easy_install:

      $ easy_install cappylib

    or pip:

      $ pip install cappylib

    You can also clone the repo from github:

      $ git clone https://github.com/ChrisPappalardo/cappylib.git

    and from the source dir run the following as root:

      $ python setup.py install

## Documentation

I included docstrings with all cappylib classes, methods, and functions.  I also included 
unit tests for all classes, methods, and functions in each respective module.

To review docstring-based documentation, use Python in calculator mode, as follows:

  $ python
  Python 2.7.3 (default, Jan  2 2013, 13:56:14)
  [GCC 4.7.2] on linux2
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import cappylib
  >>> help(cappylib)

## Usage and Examples

To use cappylib, simply import the library into your python scripts:

```python
import cappylib
```

Or you can import a specific module in the library:

```python
import cappylib.amqp
```

The library modules are as follows:

  * amqp.py
  * date_time.py
  * db.py
  * general.py
  * log.py
  * prontab.py

To see examples of class instantiation and class method and function usage, simply review the 
unit testing code at the end of each module .py file under the "TESTING" header.  
Module files can be found in your default package installation directory 
(/usr/local/lib/python2.7/dist-packages on my system).  

You can run the unit tests yourself using:

    $ python -m cappylib.<module>
