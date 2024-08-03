Usage
=====

.. _installation:

Installation
------------

To use jsonyx, first install it using pip:

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
    >>> json.loads('"\\"foo\\bar"')
    '"foo\x08ar'
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    ['streaming API']

Using Decimal instead of float::

    >>> import jsonyx as json
    >>> from decimal import Decimal
    >>> json.loads("1.1", use_decimal=True)
    Decimal('1.1')
    >>> json.dump(Decimal("1.1"))
    1.1

Using :mod:`jsonyx` from the shell to validate and pretty-print:

.. code-block:: shell-session

    $ echo '{"json": "obj"}' | python -m jsonyx --indent 4
    {
        "json": "obj"
    }
    $ echo '{1.2: 3.4}' | python -m jsonyx
      File "<stdin>", line 1, column 2
        {1.2: 3.4}
         ^
    jsonyx._decoder.JSONSyntaxError: Expecting string

See :ref:`command_line_options` for more details.

Constants
---------

.. autoattribute:: jsonyx.allow.NOTHING

    Raises an error for all JSON deviations.

.. autoattribute:: jsonyx.allow.COMMENTS

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads("0 // line comment", allow=jsonyx.allow.COMMENTS)
        0

.. autoattribute:: jsonyx.allow.DUPLICATE_KEYS

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads('{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS)
        {'key': 'value 1', 'key': 'value 2'}

    .. note::
        To get access to the second value of "key", you need to iterate over
        the items of the dictionary.

.. autoattribute:: jsonyx.allow.MISSING_COMMAS

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads("[1 2 3]", allow=jsonyx.allow.MISSING_COMMAS)
        [1, 2, 3]

    .. note::
        Whitespace or a comment must be present if the comma is missing.

.. autoattribute:: jsonyx.allow.NAN_AND_INFINITY

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads("NaN", allow=jsonyx.allow.NAN_AND_INFINITY)
        nan
        >>> json.dump(float("nan"), allow=jsonyx.allow.NAN_AND_INFINITY)
        NaN

    .. note::
        ``Decimal("sNan")`` can't be (de)serialised this way.

.. autoattribute:: jsonyx.allow.TRAILING_COMMA

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads('[0,]', allow=jsonyx.allow.TRAILING_COMMA)
        [0]

.. autoattribute:: jsonyx.allow.SURROGATES

    Example::

        >>> import jsonyx as json
        >>> import jsonyx.allow
        >>> json.loads('"\ud800"', allow=jsonyx.allow.SURROGATES)
        '\ud800'
        >>> json.dump("\ud800", allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
        "\ud800"

    .. note::
        If you're not using ``read()`` or ``write()``, you still need to set
        the unicode error handler to "surrogatepass".

.. autoattribute:: jsonyx.allow.EVERYTHING

    Equivalent to ``COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS |
    NAN_AND_INFINITY | SURROGATES | TRAILING_COMMA``.

Functions
---------

.. autofunction:: jsonyx.detect_encoding
.. autofunction:: jsonyx.dump
.. autofunction:: jsonyx.dumps
.. autofunction:: jsonyx.format_syntax_error
.. autofunction:: jsonyx.load
.. autofunction:: jsonyx.loads
.. autofunction:: jsonyx.read
.. autofunction:: jsonyx.write
.. autofunction:: jsonyx.tool.register
.. autofunction:: jsonyx.tool.run

Classes
-------

.. autoclass:: jsonyx.Decoder
    :members:

.. autoclass:: jsonyx.DuplicateKey

    Example::

        >>> import jsonyx as json
        >>> {"key": "value 1", json.DuplicateKey("key"): "value 2"}
        {'key': 'value 1', 'key': 'value 2'}

.. autoclass:: jsonyx.Encoder
    :members:

.. autoclass:: jsonyx.tool.JSONNamespace
    :members:

Exceptions
----------

.. autoexception:: jsonyx.JSONSyntaxError

.. _command_line_options:

Command line options
--------------------

.. option:: input_filename

    The path to the input JSON file, or "-" for standard input. If not
    specified, read from :data:`sys.stdin`.

    .. code-block:: shell-session

        $ python -m jsonyx mp_films.json --indent 4
        [
            {
                "title": "And Now for Something Completely Different",
                "year": 1971
            },
            {
                "title": "Monty Python and the Holy Grail",
                "year": 1975
            }
        ]

.. option:: output_filename

    The path to the output JSON file. If not specified, write to
    :data:`sys.stdout`.

    .. versionadded:: 1.2

.. option:: -h, --help

    Show the help message and exit.

.. option:: -a, --ensure-ascii

    Escape non-ascii characters.

.. option:: -c, --compact

    Don't add unnecessary whitespace after "," and ":".

.. option:: -C, --no-commas

    Separate items by whitespace instead of comma's.

.. option:: -d, --use-decimal

    Use decimal instead of float.

.. option:: -i SPACES, --indent SPACES

    Indent using spaces.

.. option:: -s, --sort-keys

    Sort the keys of objects.

.. option:: -S, --nonstrict

    Allow all JSON deviations.

.. option:: -t, --trailing-comma

    Add a trailing comma if indented.

.. option:: -T, --indent-tab

    Indent using tabs.
