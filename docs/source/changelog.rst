Changelog
=========

jsonyx 2.0.0 (unreleased)
-------------------------

.. todo:: Add release date

- Added support for Python 3.8 and Python 3.9
- Added the ``jsonyx`` application
- Added ``hooks`` to :class:`jsonyx.Decoder`, :func:`jsonyx.load`,
  :func:`jsonyx.loads` and :func:`jsonyx.read`
- Added ``commas``, ``indent_leaves``, ``max_indent_level``, ``quoted_keys``
  and ``types`` to :class:`jsonyx.Encoder`, :func:`jsonyx.dump`,
  :func:`jsonyx.dumps` and :func:`jsonyx.write`
- Added ``encoding`` to :func:`jsonyx.write` and :meth:`jsonyx.Encoder.write`
- Added ``python -m jsonyx diff``
- Added ``python -m jsonyx patch``
- Added ``--no-indent-leaves`` (alias ``-l``) to ``python -m jsonyx format``
- Added ``--max-indent-level`` (alias ``-L``) to ``python -m jsonyx format``
- Added ``--unquoted-keys`` (alias ``-q``) to ``python -m jsonyx format``
- Added ``--version`` (alias ``-v``) to ``python -m jsonyx``
- Added :data:`jsonyx.allow.UNQUOTED_KEYS`
- Added :func:`jsonyx.apply_filter`
- Added :func:`jsonyx.apply_patch`
- Added :func:`jsonyx.load_query_value`
- Added :func:`jsonyx.make_patch`
- Added :func:`jsonyx.paste_values`
- Added :func:`jsonyx.select_nodes`
- Added :class:`jsonyx.Manipulator`
- Added :exc:`jsonyx.TruncatedSyntaxError`
- Fixed :issue:`32`: Line comments continue until the end of file
- Fixed :issue:`python/cpython#125660`: Python implementation of
  :func:`jsonyx.loads` accepts invalid unicode escapes
- Fixed :issue:`python/cpython#125682`: Python implementation of
  :func:`jsonyx.loads` accepts non-ascii digits
- Improved documentation
- Improved error messages
- Made :class:`tuple` JSON serializable
- Merged ``item_separator`` and ``key_separator`` as ``separators`` for
  :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
  :func:`jsonyx.write`
- Removed ``use_decimal`` from :class:`jsonyx.Decoder`, :func:`jsonyx.load`,
  :func:`jsonyx.loads` and :func:`jsonyx.read`
- Removed :data:`!jsonyx.allow.DUPLICATE_KEYS`
- Removed :data:`!jsonyx.DuplicateKey`
- Removed :mod:`!jsonyx.tool`
- Renamed ``python -m jsonyx`` to ``python -m jsonyx format``
- Sped up decimal encoding
- Use cache for indentations in the JSON encoder

jsonyx 1.2.1 (Aug 3, 2024)
--------------------------

- First conda release
- Fixed :issue:`2`: Middle of error context is truncated incorrectly

jsonyx 1.2.0 (Aug 3, 2024)
--------------------------

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
- Renamed :option:`!filename` to :option:`!input_filename`

jsonyx 1.1.0 (Aug 3, 2024)
--------------------------

- Renamed ``python -m jsonyx.tool`` to ``python -m jsonyx``
