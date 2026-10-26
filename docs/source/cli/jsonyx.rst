jsonyx
======

.. program:: jsonyx

A command line utility to manipulate JSON files.

Usage
-----

.. code-block:: none

    jsonyx [-h] [-v]

Options
-------

-h, --help      Show the help message and exit.
-v, --version   Show the version number and exit.

Example
-------

.. code-block:: console

    $ jsonyx --version
    jsonyx 2.5.0 (C extension)

.. warning:: If the version number is followed by ``(Python)``, the performance
    will be up to 90.64x slower for encoding and up to 82.59x slower decoding,
    so make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.
