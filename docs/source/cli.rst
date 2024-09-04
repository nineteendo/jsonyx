Command Line Interface
======================

.. option:: command

    - diff: compare two JSON files and generate a diff in JSON patch format.
    - format: re-format a JSON file.
    - patch: apply a JSON patch to the input file.

    .. versionadded:: 2.0

.. option:: old_input_filename

    The path to the old input JSON file.

    .. versionadded:: 2.0

.. option:: patch_filename

    The path to the JSON patch file.

    .. versionadded:: 2.0

.. option:: input_filename

    The path to the input JSON file, or ``"-"`` for standard input. If not
    specified, read from :data:`sys.stdin`.

    .. versionchanged:: 1.2
        Renamed from :option:`!filename`

.. option:: output_filename

    The path to the output JSON file. If not specified, write to
    :data:`sys.stdout`.

    .. versionadded:: 1.2

.. option:: -h, --help

    Show the help message and exit.

.. option:: -a, --ensure-ascii

    Escape non-ASCII characters.

    .. versionadded:: 1.2
        :option:`!-a`

.. option:: -c, --compact

    Avoid unnecessary whitespace after ``","`` and ``":"``.

    .. versionadded:: 1.2
        :option:`!-c`

.. option:: -d, --use-decimal

    Use :class:`decimal.Decimal` instead of :class:`float`.

    .. versionadded:: 1.2
        :option:`!-d`

.. option:: -i SPACES, --indent SPACES

    Indent using the specified number of spaces.

    .. versionadded:: 1.2
        :option:`!-i`

.. option:: -l, --indent-leaves

    Indent leaf objects and arrays.

    .. versionadded:: 2.0

.. option:: -s, --sort-keys

    Sort the keys of objects.

    .. versionadded:: 1.2
        :option:`!-s`

.. option:: -S, --nonstrict

    Allow all JSON deviations provided by :mod:`jsonyx`.

    .. versionadded:: 1.2
        :option:`!-S`

.. option:: -t, --trailing-comma

    Add a trailing comma when indented.

    .. versionadded:: 1.2
        :option:`!-t`

.. option:: -T, --indent-tab

    Indent using tabs.

    .. versionadded:: 1.2
        :option:`!-T`

.. option:: -u, --unquoted-keys

    Don't quote keys which are identifiers.

    .. versionadded:: 2.0
