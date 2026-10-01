Changelog
=========

:mod:`jsonyx` uses a ``[major].[feature].[fix]`` versioning scheme, where:

- The **major** version increments for foundational changes or major overhauls,
- The **feature** version increments for new features or enhancements, and
- The **fix** version increments for bug or security fixes.

.. warning:: Breaking changes can occur in major and feature versions, so read
  the changelog before updating.

jsonyx 2.4.0 (unreleased)
-------------------------

New Features:
    - Added ``formatters`` to :class:`jsonyx.Encoder`, :func:`jsonyx.dump` and
      :func:`jsonyx.dumps`
    - Made :class:`frozendict` serializable by default

Breaking Changes:
    - Allowed overriding serialization in subclasses of :class:`str` (e.g.
      :class:`enum.Enum`):

      .. code-block:: diff

           >>> import jsonyx as json
          ->>> from enum import Enum
          ->>> class MyEnum(str, Enum):
          +>>> from enum import ReprEnum
          +>>> class MyEnum(str, ReprEnum):
           ...     EMPTY = ""
           ... 
           >>> json.dump(MyEnum.EMPTY)
           ""

    - Removed ``--use-decimal`` (alias ``-d``) from ``jsonyx diff``,
      ``jsonyx format`` and ``jsonyx patch``
    - Removed ``use_decimal`` from :func:`jsonyx.apply_filter`,
      :func:`jsonyx.apply_patch`, :func:`jsonyx.load_query_value`,
      :func:`jsonyx.paste_values`, :func:`jsonyx.select_nodes`, and
      :class:`jsonyx.Manipulator`
    - Removed :class:`decimal.Decimal` support from :func:`jsonyx.make_patch`
    - Removed :data:`!jsonyx.Decoder.read` and :func:`!jsonyx.read`:

      .. code-block:: diff

           >>> import jsonyx as json
           >>> from os.path import join
           >>> from tempfile import TemporaryDirectory
           >>> with TemporaryDirectory() as tmpdir:
           ...     filename = join(tmpdir, "file.json")
           ...     with open(filename, "w", encoding="utf-8") as fp:
           ...         _ = fp.write('["reader protocol"]')
          -...     json.read(filename)
          +...     with open(filename, "rb") as fp:
          +...         json.load(fp)
           ...
           ['reader protocol']

    - Removed :data:`!jsonyx.Encoder.write` and :func:`!jsonyx.write`:

      .. code-block:: diff

           >>> import jsonyx as json
           >>> from os.path import join
           >>> from tempfile import TemporaryDirectory
           >>> with TemporaryDirectory() as tmpdir:
           ...     filename = join(tmpdir, "file.json")
          -...     json.write(["writer protocol"], filename)
          +...     with open(filename, "w", encoding="utf-8") as fp:
          +...         json.dump(["writer protocol"], fp)
           ...     with open(filename, "r", encoding="utf-8") as fp:
           ...         fp.read()
           ...
           '["writer protocol"]\n'

Other Changes:
    - Added free threading support
    - Improved diffing algorithm of :func:`jsonyx.make_patch`
    - Improved error messages
    - Replaced GPL-3.0 license with LGPL-3.0

Bug Fixes:
    - Fixed :issue:`python/cpython#142831`: Use-after-free in
      :func:`jsonyx.dumps` mapping iteration via re-entrant key encoder

jsonyx 2.3.0 (Apr 30, 2025)
---------------------------

Changes:
    - Sped up string encoding

jsonyx 2.2.1 (Apr 21, 2025)
---------------------------

Bug Fixes:
    - Fixed :issue:`36`: Fatal Python error: none_dealloc
    - Fixed :issue:`33`: Performance regression compared to :mod:`json`

jsonyx 2.2.0 (Mar 31, 2025)
---------------------------

Breaking Changes:
    - Added ``cache_keys`` (default ``False`` instead of ``True``) to
      :class:`jsonyx.Decoder`, :func:`jsonyx.load`, :func:`jsonyx.loads` and
      :func:`!jsonyx.read`

jsonyx 2.1.0 (Mar 30, 2025)
---------------------------

New Features:
    - Added ``check_circular``, ``hook`` and ``skipkeys`` to
      :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
      :func:`!jsonyx.write`

jsonyx 2.0.0 (Mar 27, 2025)
---------------------------

