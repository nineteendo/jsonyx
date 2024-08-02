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
    >>> import jsonyx.allow
    >>> json.dumps({'foo': ['bar', None, 1.0, 2]})
    '{"foo": ["bar", null, 1.0, 2]}\n'
    >>> json.dump("\"foo\bar")
    "\"foo\bar"
    >>> json.dump('\\')
    "\\"
    >>> json.dump(float("nan"), allow=jsonyx.allow.NAN_AND_INFINITY)
    NaN
    >>> json.dump('\u1234', ensure_ascii=True)
    "\u1234"
    >>> json.dump({"c": 3, "b": 2, "a": 1}, sort_keys=True)
    {"a": 1, "b": 2, "c": 3}
    >>> from io import StringIO
    >>> io = StringIO()
    >>> json.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]\n'

Compact encoding::

    >>> import jsonyx as json
    >>> json.dumps({'1': 2, '3': 4}, end="", item_separator=",", key_separator=":")
    '{"1":2,"3":4}'

Pretty printing::

    >>> import jsonyx as json
    >>> json.dump({'3': 4, '1': 2}, indent=4, sort_keys=True)
    {
        "1": 2,
        "3": 4
    }

Decoding JSON::

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> json.loads('{"foo": ["bar", null, 1.0, 2]}')
    {'foo': ['bar', None, 1.0, 2]}
    >>> json.loads('"\\"foo\\bar"')
    '"foo\x08ar'
    >>> json.loads('NaN', allow=jsonyx.allow.NAN_AND_INFINITY)
    nan
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    ['streaming API']

Using Decimal instead of float::

    >>> import jsonyx as json
    >>> from decimal import Decimal
    >>> json.loads('1.1', use_decimal=True)
    Decimal('1.1')
    >>> json.dump(Decimal('1.1'))
    '1.1'


Using :mod:`jsonyx.tool` from the shell to validate and pretty-print:

.. code-block:: shell-session

    $ echo '{"json":"obj"}' | python -m jsonyx.tool --indent 4
    {
        "json": "obj"
    }
    $ echo '{1.2: 3.4}' | python -m jsonyx.tool
      File "<stdin>", line 1, column 2
        {1.2: 3.4}
         ^
    jsonyx._decoder.JSONSyntaxError: Expecting string

Constants
---------

.. autoattribute:: jsonyx.allow.NOTHING
.. autoattribute:: jsonyx.allow.COMMENTS
.. autoattribute:: jsonyx.allow.DUPLICATE_KEYS
.. autoattribute:: jsonyx.allow.MISSING_COMMAS
.. autoattribute:: jsonyx.allow.NAN_AND_INFINITY
.. autoattribute:: jsonyx.allow.TRAILING_COMMA
.. autoattribute:: jsonyx.allow.SURROGATES
.. autoattribute:: jsonyx.allow.EVERYTHING

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

Exceptions
----------

.. autoexception:: jsonyx.JSONSyntaxError
    :members: