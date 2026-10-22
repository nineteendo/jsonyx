jsonyx patch
============

.. program:: jsonyx patch

Apply a JSON patch to the input file.

Usage
-----

.. code-block:: none

    jsonyx patch [-h] [-a] [-c] [-C] [-i SPACES] [-l] [-L LEVEL] [-s] [-S] [-t]
                 [-T] [-q] patch_filename [input_filename] [output_filename]

Positional arguments
--------------------

.. option:: patch_filename

    The path to the :doc:`JSON patch </json-patch-spec>` file.

.. option:: input_filename

    The path to the input JSON file, or ``"-"`` for standard input. If not
    specified, read from :data:`sys.stdin`.

.. option:: output_filename

    The path to the output JSON file. If not specified, write to
    :data:`sys.stdout`.

Options
-------

.. versionchanged:: 2.4 Removed ``--use-decimal`` (alias ``-d``)

-h, --help              Show the help message and exit.
-a, --ensure-ascii      Escape non-ASCII characters.
-c, --compact           Avoid unnecessary whitespace after ``","`` and ``":"``.
-C, --no-commas         Don't separate items by commas when indented.
-i, --indent SPACES     Indent using the specified number of spaces.
-l, --no-indent-leaves  Don't indent leaf objects and arrays.
-L, --max-indent-level  The level up to which to indent.
-q, --unquoted-keys     Don't quote keys which are
                        :ref:`identifiers <identifiers>`.
-s, --sort-keys         Sort the keys of objects.
-S, --nonstrict         Allow all JSON deviations provided by :mod:`jsonyx`.
-t, --trailing-comma    Add a trailing comma when indented.
-T, --indent-tab        Indent using tabs.
