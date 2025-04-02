jsonyx format
=============

.. program:: jsonyx format

Re-format or validate a JSON file.

Usage
-----

.. code-block:: none

    jsonyx format [-h] [-a] [-c] [-C] [-d] [-i SPACES] [-l] [-L LEVEL] [-r]
                  [-s] [-S] [-t] [-T] [-q] [input_filename] [output_filename]

Positional arguments
--------------------

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

.. option:: -r, --rgb

    .. versionadded:: 2.3

    Use colored output, see :envvar:`JSONYX_COLORS`.

.. option:: -s, --sort-keys

    Sort the keys of objects.

.. option:: -S, --nonstrict

    Allow all JSON deviations provided by :mod:`jsonyx`.

.. option:: -t, --trailing-comma

    Add a trailing comma when indented.

.. option:: -T, --indent-tab

    Indent using tabs.

Environment variables
---------------------

.. envvar:: JSONYX_COLORS

    .. versionadded:: 2.3

    A colon-delimited list of partial terminal escape sequences like
    ``"1;31"``, in this order:

    - color for ``null``
    - color for ``false``
    - color for ``true``
    - color for numbers
    - color for strings
    - color for arrays
    - color for objects
    - color for object keys

    Default ``"0;90:0;39:0;39:0;39:0;32:1;39:1;39:1;34"``.

Example
-------

.. code-block:: shell-session

    $ echo '{"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}' | jsonyx format \
    --indent 4 \
    --no-indent-leaves
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }
    $ echo "{1.2: 3.4}" | jsonyx format
      File "<stdin>", line 1, column 2
        {1.2: 3.4}
         ^
    jsonyx.JSONSyntaxError: Expecting string