New Features:
    - Added the ``jsonyx`` application
    - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
      ``quoted_keys`` and ``types`` to :class:`jsonyx.Encoder`,
      :func:`jsonyx.dump`, :func:`jsonyx.dumps` and :func:`!jsonyx.write`
    - Added ``encoding`` to :func:`!jsonyx.write` and
      :meth:`!jsonyx.Encoder.write`
    - Added ``python -m jsonyx diff``
    - Added ``python -m jsonyx patch``
    - Added ``--no-indent-leaves`` (alias ``-l``) to
      ``python -m jsonyx format``
    - Added ``--max-indent-level`` (alias ``-L``) to
      ``python -m jsonyx format``
    - Added ``--unquoted-keys`` (alias ``-q``) to ``python -m jsonyx format``
    - Added ``--version`` (alias ``-v``) to ``python -m jsonyx``
    - Added :data:`jsonyx.allow.NON_STR_KEYS`
    - Added :data:`jsonyx.allow.UNQUOTED_KEYS`
    - Added :func:`jsonyx.apply_filter`
    - Added :func:`jsonyx.apply_patch`
    - Added :func:`jsonyx.load_query_value`
    - Added :func:`jsonyx.make_patch`
    - Added :func:`jsonyx.paste_values`
    - Added :func:`jsonyx.select_nodes`
    - Added :class:`jsonyx.Manipulator`
    - Added :exc:`jsonyx.TruncatedSyntaxError`
    - Made :class:`tuple` serializable by default

Breaking Changes:
    - Allowed overriding serialization in subclasses of :class:`float` and
      :class:`int` (e.g. :class:`enum.Enum`):

      .. code-block:: diff

           >>> import jsonyx as json
          ->>> from enum import Enum
          ->>> class MyEnum(float, Enum): # or int
          +>>> from enum import ReprEnum
          +>>> class MyEnum(float, ReprEnum): # or int
           ...     ZERO = 0
           ... 
           >>> json.dump(MyEnum.ZERO)
           0.0

    - Made :class:`decimal.Decimal` not serializable by default:

      .. code-block:: diff

           >>> import jsonyx as json
           >>> from decimal import Decimal
          ->>> json.dump(Decimal('1.1'))
          +>>> json.dump(Decimal('1.1'), types={"float": Decimal})
           1.1

    - Removed :data:`!jsonyx.allow.DUPLICATE_KEYS`:

      .. code-block:: diff

           >>> import jsonyx as json
          ->>> import jsonyx.allow
          ->>> json.loads('{"a": 1, "a": 2}', allow=jsonyx.allow.DUPLICATE_KEYS)
          -{'a': 1, 'a': 2}
          +>>> from multidict import MultiDict
          +>>> json.loads('{"a": 1, "a": 2}', hooks={"object": MultiDict})
          +<MultiDict('a': 1, 'a': 2)>

    - Removed :class:`!jsonyx.DuplicateKey`
    - Removed :mod:`!jsonyx.tool`
    - Renamed ``python -m jsonyx`` to ``python -m jsonyx format``
    - Replaced ``item_separator`` and ``key_separator`` with ``separators`` for
      :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
      :func:`!jsonyx.write`:

      .. code-block:: diff

           >>> import jsonyx as json
          ->>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", item_separator=",", key_separator=":")
          +>>> json.dumps({"a": 1, "b": 2, "c": 3}, end="", separators=(",", ":"))
           '{"a":1,"b":2,"c":3}'

    - Replaced ``use_decimal`` with ``hooks`` for :class:`jsonyx.Decoder`,
      :func:`jsonyx.load`, :func:`jsonyx.loads` and :func:`!jsonyx.read`:

      .. code-block:: diff

           >>> import jsonyx as json
           >>> from decimal import Decimal
          ->>> json.loads("1.1", use_decimal=True)
          +json.loads("1.1", hooks={"float": Decimal})
           Decimal('1.1')

Other Changes:
    - Added cache for indentations in the JSON encoder
    - Added support for Python 3.8 and Python 3.9
    - Improved documentation
    - Improved error messages

Bug Fixes:
    - Fixed :issue:`32`: Line comments continue until the end of file
    - Fixed :issue:`python/cpython#125660`: Python implementation of
      :func:`jsonyx.loads` accepts invalid unicode escapes
    - Fixed :issue:`python/cpython#125682`: Python implementation of
      :func:`jsonyx.loads` accepts non-ascii digits

jsonyx 1.2.1 (Aug 3, 2024)
--------------------------

Changes:
    - First conda release.

Bug Fixes:
    - Fixed :issue:`2`: Middle of error context is truncated incorrectly

jsonyx 1.2.0 (Aug 3, 2024)
--------------------------

New Features:
    - Added :option:`!output_filename`
    - Added :option:`!-a` as an alias to :option:`!--ensure-ascii`
    - Added :option:`!-c` as an alias to :option:`!--compact`
    - Added :option:`!-C` as an alias to :option:`!--no-commas`
    - Added :option:`!-d` as an alias to :option:`!--use-decimal`
    - Added :option:`!-i` as an alias to :option:`!--indent`
    - Added :option:`!-s` as an alias to :option:`!--sort-keys`
    - Added :option:`!-S` as an alias to :option:`!--nonstrict`
    - Added :option:`!-t` as an alias to :option:`!--trailing-comma`
    - Added :option:`!-T` as an alias to :option:`!--indent-tab`

Other Changes:
    - Renamed :option:`!filename` to :option:`!input_filename`

jsonyx 1.1.0 (Aug 3, 2024)
--------------------------

Breaking Changes:
    - Renamed ``python -m jsonyx.tool`` to ``python -m jsonyx``

jsonyx 1.0.0 (Aug 3, 2024)
--------------------------

Initial release