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

Changes:
    - Improved error messages

jsonyx 2.3.0 (Apr 30, 2025)
---------------------------

Changes:
    - Speed up string encoding

jsonyx 2.2.1 (Apr 21, 2025)
---------------------------

Bug Fixes:
    - Fixed :issue:`36`: Fatal Python error: none_dealloc
    - Fixed :issue:`33`: Performance regression compared to :mod:`json`

jsonyx 2.2.0 (Mar 31, 2025)
---------------------------

New Features:
    - Added ``cache_keys`` to :class:`jsonyx.Decoder`, :func:`jsonyx.load`,
      :func:`jsonyx.loads` and :func:`jsonyx.read`

Breaking Changes:
    - Disabled caching keys by default for :class:`jsonyx.Decoder`,
      :func:`jsonyx.load`, :func:`jsonyx.loads` and :func:`jsonyx.read`

jsonyx 2.1.0 (Mar 30, 2025)
---------------------------

New Features:
    - Added ``check_circular``, ``hook`` and ``skipkeys`` to
      :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
      :func:`jsonyx.write`

jsonyx 2.0.0 (Mar 27, 2025)
---------------------------

New Features:
    - Added the ``jsonyx`` application
    - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
      ``quoted_keys`` and ``types`` to :class:`jsonyx.Encoder`,
      :func:`jsonyx.dump`, :func:`jsonyx.dumps` and :func:`jsonyx.write`
    - Added ``encoding`` to :func:`jsonyx.write` and
      :meth:`jsonyx.Encoder.write`
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

Breaking Changes:
    - Made :class:`tuple` serializable by default instead of :class:`enum.Enum`
      and :class:`decimal.Decimal`
    - Removed :data:`!jsonyx.allow.DUPLICATE_KEYS`
    - Removed :data:`!jsonyx.DuplicateKey`
    - Removed :mod:`!jsonyx.tool`
    - Renamed ``python -m jsonyx`` to ``python -m jsonyx format``
    - Replaced ``item_separator`` and ``key_separator`` with ``separators`` for
      :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
      :func:`jsonyx.write`
    - Replaced ``use_decimal`` with ``hooks`` for :class:`jsonyx.Decoder`,
      :func:`jsonyx.load`, :func:`jsonyx.loads` and :func:`jsonyx.read`

Other Changes:
    - Added support for Python 3.8 and Python 3.9
    - Improved documentation
    - Improved error messages
    - Use cache for indentations in the JSON encoder

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
