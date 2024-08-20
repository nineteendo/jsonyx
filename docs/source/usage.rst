Usage
=====

.. _installation:

Installation
------------

To use :mod:`jsonyx`, first install it using pip:

.. code-block:: console

    (.venv) $ pip install jsonyx

Quick start
-----------

Encoding basic Python object hierarchies::

    >>> import jsonyx as json
    >>> json.dumps({"foo": ["bar", None, 1.0, 2]})
    '{"foo": ["bar", null, 1.0, 2]}\n'
    >>> json.dump('"foo\bar')
    "\"foo\bar"
    >>> json.dump("\\")
    "\\"
    >>> json.dump("\u1234", ensure_ascii=True)
    "\u1234"
    >>> json.dump({"c": 3, "b": 2, "a": 1}, sort_keys=True)
    {"a": 1, "b": 2, "c": 3}
    >>> from io import StringIO
    >>> io = StringIO()
    >>> json.dump(["streaming API"], io)
    >>> io.getvalue()
    '["streaming API"]\n'
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     filename = Path(tmpdir) / "file.json"
    ...     json.write(["filesystem API"], filename)
    ...     filename.read_text("utf_8")
    ...
    '["filesystem API"]\n'

Compact encoding::

    >>> import jsonyx as json
    >>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", item_separator=",", key_separator=":")
    '{"a":1,"b":2,"c":3}'

Pretty printing::

    >>> import jsonyx as json
    >>> json.dump({"c": 3, "b": 2, "a": 1}, indent=4, sort_keys=True)
    {
        "a": 1,
        "b": 2,
        "c": 3
    }

Decoding JSON::

    >>> import jsonyx as json
    >>> json.loads('{"foo": ["bar", null, 1.0, 2]}')
    {'foo': ['bar', None, 1.0, 2]}
    >>> json.loads(r'"\"foo\bar"')
    '"foo\x08ar'
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    ['streaming API']
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     filename = Path(tmpdir) / "file.json"
    ...     _ = filename.write_text('["filesystem API"]', "utf_8")
    ...     json.Decoder().read(filename)
    ...
    ['filesystem API']

Allow NaN and infinity::

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> json.loads("NaN", allow=jsonyx.allow.NAN_AND_INFINITY)
    nan
    >>> json.dump(float("nan"), allow=jsonyx.allow.NAN_AND_INFINITY)
    NaN

Using :class:`decimal.Decimal` instead of :class:`float`::

    >>> import jsonyx as json
    >>> from decimal import Decimal
    >>> json.loads("1.1", use_decimal=True)
    Decimal('1.1')
    >>> json.dump(Decimal("1.1"))
    1.1

Make a patch from two Python objects::

    >>> import jsonyx as json
    >>> json.make_patch([1, 2, 3, 5], [1, 3, 4, 5])
    [{'op': 'del', 'path': '$[1]'}, {'op': 'insert', 'path': '$[2]', 'value': 4}]

Applying a patch::

    >>> import jsonyx as json
    >>> json.apply_patch([1, 2, 3], {"op": "clear"})
    []

Using :mod:`jsonyx` from the shell to validate and pretty-print:

.. code-block:: shell-session

    $ echo '{"json": "obj"}' | python -m jsonyx format --indent 4
    {
        "json": "obj"
    }
    $ echo '{1.2: 3.4}' | python -m jsonyx format
      File "<stdin>", line 1, column 2
        {1.2: 3.4}
         ^
    jsonyx.JSONSyntaxError: Expecting string

See :ref:`command_line_options` for more details.

.. _command_line_options:

Command line options
--------------------

.. option:: command

    - diff: make a JSON patch from two JSON files.
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

    The path to the input JSON file, or "-" for standard input. If not
    specified, read from :data:`sys.stdin`.

.. option:: output_filename

    The path to the output JSON file, or "-" for standard output. If not
    specified, write to :data:`sys.stdout`.

    .. versionadded:: 1.2

.. option:: -h, --help

    Show the help message and exit.

.. option:: -a, --ensure-ascii

    Escape non-ASCII characters.

.. option:: -c, --compact

    Avoid unnecessary whitespace after "," and ":".

.. option:: -C, --no-commas

    Separate items by whitespace instead of commas.

.. option:: -d, --use-decimal

    Use decimal instead of float.

.. option:: -i SPACES, --indent SPACES

    Indent using the specified number of spaces.

.. option:: -s, --sort-keys

    Sort the keys of objects.

.. option:: -S, --nonstrict

    Allow all JSON deviations.

.. option:: -t, --trailing-comma

    Add a trailing comma if indented.

.. option:: -T, --indent-tab

    Indent using tabs.
