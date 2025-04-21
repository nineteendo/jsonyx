Welcome to jsonyx's Documentation!
==================================

.. meta::
    :google-site-verification: Htf0oc5j12UrWDfRoSv2B_0mn4S_mJ2P7eFiE63wwgg

:mod:`jsonyx` is a customizable `JSON <https://json.org>`_ library for Python
3.8+. It is written in pure Python with an optional C extension for better
performance and no dependencies.

Key Features
------------

- JSON decoding, encoding and patching
- Pretty-printing:

  .. code-block:: json

      {
          "foo": [1, 2, 3],
          "bar": {"a": 1, "b": 2, "c": 3}
      }

- Optionally supports these JSON deviations (according to
  :doc:`this specification </jsonyx-spec>`):

  .. code-block:: javascript

      {
          /* Block */ // and line comments
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

Benchmark (Apr 20, 2025)
------------------------

We recommend to use :pypi:`orjson`, :pypi:`msgspec` or :pypi:`pysimdjson` for
performance critical applications:

.. tab:: Python 3.9.20

    .. only:: latex

        .. rubric:: encode (Python 3.9.20)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         9.73x  5.09x   1.11x    1.00x      1.68 μs
    List of 256 ASCII strings                   11.37x 13.10x   1.59x    1.00x      3.81 μs
    List of 256 floats                          22.98x 22.71x   1.41x    1.00x      8.04 μs
    List of 256 dicts with 1 int                11.13x  9.06x   3.10x    1.00x     10.01 μs
    Medium complex object                       18.03x 13.09x   1.08x    1.00x     16.19 μs
    List of 256 strings                         22.89x 19.54x   2.30x    1.00x     14.23 μs
    Complex object                               7.18x  7.01x   1.00x DNF [1]_    223.33 μs
    Dict with 256 lists of 256 dicts with 1 int 13.27x  9.45x   1.19x    1.00x   2422.11 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: encode (Python 3.10.15)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.23x  3.93x   1.00x    1.00x      1.89 μs
    List of 256 ASCII strings                   12.79x 13.04x   1.70x    1.00x      3.66 μs
    List of 256 floats                          22.16x 22.32x   1.26x    1.00x      8.16 μs
    List of 256 dicts with 1 int                13.16x 10.53x   1.36x    1.00x      8.21 μs
    Medium complex object                       10.72x  9.74x   1.13x    1.00x     13.95 μs
    List of 256 strings                         22.61x 18.54x   1.90x    1.00x     15.22 μs
    Complex object                               7.84x  7.15x   1.00x DNF [1]_    212.84 μs
    Dict with 256 lists of 256 dicts with 1 int 11.95x  8.72x   1.15x    1.00x   2597.61 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: encode (Python 3.11.10)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.32x  3.89x   1.02x    1.00x      1.92 μs
    List of 256 ASCII strings                   13.55x 10.90x   1.44x    1.00x      4.15 μs
    List of 256 floats                          22.02x 22.32x   1.27x    1.00x      8.15 μs
    List of 256 dicts with 1 int                13.71x 10.37x   1.28x    1.00x      8.27 μs
    Medium complex object                       11.45x  9.97x   1.16x    1.00x     13.27 μs
    List of 256 strings                         20.80x 13.47x   2.05x    1.00x     17.48 μs
    Complex object                               8.08x  7.12x   1.00x DNF [1]_    211.77 μs
    Dict with 256 lists of 256 dicts with 1 int 13.05x  9.51x   1.21x    1.00x   2371.33 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: encode (Python 3.12.7)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.36x  3.91x   1.00x    1.03x      1.97 μs
    List of 256 ASCII strings                   10.42x 10.08x   1.37x    1.00x      4.53 μs
    List of 256 floats                          23.27x 23.37x   1.33x    1.00x      8.06 μs
    List of 256 dicts with 1 int                10.91x 11.43x   1.31x    1.00x      8.11 μs
    Medium complex object                        9.99x 10.46x   1.14x    1.00x     13.60 μs
    List of 256 strings                         17.98x 14.32x   1.64x    1.00x     18.59 μs
    Complex object                               7.44x  7.75x   1.00x DNF [1]_    205.09 μs
    Dict with 256 lists of 256 dicts with 1 int  8.87x  9.70x   1.16x    1.00x   2453.00 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.13.0

    .. only:: latex

        .. rubric:: encode (Python 3.13.0)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.54x  4.06x   1.04x    1.00x      1.85 μs
    List of 256 ASCII strings                   11.76x 10.42x   1.33x    1.00x      4.34 μs
    List of 256 floats                          24.82x 25.10x   1.30x    1.00x      8.09 μs
    List of 256 dicts with 1 int                11.10x 11.50x   1.34x    1.00x      7.92 μs
    Medium complex object                       10.25x 11.05x   1.14x    1.00x     13.77 μs
    List of 256 strings                         22.19x 17.00x   1.86x    1.00x     15.81 μs
    Complex object                               7.54x  7.41x   1.00x DNF [1]_    215.37 μs
    Dict with 256 lists of 256 dicts with 1 int  9.34x  9.74x   1.29x    1.00x   2394.91 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.9.20
    :new-set:

    .. only:: latex

        .. rubric:: decode (Python 3.9.20)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.08x  4.86x   2.42x  1.43x         1.00x      1.51 μs
    List of 256 ASCII strings                    8.71x  7.78x   3.96x  3.83x         1.00x      3.31 μs
    List of 256 floats                           9.49x  9.35x   2.00x  1.40x         1.00x      6.21 μs
    List of 256 dicts with 1 int                11.37x 10.68x   6.09x  4.30x         1.00x      6.22 μs
    Medium complex object                       11.53x 11.95x   4.52x  3.75x         1.00x      7.94 μs
    List of 256 strings                          5.70x  3.80x   9.51x  8.71x         1.00x     16.53 μs
    Complex object                               7.86x  7.12x   8.51x  7.70x         1.00x    133.58 μs
    Dict with 256 lists of 256 dicts with 1 int 17.92x 16.51x  13.48x 11.87x         1.00x   1667.46 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: decode (Python 3.10.15)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.29x  5.20x   3.13x  1.62x         1.00x      1.38 μs
    List of 256 ASCII strings                    9.49x  8.44x   5.02x  4.68x         1.00x      2.81 μs
    List of 256 floats                           9.64x  9.13x   2.08x  1.61x         1.00x      6.16 μs
    List of 256 dicts with 1 int                10.73x 10.37x   6.01x  4.27x         1.00x      6.18 μs
    Medium complex object                       11.45x 11.66x   4.68x  3.96x         1.00x      7.64 μs
    List of 256 strings                          3.82x  2.57x   5.63x  5.09x         1.00x     24.07 μs
    Complex object                               7.91x  7.48x   8.26x  7.68x         1.00x    134.21 μs
    Dict with 256 lists of 256 dicts with 1 int 17.61x 15.95x  12.86x 12.42x         1.00x   1637.85 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: decode (Python 3.11.10)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.87x  5.12x   3.06x  1.57x         1.00x      1.46 μs
    List of 256 ASCII strings                    6.12x  6.55x   3.80x  3.79x         1.00x      3.54 μs
    List of 256 floats                           9.67x 10.88x   2.16x  1.66x         1.00x      6.17 μs
    List of 256 dicts with 1 int                11.29x 10.90x   6.88x  4.56x         1.00x      6.13 μs
    Medium complex object                       12.07x 11.22x   4.90x  3.86x         1.00x      7.95 μs
    List of 256 strings                          5.90x  3.71x   9.97x  7.10x         1.00x     16.64 μs
    Complex object                               8.85x  7.04x   8.27x  7.61x         1.00x    131.74 μs
    Dict with 256 lists of 256 dicts with 1 int 11.32x 10.20x   9.00x  8.56x         1.00x   2437.26 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: decode (Python 3.12.7)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.86x  5.37x   2.97x  1.41x         1.00x      1.40 μs
    List of 256 ASCII strings                    7.04x  7.85x   4.80x  4.36x         1.00x      3.05 μs
    List of 256 floats                          10.91x 11.18x   2.21x  1.67x         1.00x      6.12 μs
    List of 256 dicts with 1 int                12.05x 11.64x   6.86x  5.00x         1.00x      6.24 μs
    Medium complex object                       11.85x 11.81x   4.88x  4.16x         1.00x      8.11 μs
    List of 256 strings                          5.57x  3.74x   9.82x  7.53x         1.00x     16.86 μs
    Complex object                               8.78x  7.45x   8.56x  7.60x         1.00x    137.30 μs
    Dict with 256 lists of 256 dicts with 1 int 17.32x 14.97x  11.67x 10.68x         1.00x   1704.53 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.13.0

    .. only:: latex

        .. rubric:: decode (Python 3.13.0)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.36x  5.26x   2.76x  1.40x         1.00x      1.46 μs
    List of 256 ASCII strings                    8.54x  6.93x   4.28x  3.96x         1.00x      3.46 μs
    List of 256 floats                          10.85x 11.25x   2.23x  1.74x         1.00x      6.05 μs
    List of 256 dicts with 1 int                12.79x 11.43x   7.12x  5.19x         1.00x      6.12 μs
    Medium complex object                       12.70x 12.01x   5.16x  4.60x         1.00x      7.98 μs
    List of 256 strings                          7.11x  3.82x   9.70x  7.80x         1.00x     16.52 μs
    Complex object                               9.87x  7.74x   8.90x  7.94x         1.00x    130.28 μs
    Dict with 256 lists of 256 dicts with 1 int 17.84x 15.18x  12.08x 10.32x         1.00x   1674.28 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. warning:: The Python version of :mod:`jsonyx` is up to 36.25x slower, so
    make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.

Check out the :doc:`/get-started` section for further information, including
how to :ref:`install <installation>` the project.

.. rubric:: Footnotes

.. [1] failed due to recursion error
.. [2] delays creation of Python objects until they are accessed

.. _end_forword:

.. toctree::
    :hidden:

    Home <self>

.. _start_toctree:

.. toctree::
    :hidden:

    get-started
    how-to
    api/index
    cli/index

.. toctree::
    :caption: Specification
    :hidden:

    jsonyx-spec
    json-patch-spec
    json-path-spec

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
