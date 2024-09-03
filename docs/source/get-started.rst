Getting Started
===============

.. _installation:

Installation
------------

To use :mod:`jsonyx`, first install it using pip, `conda <https://conda.org>`_
or `mamba <https://mamba.readthedocs.io>`_:

.. code-block:: console

    (.venv) $ pip install -U jsonyx

.. code-block:: console

    $ conda install conda-forge::jsonyx

.. code-block:: console

    $ mamba install conda-forge::jsonyx

Quick start
-----------

Encoding basic Python object hierarchies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'
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

Compact encoding
^^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", separators=(",", ":"))
    '{"a":1,"b":2,"c":3}'

Pretty printing
^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.dump({"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}, indent=4)
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

.. tip::
    Use ``indent_leaves=True`` to indent everything and ``sort_keys=True`` to
    sort the keys of objects.

.. warning::
    To pretty-print unpaired surrogates, you need to use
    :data:`jsonyx.allow.SURROGATES` and ``ensure_ascii=True``.

Decoding JSON
^^^^^^^^^^^^^

::

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

Using :class:`decimal.Decimal` instead of :class:`float`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.loads("[1.0000000000000001, 1e400]", use_decimal=True)
    [Decimal('1.0000000000000001'), Decimal('1E+400')]

.. note::
    :class:`decimal.Decimal` can be natively serialized.

Making a patch from two Python objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.make_patch([1, 2, 3], [1, 3])
    [{'op': 'del', 'path': '$[1]'}]

Applying a patch
^^^^^^^^^^^^^^^^

::

    >>> import jsonyx as json
    >>> json.apply_patch([1, 2, 3], {'op': 'del', 'path': '$[1]'})
    [1, 3]

.. tip::
    Using queries instead of indices is more robust.

Using the ``jsonyx`` command line utility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell-session

    $ echo '{"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}' | jsonyx format --indent 4
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }
    $ echo '{1.2: 3.4}' | jsonyx format
      File "<stdin>", line 1, column 2
        {1.2: 3.4}
         ^
    jsonyx.JSONSyntaxError: Expecting string

See :doc:`api/index` and :doc:`cli` for more details.
