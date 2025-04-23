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
    List of 256 booleans                         7.61x  4.97x   1.01x    1.00x      1.67 μs
    List of 256 ASCII strings                   11.59x 13.00x   1.65x    1.00x      3.65 μs
    List of 256 floats                          22.74x 22.52x   1.32x    1.00x      8.13 μs
    List of 256 dicts with 1 int                 9.69x  7.92x   1.00x    1.32x     11.34 μs
    Medium complex object                       13.68x 20.81x   1.00x    1.06x     15.34 μs
    List of 256 strings                         26.63x 20.14x   2.16x    1.00x     15.40 μs
    Complex object                               7.65x  7.27x   1.00x DNF [1]_    213.92 μs
    Dict with 256 lists of 256 dicts with 1 int 12.67x  9.51x   1.17x    1.00x   2443.96 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: encode (Python 3.10.15)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.04x  3.92x   1.00x    1.02x      1.87 μs
    List of 256 ASCII strings                   11.32x 11.55x   1.40x    1.00x      4.12 μs
    List of 256 floats                          22.01x 22.09x   1.25x    1.00x      8.21 μs
    List of 256 dicts with 1 int                13.27x 10.57x   1.32x    1.00x      8.16 μs
    Medium complex object                       10.63x  9.73x   1.15x    1.00x     14.01 μs
    List of 256 strings                         22.94x 17.95x   1.81x    1.00x     15.73 μs
    Complex object                               7.76x  6.92x   1.00x DNF [1]_    215.50 μs
    Dict with 256 lists of 256 dicts with 1 int 13.09x  9.18x   1.24x    1.00x   2441.73 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: encode (Python 3.11.10)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.30x  3.76x   1.00x    1.01x      1.90 μs
    List of 256 ASCII strings                   14.33x 11.61x   1.55x    1.00x      3.90 μs
    List of 256 floats                          21.63x 21.72x   1.28x    1.00x      8.28 μs
    List of 256 dicts with 1 int                14.29x 11.26x   1.34x    1.00x      7.88 μs
    Medium complex object                       11.27x  9.79x   1.16x    1.00x     13.46 μs
    List of 256 strings                         21.70x 14.95x   2.09x    1.00x     16.08 μs
    Complex object                               8.02x  6.99x   1.00x DNF [1]_    213.72 μs
    Dict with 256 lists of 256 dicts with 1 int 13.33x  9.36x   1.30x    1.00x   2362.18 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: encode (Python 3.12.7)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.38x  4.04x   1.00x    1.04x      1.90 μs
    List of 256 ASCII strings                   13.34x 12.80x   1.67x    1.00x      3.51 μs
    List of 256 floats                          23.41x 25.06x   1.33x    1.00x      8.03 μs
    List of 256 dicts with 1 int                10.93x 11.61x   1.28x    1.00x      7.94 μs
    Medium complex object                       10.04x 10.49x   1.14x    1.00x     13.47 μs
    List of 256 strings                         23.33x 18.83x   2.24x    1.00x     13.90 μs
    Complex object                               7.27x  7.63x   1.00x DNF [1]_    208.32 μs
    Dict with 256 lists of 256 dicts with 1 int  8.26x  9.18x   1.07x    1.00x   2618.09 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.13.0

    .. only:: latex

        .. rubric:: encode (Python 3.13.0)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.58x  4.13x   1.05x    1.00x      1.84 μs
    List of 256 ASCII strings                   14.00x 11.60x   1.57x    1.00x      3.92 μs
    List of 256 floats                          24.93x 25.59x   1.34x    1.00x      8.28 μs
    List of 256 dicts with 1 int                11.58x 12.28x   1.38x    1.00x      7.84 μs
    Medium complex object                       10.12x 10.40x   1.16x    1.00x     13.87 μs
    List of 256 strings                         19.70x 14.69x   1.73x    1.00x     18.10 μs
    Complex object                               7.68x  7.55x   1.00x DNF [1]_    211.43 μs
    Dict with 256 lists of 256 dicts with 1 int  4.52x  5.43x   3.20x    1.00x   5082.41 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.9.20
    :new-set:

    .. only:: latex

        .. rubric:: decode (Python 3.9.20)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         3.77x  4.65x   2.31x  1.42x         1.00x      1.52 μs
    List of 256 ASCII strings                   10.53x  9.22x   5.16x  4.57x         1.00x      2.77 μs
    List of 256 floats                           9.31x  8.63x   1.96x  1.37x         1.00x      6.35 μs
    List of 256 dicts with 1 int                11.65x 10.79x   6.15x  4.38x         1.00x      6.21 μs
    Medium complex object                       10.95x 11.22x   4.36x  3.52x         1.00x      8.33 μs
    List of 256 strings                          5.43x  3.80x   9.01x  8.38x         1.00x     17.32 μs
    Complex object                               7.93x  7.18x   8.58x  7.74x         1.00x    132.03 μs
    Dict with 256 lists of 256 dicts with 1 int 17.98x 16.50x  13.52x 11.97x         1.00x   1653.69 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: decode (Python 3.10.15)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.21x  5.20x   3.00x  1.59x         1.00x      1.39 μs
    List of 256 ASCII strings                    9.80x  8.24x   4.90x  4.62x         1.00x      2.87 μs
    List of 256 floats                           9.75x  9.08x   2.14x  1.64x         1.00x      6.12 μs
    List of 256 dicts with 1 int                10.96x 10.52x   6.02x  4.33x         1.00x      6.16 μs
    Medium complex object                       11.39x 11.51x   4.63x  3.99x         1.00x      7.74 μs
    List of 256 strings                          4.80x  3.24x   7.20x  6.38x         1.00x     19.14 μs
    Complex object                               8.19x  7.33x   8.58x  7.73x         1.00x    130.05 μs
    Dict with 256 lists of 256 dicts with 1 int 15.90x 14.53x  11.43x 10.09x         1.00x   1772.84 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: decode (Python 3.11.10)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.76x  5.07x   3.05x  1.58x         1.00x      1.46 μs
    List of 256 ASCII strings                    7.53x  8.05x   4.73x  4.44x         1.00x      2.88 μs
    List of 256 floats                          10.17x 11.10x   2.23x  1.71x         1.00x      5.89 μs
    List of 256 dicts with 1 int                11.14x 10.56x   6.73x  4.54x         1.00x      6.14 μs
    Medium complex object                       11.28x 10.64x   4.67x  3.67x         1.00x      8.38 μs
    List of 256 strings                          3.77x  2.70x   7.32x  5.18x         1.00x     22.81 μs
    Complex object                               9.12x  7.22x   8.44x  7.70x         1.00x    130.03 μs
    Dict with 256 lists of 256 dicts with 1 int 16.47x 14.35x  12.29x  9.09x         1.00x   1682.02 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: decode (Python 3.12.7)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.17x  4.79x   2.53x  1.27x         1.00x      1.60 μs
    List of 256 ASCII strings                    7.87x  8.34x   4.86x  4.46x         1.00x      2.97 μs
    List of 256 floats                           9.96x 10.23x   1.99x  1.53x         1.00x      6.69 μs
    List of 256 dicts with 1 int                12.30x 11.45x   6.94x  5.10x         1.00x      6.02 μs
    Medium complex object                       11.36x 11.39x   4.70x  3.90x         1.00x      8.48 μs
    List of 256 strings                          4.32x  2.90x   7.59x  5.82x         1.00x     21.81 μs
    Complex object                               9.17x  7.63x   8.86x  7.96x         1.00x    130.83 μs
    Dict with 256 lists of 256 dicts with 1 int 19.19x 15.57x  11.28x  9.74x         1.00x   1626.35 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.13.0

    .. only:: latex

        .. rubric:: decode (Python 3.13.0)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         5.62x  5.07x   3.59x  1.48x         1.00x      1.50 μs
    List of 256 ASCII strings                    7.01x  6.08x   3.69x  3.37x         1.00x      4.07 μs
    List of 256 floats                          10.84x 11.22x   2.25x  1.73x         1.00x      6.11 μs
    List of 256 dicts with 1 int                12.94x 11.52x   7.11x  5.16x         1.00x      6.12 μs
    Medium complex object                       13.06x 12.24x   5.27x  4.47x         1.00x      7.83 μs
    List of 256 strings                          6.80x  3.69x   9.48x  7.88x         1.00x     16.98 μs
    Complex object                               9.89x  7.84x   9.01x  8.00x         1.00x    130.54 μs
    Dict with 256 lists of 256 dicts with 1 int 18.73x 15.92x  11.58x  9.65x         1.00x   1624.49 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. warning:: The Python version of :mod:`jsonyx` is up to 7.01x slower for
    encoding and up to 52.84x slower for decoding, so make sure you have a
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
