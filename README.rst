============
hashids-cffi
============
A python port of the JavaScript *hashids* implementation that provides bindings to the `hashids.c <https://github.com/tzvetkoff/hashids.c>` C implementation.
It generates YouTube-like hashes from one or many numbers.
Use hashids when you do not want to expose your database ids to the user. Website: http://www.hashids.org/

.. image:: https://travis-ci.org/thedrow/hashids-cffi.svg?branch=master
    :target: https://travis-ci.org/thedrow/hashids-cffi

Installation
============

Install the module from PyPI, e. g. with pip:

.. code:: bash

  pip install hashids-cffi

Limitations and Known Issues
============================
* The C library does not support unicode and therefor segfaults when passed a unicode string.
  Only ascii encoded alphabets, salts and hashes are currently allowed.
* The C library only supports unsigned long long integers (The maximum value is 2 :sup:`64`-1). If you need a wider range use the pure Python implementation
* The C library does not check for overflows so on rare occasions you might be provided with incorrect results.
* The C library is not thread safe and maintains global state for error reporting.