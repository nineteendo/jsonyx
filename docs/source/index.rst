Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <http://json.org>`_ library for Python
3.10+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

.. rubric:: Key Features

- JSON decoding, encoding and patching
- Pretty-printing:

.. code-block:: json

    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

- Optionally supports these JSON deviations using :mod:`jsonyx.allow`:

.. code-block:: javascript

    {
        /* Block */ // and line comments
        "Decimal numbers": [1.0000000000000001, 1e400],
        "Duplicate keys": {"key": "value 1", "key": "value 2"},
        "Missing commas": [1 2 3],
        "NaN and infinity": [NaN, Infinity, -Infinity],
        "Surrogates": "\ud800",
        "Trailing comma": [0,],
        "Unquoted keys": {key: "value"}
    }

- Detailed error messages:

.. code-block:: none

    Traceback (most recent call last):
      File "C:\Users\wanne\Downloads\broken.json", line 2, column 15-19
        "path": "c:\users"
                     ^^^^
    jsonyx.JSONSyntaxError: Expecting 4 hex digits

- Dedicated functions for reading and writing files and pretty printing

.. rubric:: Benchmark

We recommend to use ``orjson`` or ``msgspec`` for performance critical
applications:

+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| encode                       |  json | jsonyx | msgspec |   orjson | rapidjson | simplejson | unit (μs) |
+==============================+=======+========+=========+==========+===========+============+===========+
| List of 256 booleans         |  9.49 |   8.90 |    1.38 |     1.00 |      3.41 |       6.97 |      2.02 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| List of 256 ASCII strings    | 13.35 |  12.31 |    1.60 |     1.00 |      9.46 |      14.49 |      4.00 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| List of 256 dicts with 1 int | 11.16 |  24.23 |    1.47 |     1.00 |      6.40 |      33.29 |      8.43 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| List of 256 doubles          | 24.05 |  23.37 |    1.42 |     1.00 |     24.83 |      24.64 |      8.60 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| Medium complex object        | 10.00 |  12.59 |    1.24 |     1.00 |      7.37 |      15.81 |     14.32 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| List of 256 strings          | 25.35 |  11.89 |    2.42 |     1.00 |     32.46 |      20.08 |     13.91 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| Complex object               |  7.68 |   6.72 |    1.00 | inf [1]_ |      6.85 |       9.63 |    211.44 |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+
| Dict with 256 lists of 256   | 10.33 |  22.58 |    1.42 |     1.00 |      5.95 |      33.45 |   2347.07 |
| dicts with 1 int             |       |        |         |          |           |            |           |
+------------------------------+-------+--------+---------+----------+-----------+------------+-----------+


+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| decode                       |   json | jsonyx | msgspec | orjson | rapidjson | simplejson | unit (μs) |
+==============================+========+========+=========+========+===========+============+===========+
| List of 256 booleans         |   3.44 |   5.07 |    2.10 |   1.00 |      2.44 |       4.29 |      2.03 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| List of 256 ASCII strings    |   1.71 |   1.70 |    1.14 |   1.00 |      1.66 |       2.36 |     13.01 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| List of 256 dicts with 1 int |   2.37 |   2.84 |    1.42 |   1.00 |      2.22 |       3.34 |     32.31 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| List of 256 doubles          |   6.62 |   6.96 |    1.45 |   1.00 |      5.65 |       6.51 |     10.32 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| Medium complex object        |   2.95 |   3.67 |    1.24 |   1.00 |      2.69 |       3.72 |     33.62 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| List of 256 strings          |   1.00 |   1.00 |    2.63 |   1.96 |      2.87 |       1.27 |     67.23 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| Complex object               |   1.18 |   1.06 |    1.08 |   1.00 |      1.23 |       1.28 |   1077.42 |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+
| Dict with 256 lists of 256   |   1.63 |   1.86 |    1.12 |   1.00 |      1.43 |       2.09 |  17881.06 |
| dicts with 1 int             |        |        |         |        |           |            |           |
+------------------------------+--------+--------+---------+--------+-----------+------------+-----------+

Check out the :doc:`get-started` section for further information, including how
to :ref:`install <installation>` the project.

.. rubric:: Footnotes

.. [1] failed due to recursion error

.. toctree::
    :hidden:

    get-started
    how-to
    api/index
    cli

.. toctree::
    :caption: About the Project
    :hidden:

    changelog
    License <https://github.com/nineteendo/jsonyx/blob/main/LICENSE>

.. toctree::
    :caption: Project Links
    :hidden:

    PyPI Package <https://pypi.org/project/jsonyx>
    Conda Package <https://anaconda.org/conda-forge/jsonyx>
    GitHub Repository <https://github.com/nineteendo/jsonyx>
    Issue Tracker <https://github.com/nineteendo/jsonyx/issues>
    Sponser <https://paypal.me/nineteendo>
