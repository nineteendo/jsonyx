Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <http://json.org>`_ library for Python
3.8+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

.. rubric:: Key Features

- JSON decoding, encoding and patching
- Pretty-printing:
    .. code-block:: json

        {
            "foo": [1, 2, 3],
            "bar": {"a": 1, "b": 2, "c": 3}
        }

- Optionally supports these JSON deviations (according to
  :doc:`this specification <jsonyx-spec>`):

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

.. rubric:: Benchmark (Mar 17, 2025)

We recommend to use :pypi:`orjson`, :pypi:`msgspec` or :pypi:`pysimdjson` for
performance critical applications:

=========================================== ====== ====== ======= ======== ============
encode                                        json jsonyx msgspec   orjson fastest time
=========================================== ====== ====== ======= ======== ============
List of 256 booleans                         4.69x  5.64x   1.00x     1.04      1.92 μs
List of 256 ASCII strings                   13.08x 15.03x   1.62x     1.00      3.67 μs
List of 256 floats                          24.38x 24.69x   1.35x     1.00      7.89 μs
List of 256 dicts with 1 int                11.34x 14.32x   1.35x     1.00      7.67 μs
Medium complex object                       10.64x 12.05x   1.15x     1.00     13.38 μs
List of 256 strings                         21.28x 15.85x   1.95x     1.00     15.16 μs
Complex object                               7.14x  7.65x   1.00x DNF [1]_    213.74 μs
Dict with 256 lists of 256 dicts with 1 int  9.03x 11.34x   1.14x     1.00   2423.70 μs
=========================================== ====== ====== ======= ======== ============

=========================================== ====== ====== ======= ====== ======== ============
decode                                        json jsonyx msgspec orjson simdjson fastest time
=========================================== ====== ====== ======= ====== ======== ============
List of 256 booleans                         4.65x  7.19x   3.02x  1.41x    1.00x      1.43 μs
List of 256 ASCII strings                    7.35x 12.65x   4.73x  4.42x    1.00x      2.98 μs
List of 256 floats                          10.85x 12.17x   2.16x  1.66x    1.00x      6.10 μs
List of 256 dicts with 1 int                13.56x 16.11x   6.92x  5.24x    1.00x      6.17 μs
Medium complex object                       12.47x 18.84x   5.25x  4.34x    1.00x      7.68 μs
List of 256 strings                          4.01x  3.41x  14.99x  8.04x    1.00x     23.47 μs
Complex object                               8.92x  7.75x   9.09x  9.16x    1.00x    145.17 μs
Dict with 256 lists of 256 dicts with 1 int 17.95x 22.36x  12.42x 10.53x    1.00x   1621.17 μs
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
