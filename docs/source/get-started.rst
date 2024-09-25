Getting Started
===============

.. _installation:

Installation
------------

To use :mod:`jsonyx`, first install it using pip,
`pipx <https://pipx.pypa.io>`_ or `conda <https://docs.conda.io>`_:

.. tab:: pip

    .. tab:: PyPI

        .. only:: latex

            .. rubric:: pip (PyPI)

        .. code-block:: console

            (.venv) $ pip install -U jsonyx

    .. tab:: GitHub

        .. only:: latex

            .. rubric:: pip (GitHub)

        .. code-block:: console

            (.venv) $ pip install --force-reinstall git+https://github.com/nineteendo/jsonyx

.. tab:: pipx

    .. tab:: PyPI

        .. only:: latex

            .. rubric:: pipx (PyPI)

        .. code-block:: console

            $ pipx install jsonyx

    .. tab:: GitHub

        .. only:: latex

            .. rubric:: pipx (GitHub)

        .. code-block:: console

            $ pipx install -f git+https://github.com/nineteendo/jsonyx

.. tab:: conda

    .. tab:: conda-forge

        .. only:: latex

            .. rubric:: conda (conda-forge)

        .. code-block:: console

            (base) $ conda install conda-forge::jsonyx

Check if the correct version is installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

.. tab:: long options


    .. only:: latex

        .. rubric:: long options

    .. code-block:: console

        $ jsonyx --version
        jsonyx 2.0.0

.. tab:: short options

    .. only:: latex

        .. rubric:: short options

    .. code-block:: console

        $ jsonyx -v
        jsonyx 2.0.0

Quick start
-----------

Encoding basic Python object hierarchies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionchanged:: 2.0
    Made :class:`tuple` JSON serializable

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
    >>> json.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'
    >>> json.dump('"foo\bar')
    "\"foo\bar"
    >>> json.dump("\\")
    "\\"
    >>> json.dump("\u20AC")
    "€"
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

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> encoder = json.Encoder()
    >>> encoder.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'
    >>> encoder.dump('"foo\bar')
    "\"foo\bar"
    >>> encoder.dump("\\")
    "\\"
    >>> encoder.dump("\u20AC")
    "€"
    >>> from io import StringIO
    >>> io = StringIO()
    >>> encoder.dump(["streaming API"], io)
    >>> io.getvalue()
    '["streaming API"]\n'
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     filename = Path(tmpdir) / "file.json"
    ...     encoder.write(["filesystem API"], filename)
    ...     filename.read_text("utf_8")
    ...
    '["filesystem API"]\n'

Compact encoding
^^^^^^^^^^^^^^^^

.. versionchanged:: 2.0

    - Added ``quoted_keys``.
    - Merged ``item_separator`` and ``key_separator`` as ``separators``.

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
    >>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", separators=(",", ":"))
    '{"a":1,"b":2,"c":3}'

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> encoder = json.Encoder(end="", separators=(",", ":"))
    >>> encoder.dumps({"a": 1, "b": 2, "c": 3})
    '{"a":1,"b":2,"c":3}'

.. tip:: Use ``quoted_keys=False`` for even more compact encoding, but this
    isn't widely supported.

Pretty printing
^^^^^^^^^^^^^^^

.. versionchanged:: 2.0
    Added ``indent_leaves``.

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
    >>> json.dump({"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}, indent=4)
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> encoder = json.Encoder(indent=4)
    >>> encoder.dump({"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}})
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

.. tip:: Use ``ensure_ascii=True`` to escape non-ASCII characters,
    ``indent_leaves=True`` to indent everything and ``sort_keys=True`` to sort
    the keys of objects.

.. seealso:: The built-in :mod:`pprint` module for pretty-printing arbitrary
    Python data structures.

Decoding JSON
^^^^^^^^^^^^^

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
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
    ...     json.read(filename)
    ...
    ['filesystem API']

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> decoder = json.Decoder()
    >>> decoder.loads('{"foo": ["bar", null, 1.0, 2]}')
    {'foo': ['bar', None, 1.0, 2]}
    >>> decoder.loads(r'"\"foo\bar"')
    '"foo\x08ar'
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> decoder.load(io)
    ['streaming API']
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     filename = Path(tmpdir) / "file.json"
    ...     _ = filename.write_text('["filesystem API"]', "utf_8")
    ...     decoder.read(filename)
    ...
    ['filesystem API']

Using :class:`decimal.Decimal` instead of :class:`float`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
    >>> json.loads("[1.0000000000000001, 1e400]", use_decimal=True)
    [Decimal('1.0000000000000001'), Decimal('1E+400')]

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> decoder = json.Decoder(use_decimal=True)
    >>> decoder.loads("[1.0000000000000001, 1e400]")
    [Decimal('1.0000000000000001'), Decimal('1E+400')]

.. note:: :class:`decimal.Decimal` can be natively serialized, but not as fast
    as :class:`float`.

Making a patch from two Python objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

>>> import jsonyx as json
>>> json.make_patch([1, 2, 3], [1, 3])
[{'op': 'del', 'path': '$[1]'}]

Applying a patch
^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>>
    >>> json.apply_patch([1, 2, 3], {'op': 'del', 'path': '$[1]'})
    [1, 3]

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> manipulator = json.Manipulator()
    >>> manipulator.apply_patch([1, 2, 3], {'op': 'del', 'path': '$[1]'})
    [1, 3]

.. tip:: Using queries instead of indices is more robust.

Using the ``jsonyx`` application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

.. tab:: long options

    .. only:: latex

        .. rubric:: long options

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

.. tab:: short options

    .. only:: latex

        .. rubric:: short options

    .. code-block:: shell-session

        $ echo '{"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}' | jsonyx format -i4
        {
            "foo": [1, 2, 3],
            "bar": {"a": 1, "b": 2, "c": 3}
        }
        $ echo '{1.2: 3.4}' | jsonyx format
          File "<stdin>", line 1, column 2
            {1.2: 3.4}
             ^
        jsonyx.JSONSyntaxError: Expecting string

See :doc:`api/index` and :doc:`cli/index` for more details.
