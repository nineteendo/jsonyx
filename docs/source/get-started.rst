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

.. code-block:: console

    $ jsonyx --version
    jsonyx 2.0.0 (C extension)

.. warning:: If the version number is followed by ``(Python)``, the performance
    will be up to 36.25x slower, so make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.

Quick start
-----------

Encoding basic Python object hierarchies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionchanged:: 2.0 Made :class:`tuple` JSON serializable.

Dumping to a string:

>>> import jsonyx as json
>>> json.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
'["foo", {"bar": ["baz", null, 1.0, 2]}]\n'

Writing to standard output:

>>> import jsonyx as json
>>> json.dump('"foo\bar')
"\"foo\bar"
>>> json.dump("\\")
"\\"
>>> json.dump("\u20AC")
"€"

Writing to an open file:

>>> import jsonyx as json
>>> from io import StringIO
>>> io = StringIO()
>>> json.dump(["streaming API"], io)
>>> io.getvalue()
'["streaming API"]\n'

Writing to a file:

>>> import jsonyx as json
>>> from pathlib import Path
>>> from tempfile import TemporaryDirectory
>>> with TemporaryDirectory() as tmpdir:
...     filename = Path(tmpdir) / "file.json"
...     json.write(["filesystem API"], filename)
...     filename.read_text("utf-8")
...
'["filesystem API"]\n'

.. tip:: Using :class:`jsonyx.Encoder` is faster.

Compact encoding
^^^^^^^^^^^^^^^^

.. versionchanged:: 2.0

    - Added ``quoted_keys``.
    - Replaced ``item_separator`` and ``key_separator`` with ``separators``.

>>> import jsonyx as json
>>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", separators=(",", ":"))
'{"a":1,"b":2,"c":3}'

.. tip:: Use ``quoted_keys=False`` for even more compact encoding, but this
    isn't widely supported.

Pretty printing
^^^^^^^^^^^^^^^

.. versionchanged:: 2.0 Added ``indent_leaves`` and ``max_indent_level``.

>>> import jsonyx as json
>>> obj = {"foo": [1, 2, 3], "bar": {"a": 1, "b": 2, "c": 3}}
>>> json.dump(obj, indent=4, indent_leaves=False)
{
    "foo": [1, 2, 3],
    "bar": {"a": 1, "b": 2, "c": 3}
}

.. tip:: Use ``ensure_ascii=True`` to escape non-ASCII characters,
    ``max_indent_level=1`` to indent up to level 1, and ``sort_keys=True`` to
    sort the keys of objects.
.. seealso:: The built-in :mod:`pprint` module for pretty-printing arbitrary
    Python data structures.

Decoding JSON
^^^^^^^^^^^^^

Loading from a string:

>>> import jsonyx as json
>>> json.loads('{"foo": ["bar", null, 1.0, 2]}')
{'foo': ['bar', None, 1.0, 2]}
>>> json.loads(r'"\"foo\bar"')
'"foo\x08ar'

Reading from an open file:

>>> import jsonyx as json
>>> from io import StringIO
>>> io = StringIO('["streaming API"]')
>>> json.load(io)
['streaming API']

Reading from a file:

>>> import jsonyx as json
>>> from pathlib import Path
>>> from tempfile import TemporaryDirectory
>>> with TemporaryDirectory() as tmpdir:
...     filename = Path(tmpdir) / "file.json"
...     _ = filename.write_text('["filesystem API"]', "utf-8")
...     json.read(filename)
...
['filesystem API']

.. tip:: Using :class:`jsonyx.Decoder` is faster.

Using :class:`decimal.Decimal` instead of :class:`float`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionchanged:: 2.0

    - Added ``types``.
    - Made :class:`decimal.Decimal` not JSON serializable.
    - Replaced ``use_decimal`` with ``hooks``.

>>> import jsonyx as json
>>> from decimal import Decimal
>>> json.loads("1.1", hooks={"float": Decimal})
Decimal('1.1')
>>> json.dump(Decimal('1.1'), types={"float": Decimal})
1.1

Making a :doc:`patch </jsonyx-patch-spec>` from two Python objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

>>> import jsonyx as json
>>> json.make_patch([1, 2, 3], [1, 3])
[{'op': 'del', 'path': '$[1]'}]

Applying a :doc:`patch </jsonyx-patch-spec>`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

>>> import jsonyx as json
>>> json.apply_patch([1, 2, 3], {"op": "del", "path": "$[1]"})
[1, 3]

.. tip:: Using a :ref:`filter` instead of an index is more robust.

Using the ``jsonyx`` application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

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

See :doc:`/api/index` and :doc:`/cli/index` for more details.
