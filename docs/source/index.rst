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

We recommend to use :pypi:`orjson` or :pypi:`msgspec` for performance critical
applications:

===========================================  =====  ======  =======  ========  =========  =========
encode                                        json  jsonyx  msgspec    orjson  rapidjson  unit (μs)
===========================================  =====  ======  =======  ========  =========  =========
List of 256 booleans                          4.82    4.11     1.16      1.00       3.12       1.85
List of 256 ASCII strings                    14.71   12.73     1.67      1.00      10.12       3.64
List of 256 floats                           23.47   23.54     1.38      1.00      24.87       8.57
List of 256 dicts with 1 int                 10.87   11.17     1.48      1.00       6.30       8.54
Medium complex object                         9.90    9.76     1.24      1.00       7.31      14.48
List of 256 strings                          26.73   14.99     2.26      1.00      34.28      13.69
Complex object                                7.80    5.55     1.00  inf [1]_       6.92     205.10
Dict with 256 lists of 256 dicts with 1 int   9.58   10.23     1.27      1.00       5.32    2517.22
===========================================  =====  ======  =======  ========  =========  =========

===========================================  ====  ======  =======  ======  =========  =========
decode                                       json  jsonyx  msgspec  orjson  rapidjson  unit (μs)
===========================================  ====  ======  =======  ======  =========  =========
List of 256 booleans                         3.40    5.24     2.06    1.00       2.42       2.03
List of 256 ASCII strings                    1.68    2.05     1.12    1.00       1.59      13.11
List of 256 floats                           6.58    7.38     1.45    1.00       5.71      10.25
List of 256 dicts with 1 int                 2.36    2.84     1.38    1.00       2.22      32.11
Medium complex object                        2.89    3.70     1.23    1.00       2.62      33.99
List of 256 strings                          1.02    1.00     2.74    2.04       2.99      64.38
Complex object                               1.12    1.04     1.06    1.00       1.23    1061.41
Dict with 256 lists of 256 dicts with 1 int  1.66    1.91     1.14    1.00       1.47   17536.25
===========================================  ====  ======  =======  ======  =========  =========

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
    genindex

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
