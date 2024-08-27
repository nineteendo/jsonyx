Changelog
=========

v2.0.0
------

- Added :option:`command`
- Added :option:`old_input_filename`
- Added :option:`patch_filename`
- Added :func:`jsonyx.apply_patch`
- Added :func:`jsonyx.apply_patch`
- Added :func:`jsonyx.apply_patch`
- Added :func:`jsonyx.run_select_query`
- Added :func:`jsonyx.run_filter_query`
- Added :func:`jsonyx.load_query_value`
- Added :func:`jsonyx.make_patch`
- Added :func:`jsonyx.Manipulator`
- Fixed typo in error message
- Improved documentation
- Removed :mod:`!jsonyx.tool`

v1.2.0
------

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
- Fixed `#2 <https://github.com/nineteendo/jsonyx/issues/2>`_: Middle of error context is truncated incorrectly
- Renamed :option:`!filename` to :option:`input_filename`

v1.1.0
------

- Allow ``python -m jsonyx`` instead of ``python -m jsonyx.tool``
