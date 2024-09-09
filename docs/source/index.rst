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

===========================================  ======  ========  ========  ============  ===========
encode                                         json    jsonyx    orjson    simplejson    unit (μs)
===========================================  ======  ========  ========  ============  ===========
List of 256 booleans                           4.25      3.77      1.00          6.04         2.02
List of 256 ASCII strings                     15.04     13.59      1.00         15.62         3.59
List of 256 dicts with 1 int                  11.01     24.97      1.00         33.83         8.21
List of 256 doubles                           24.72     24.65      1.00         24.90         8.39
Medium complex object                         10.14     12.76      1.00         16.06        14.08
List of 256 strings                           24.91     11.64      1.00         19.59        14.22
Complex object                                 1.17      1.00    inf             1.48      1390.97
Dict with 256 lists of 256 dicts with 1 int    9.70     20.34      1.00         31.16      2538.13
===========================================  ======  ========  ========  ============  ===========

===========================================  ======  ========  ========  ============  ===========
decode                                         json    jsonyx    orjson    simplejson    unit (μs)
===========================================  ======  ========  ========  ============  ===========
List of 256 booleans                           3.42      4.98      1.00          4.29         2.00
List of 256 ASCII strings                      1.67      1.71      1.00          2.39        13.00
List of 256 dicts with 1 int                   2.28      2.76      1.00          3.22        33.16
List of 256 doubles                            6.69      7.59      1.00          6.67        10.11
Medium complex object                          2.93      3.66      1.00          3.69        33.71
List of 256 strings                            1.02      1.00      2.02          1.30        64.05
Complex object                                 1.13      1.07      1.00          1.22      1068.31
Dict with 256 lists of 256 dicts with 1 int    1.57      1.82      1.00          1.92     18632.05
===========================================  ======  ========  ========  ============  ===========

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
