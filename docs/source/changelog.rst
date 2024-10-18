Changelog
=========

jsonyx 2.0.0 (unreleased)
-------------------------

.. todo:: Add release date

- Added support for Python 3.8 and Python 3.9
- Added the ``jsonyx`` application
- Added ``commas``, ``indent_leaves``, ``mapping_types``, ``seq_types`` and
  ``quoted_keys`` to :class:`jsonyx.Encoder`, :func:`jsonyx.dump`,
  :func:`jsonyx.dumps` and :func:`jsonyx.write`
- Added ``python -m jsonyx diff`` and ``python -m jsonyx patch``
- Added ``--indent-leaves`` and its alias ``-l`` to ``python -m jsonyx format``
- Added ``--unquoted-keys`` and its alias ``-q`` to ``python -m jsonyx format``
- Added ``--version`` and its alias ``-v`` to ``python -m jsonyx``
- Added :data:`jsonyx.allow.UNQUOTED_KEYS`
- Added :func:`jsonyx.apply_patch` and :func:`jsonyx.make_patch`
- Added :func:`jsonyx.load_query_value`
- Added :func:`jsonyx.run_filter_query` and :func:`jsonyx.run_select_query`
- Added :func:`jsonyx.Manipulator`
- Changed error for big integers to :exc:`jsonyx.JSONSyntaxError`
- Fixed line comment detection
- Fixed typo in error message
- Improved documentation
- Made :class:`tuple` JSON serializable
- Merged ``item_separator`` and ``key_separator`` as ``separators`` for
  :class:`jsonyx.Encoder`, :func:`jsonyx.dump`, :func:`jsonyx.dumps` and
  :func:`jsonyx.write`
- Reject invalid unicode escapes
- Rejected non-ascii numbers conforming to the json specification
- Removed leading and trailing whitespace from error messages
- Removed :mod:`!jsonyx.tool`
- Renamed ``python -m jsonyx`` to ``python -m jsonyx format``
- Sped up decimal encoding

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
