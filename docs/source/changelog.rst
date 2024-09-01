Changelog
=========

v2.0.0 (unreleased)
-------------------

- Added the ``jsonyx`` command line utility
- Added *indent_leaves* and *unquoted_keys* to :class:`jsonyx.Encoder`, :func:`jsonyx.dump`,
  :func:`jsonyx.dumps` and :func:`jsonyx.write`
- Added :data:`jsonyx.allow.UNQUOTED_KEYS`
- Added :func:`jsonyx.apply_patch` and :func:`jsonyx.make_patch`
- Added :func:`jsonyx.load_query_value`
- Added :func:`jsonyx.run_filter_query` and :func:`jsonyx.run_select_query`
- Added :func:`jsonyx.Manipulator`
- Added :option:`command`
- Added :option:`old_input_filename` and :option:`patch_filename`
- Added :option:`--indent-leaves` and its alias :option:`-l`
- Added :option:`--unquoted-keys` and its alias :option:`-u`
- Fixed comment detection
- Fixed typo in error message
- Improved documentation
- Made :class:`collections.abc.Mapping` and :class:`collections.abc.Sequence`
  JSON serializable
- Removed :mod:`!jsonyx.tool`

`v1.2.1 <https://pypi.org/project/jsonyx/1.2.1>`_
-------------------------------------------------

- First conda release
- Fixed `#2 <https://github.com/nineteendo/jsonyx/issues/2>`_: Middle of error
  context is truncated incorrectly

`v1.2.0 <https://pypi.org/project/jsonyx/1.2.0>`_
-------------------------------------------------

- Added :option:`output_filename`
- Added :option:`-a` as an alias to :option:`--ensure-ascii`
- Added :option:`-c` as an alias to :option:`--compact`
- Added :option:`-C` as an alias to :option:`--no-commas`
- Added :option:`-d` as an alias to :option:`--use-decimal`
- Added :option:`-i` as an alias to :option:`--indent`
- Added :option:`-s` as an alias to :option:`--sort-keys`
- Added :option:`-S` as an alias to :option:`--nonstrict`
- Added :option:`-t` as an alias to :option:`--trailing-comma`
- Added :option:`-T` as an alias to :option:`--indent-tab`
- Renamed :option:`!filename` to :option:`input_filename`

`v1.1.0 <https://pypi.org/project/jsonyx/1.1.0>`_
-------------------------------------------------

- Allowed ``python -m jsonyx`` instead of ``python -m jsonyx.tool``
