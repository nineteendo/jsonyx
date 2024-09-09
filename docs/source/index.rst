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

We recommend to use ``orjson`` for performance critical applications:

=====================================================  ======  ========  ========  ============  ===========
encode                                                   json    jsonyx    orjson    simplejson    unit (μs)
=====================================================  ======  ========  ========  ============  ===========
Array with 256 doubles                                  22.67     22.22      1.00         23.98         9.07
Array with 256 UTF-8 strings                            20.64      9.07      1.00         15.72        17.76
Array with 256 strings                                  12.39     11.28      1.00         13.32         4.26
Medium complex object                                    9.97     12.54      1.00         15.95        14.27
Array with 256 True values                               4.73      4.23      1.00          6.97         1.80
Array with 256 dict{string, int} pairs                  11.31     24.53      1.00         34.79         8.34
Dict with 256 arrays with 256 dict{string, int} pairs    9.26     20.32      1.00         29.77      2594.64
Complex object                                           1.16      1.00    inf             1.56      1384.86
=====================================================  ======  ========  ========  ============  ===========

=====================================================  ======  ========  ========  ============  ===========
decode                                                   json    jsonyx    orjson    simplejson    unit (μs)
=====================================================  ======  ========  ========  ============  ===========
Array with 256 doubles                                   6.84      7.19      1.00          6.86         9.95
Array with 256 UTF-8 strings                             1.17      1.00      2.02          1.31        64.42
Array with 256 strings                                   1.70      1.74      1.00          2.39        12.80
Medium complex object                                    2.92      3.60      1.00          3.67        34.57
Array with 256 True values                               3.07      4.94      1.00          7.25         2.18
Array with 256 dict{string, int} pairs                   3.38      2.83      1.00          3.44        36.09
Dict with 256 arrays with 256 dict{string, int} pairs    1.61      1.91      1.00          1.80     19592.58
Complex object                                           1.16      1.06      1.00          1.29      1075.54
=====================================================  ======  ========  ========  ============  ===========

Check out the :doc:`get-started` section for further information, including how
to :ref:`install <installation>` the project.

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
