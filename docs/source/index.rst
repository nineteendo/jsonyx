Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <http://json.org>`_ library for Python
3.8+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

.. todo:: Add specification

.. rubric:: Key Features

- JSON decoding, encoding and patching
- Pretty-printing:

.. code-block:: json

    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }

- Optionally supports these JSON deviations:

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
      File "/Users/wannes/Downloads/broken.json", line 1, column 99-381
        ...sList": {"GlossEntry": {"ID": "SGM..."GML", "XML"]}, "GlossSee": "markup"
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    jsonyx.JSONSyntaxError: Unterminated object

- Dedicated functions for reading and writing files and pretty printing

.. rubric:: Benchmark (Feb 5, 2025)

We recommend to use :pypi:`orjson`, :pypi:`msgspec` or :pypi:`pysimdjson` for
performance critical applications:

=========================================== ====== ====== ======= ======== ============
encode                                        json jsonyx msgspec   orjson fastest time
=========================================== ====== ====== ======= ======== ============
List of 256 booleans                         4.49x  4.47x   1.00x    1.07x      1.95 μs
List of 256 ASCII strings                   12.41x 14.20x   1.55x    1.00x      3.76 μs
List of 256 floats                          23.03x 23.68x   1.31x    1.00x      8.08 μs
List of 256 dicts with 1 int                11.08x 13.61x   1.33x    1.00x      7.86 μs
Medium complex object                       10.29x 11.47x   1.14x    1.00x     13.71 μs
List of 256 strings                         22.45x 14.65x   2.15x    1.00x     14.31 μs
Complex object                               7.11x  5.47x   1.00x DNF [1]_    212.52 μs
Dict with 256 lists of 256 dicts with 1 int  9.32x 11.44x   1.31x    1.00x   2359.82 μs
=========================================== ====== ====== ======= ======== ============

=========================================== ====== ====== ======= ====== ======== ============
decode                                        json jsonyx msgspec orjson simdjson fastest time
=========================================== ====== ====== ======= ====== ======== ============
List of 256 booleans                         4.64x  7.19x   2.99x  1.40x    1.00x      1.42 μs
List of 256 ASCII strings                    7.61x 12.30x   5.04x  4.66x    1.00x      2.87 μs
List of 256 floats                          11.04x 12.00x   2.18x  1.64x    1.00x      6.23 μs
List of 256 dicts with 1 int                12.14x 15.93x   6.82x  5.02x    1.00x      6.22 μs
Medium complex object                       12.53x 19.08x   5.24x  4.46x    1.00x      7.72 μs
List of 256 strings                          5.37x  4.11x   9.40x  7.26x    1.00x     17.52 μs
Complex object                               9.21x  8.66x   8.91x  7.95x    1.00x    130.93 μs
Dict with 256 lists of 256 dicts with 1 int 18.00x 22.32x  12.38x 10.84x    1.00x   1622.21 μs
=========================================== ====== ====== ======= ====== ======== ============

.. warning:: The Python version of :mod:`jsonyx` is up to 36.25x slower, so
    make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.

Check out the :doc:`get-started` section for further information, including how
to :ref:`install <installation>` the project.

.. rubric:: Footnotes

.. [1] failed due to recursion error

.. toctree::
    :hidden:

    Home <self>
    get-started
    how-to
    api/index
    cli/index

.. toctree::
    :caption: Specification
    :hidden:

    jsonyx-spec
    jsonyx-patch-spec

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
