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

    >>> import jsonyx
    >>> import jsonyx.allow
    >>> jsonyx.dumps({'foo': ['bar', None, 1.0, 2]})
    '{"foo": ["bar", null, 1.0, 2]}\n'
    >>> jsonyx.dump("\"foo\bar")
    "\"foo\bar"
    >>> jsonyx.dump('\\')
    "\\"
    >>> jsonyx.dump(float("nan"), allow=jsonyx.allow.NAN_AND_INFINITY)
    NaN
    >>> jsonyx.dump('\u1234', ensure_ascii=True)
    "\u1234"
    >>> jsonyx.dump({"c": 3, "b": 2, "a": 1}, sort_keys=True)
    {"a": 1, "b": 2, "c": 3}
    >>> from io import StringIO
    >>> io = StringIO()
    >>> jsonyx.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]\n'

Compact encoding::

    >>> import jsonyx
    >>> jsonyx.dumps({'1': 2, '3': 4}, end="", item_separator=",", key_separator=":")
    '{"1":2,"3":4}'

Pretty printing::

    >>> import jsonyx
    >>> jsonyx.dump({'3': 4, '1': 2}, indent=4, sort_keys=True)
    {
        "1": 2,
        "3": 4
    }

Decoding JSON::

    >>> import jsonyx
    >>> import jsonyx.allow
    >>> jsonyx.loads('{"foo": ["bar", null, 1.0, 2]}')
    {'foo': ['bar', None, 1.0, 2]}
    >>> jsonyx.loads('"\\"foo\\bar"')
    '"foo\x08ar'
    >>> jsonyx.loads('NaN', allow=jsonyx.allow.NAN_AND_INFINITY)
    nan
    >>> jsonyx.loads('1.1', use_decimal=True)
    Decimal('1.1')
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> jsonyx.load(io)
    ['streaming API']

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

    .. autofunction:: load
    .. autofunction:: loads
    .. autofunction:: read
.. autoclass:: jsonyx.DuplicateKey
.. autoclass:: jsonyx.Encoder

    .. autofunction:: dump
    .. autofunction:: dumps
    .. autofunction:: write

Exceptions
----------

.. autoexception:: jsonyx.JSONSyntaxError