jsonyx diff
===========

.. program:: jsonyx diff

Compare two JSON files and generate a diff in JSON patch format.

Usage
-----

.. code-block:: none

    jsonyx diff [-h] [-a] [-c] [-C] [-d] [-i SPACES] [-l] [-L LEVEL] [-s] [-S]
                [-t] [-T] [-q] old_input_filename [input_filename]
                [output_filename]

Positional arguments
--------------------

.. option:: old_input_filename

    The path to the old input JSON file.

.. option:: input_filename

    The path to the input JSON file, or ``"-"`` for standard input. If not
    specified, read from :data:`sys.stdin`.

.. option:: output_filename

    The path to the output JSON file. If not specified, write to
    :data:`sys.stdout`.

Options
-------

.. option:: -h, --help

    Show the help message and exit.

.. option:: -a, --ensure-ascii

    Escape non-ASCII characters.

.. option:: -c, --compact

    Avoid unnecessary whitespace after ``","`` and ``":"``.

.. option:: -C, --no-commas

    Don't separate items by commas when indented.

.. option:: -d, --use-decimal

    Use :class:`decimal.Decimal` instead of :class:`float`.

.. option:: -i, --indent SPACES

    Indent using the specified number of spaces.

.. option:: -l, --no-indent-leaves

    Don't indent leaf objects and arrays.

.. option:: -L, --max-indent-level

    The level up to which to indent.

.. option:: -q, --unquoted-keys

    Don't quote keys which are :ref:`identifiers <identifiers>`.

.. option:: -s, --sort-keys

    Sort the keys of objects.

.. option:: -S, --nonstrict

    Allow all JSON deviations provided by :mod:`jsonyx`.

.. option:: -t, --trailing-comma

    Add a trailing comma when indented.

.. option:: -T, --indent-tab

    Indent using tabs.
