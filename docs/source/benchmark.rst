Benchmark (Apr 30, 2025)
========================

We recommend to use :pypi:`orjson`, :pypi:`msgspec` or :pypi:`pysimdjson` for
performance critical applications:

.. tab:: Python 3.13.0

    .. only:: latex

        .. rubric:: encode (Python 3.13.0)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.62x  4.17x   1.06x    1.00x      1.82 μs
    List of 256 ASCII strings                   14.09x  8.10x   1.66x    1.00x      3.66 μs
    List of 256 floats                          25.20x 25.18x   1.33x    1.00x      8.07 μs
    List of 256 dicts with 1 int                11.24x  9.89x   1.34x    1.00x      7.87 μs
    Medium complex object                       10.21x  8.85x   1.17x    1.00x     13.87 μs
    List of 256 strings                         26.46x 15.18x   2.23x    1.00x     13.37 μs
    Complex object                               7.86x  7.41x   1.00x DNF [1]_    207.83 μs
    Dict with 256 lists of 256 dicts with 1 int  9.87x  8.72x   1.24x    1.00x   2295.24 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: encode (Python 3.12.7)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         4.57x  3.99x   1.00x    1.06x      1.91 μs
    List of 256 ASCII strings                   10.98x  6.89x   1.38x    1.00x      4.27 μs
    List of 256 floats                          23.85x 23.59x   1.35x    1.00x      8.04 μs
    List of 256 dicts with 1 int                10.75x  9.66x   1.25x    1.00x      8.23 μs
    Medium complex object                        9.89x  8.93x   1.12x    1.00x     13.77 μs
    List of 256 strings                         20.65x 11.83x   1.83x    1.00x     16.02 μs
    Complex object                               7.26x  7.34x   1.00x DNF [1]_    210.00 μs
    Dict with 256 lists of 256 dicts with 1 int  9.51x  9.02x   1.22x    1.00x   2381.95 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: encode (Python 3.11.10)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.14x  3.71x   1.00x    1.01x      1.90 μs
    List of 256 ASCII strings                   15.50x  8.85x   1.61x    1.00x      3.56 μs
    List of 256 floats                          23.09x 22.28x   1.26x    1.00x      8.04 μs
    List of 256 dicts with 1 int                14.50x  9.35x   1.36x    1.00x      7.75 μs
    Medium complex object                       11.33x  8.35x   1.15x    1.00x     13.35 μs
    List of 256 strings                         22.60x 11.32x   2.24x    1.00x     15.51 μs
    Complex object                               8.25x  6.92x   1.00x DNF [1]_    209.85 μs
    Dict with 256 lists of 256 dicts with 1 int 13.66x  7.91x   1.23x    1.00x   2364.31 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: encode (Python 3.10.15)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         6.26x  4.12x   1.00x    1.03x      1.88 μs
    List of 256 ASCII strings                   11.68x  8.62x   1.46x    1.00x      4.06 μs
    List of 256 floats                          22.07x 22.12x   1.25x    1.00x      8.22 μs
    List of 256 dicts with 1 int                13.21x  8.93x   1.32x    1.00x      8.23 μs
    Medium complex object                       10.62x  8.20x   1.18x    1.00x     13.99 μs
    List of 256 strings                         24.94x 13.48x   2.09x    1.00x     14.21 μs
    Complex object                               8.12x  6.90x   1.00x DNF [1]_    215.91 μs
    Dict with 256 lists of 256 dicts with 1 int 12.15x  8.06x   1.18x    1.00x   2585.56 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.9.20

    .. only:: latex

        .. rubric:: encode (Python 3.9.20)

    .. tabularcolumns:: lrrrrr

    =========================================== ====== ====== ======= ======== ============
    encode                                        json jsonyx msgspec   orjson fastest time
    =========================================== ====== ====== ======= ======== ============
    List of 256 booleans                         7.51x  4.63x   1.01x    1.00x      1.67 μs
    List of 256 ASCII strings                   11.36x  8.94x   1.53x    1.00x      3.76 μs
    List of 256 floats                          23.27x 22.77x   1.35x    1.00x      8.03 μs
    List of 256 dicts with 1 int                13.68x  8.89x   1.26x    1.00x      8.06 μs
    Medium complex object                       10.91x  8.41x   1.08x    1.00x     13.98 μs
    List of 256 strings                         21.19x 11.98x   2.13x    1.00x     15.38 μs
    Complex object                               7.60x  7.02x   1.00x DNF [1]_    210.12 μs
    Dict with 256 lists of 256 dicts with 1 int 12.34x  7.56x   1.16x    1.00x   2519.36 μs
    =========================================== ====== ====== ======= ======== ============

.. tab:: Python 3.13.0
    :new-set:

    .. only:: latex

        .. rubric:: decode (Python 3.13.0)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.70x  5.22x   2.92x  1.41x         1.00x      1.45 μs
    List of 256 ASCII strings                    9.04x  7.05x   4.85x  4.43x         1.00x      3.15 μs
    List of 256 floats                          10.91x 11.22x   2.24x  1.73x         1.00x      6.14 μs
    List of 256 dicts with 1 int                12.99x 11.65x   7.35x  5.30x         1.00x      6.11 μs
    Medium complex object                       13.41x 12.94x   5.44x  4.67x         1.00x      7.65 μs
    List of 256 strings                          6.85x  3.75x   9.56x  7.85x         1.00x     16.78 μs
    Complex object                               9.36x  7.63x   8.55x  7.67x         1.00x    136.11 μs
    Dict with 256 lists of 256 dicts with 1 int 19.03x 15.62x  11.58x  9.87x         1.00x   1640.77 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.12.7

    .. only:: latex

        .. rubric:: decode (Python 3.12.7)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.25x  4.76x   2.64x  1.26x         1.00x      1.57 μs
    List of 256 ASCII strings                    7.44x  7.04x   4.98x  4.57x         1.00x      2.91 μs
    List of 256 floats                          10.41x 10.29x   2.02x  1.52x         1.00x      6.66 μs
    List of 256 dicts with 1 int                12.29x 11.26x   7.19x  5.24x         1.00x      6.02 μs
    Medium complex object                       12.12x 11.74x   4.84x  4.09x         1.00x      8.00 μs
    List of 256 strings                          5.36x  3.59x   9.36x  7.26x         1.00x     17.53 μs
    Complex object                               8.70x  7.38x   8.43x  7.65x         1.00x    136.18 μs
    Dict with 256 lists of 256 dicts with 1 int 17.61x 15.44x  11.45x  9.84x         1.00x   1647.79 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.11.10

    .. only:: latex

        .. rubric:: decode (Python 3.11.10)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.77x  5.19x   3.00x  1.57x         1.00x      1.46 μs
    List of 256 ASCII strings                    7.55x  8.52x   4.69x  4.49x         1.00x      2.83 μs
    List of 256 floats                          10.08x 10.95x   2.22x  1.70x         1.00x      5.94 μs
    List of 256 dicts with 1 int                10.83x 10.31x   6.27x  4.52x         1.00x      6.17 μs
    Medium complex object                       11.92x 11.56x   4.91x  3.92x         1.00x      7.90 μs
    List of 256 strings                          4.04x  2.87x   7.65x  5.58x         1.00x     21.49 μs
    Complex object                               9.10x  7.38x   8.51x  7.84x         1.00x    128.91 μs
    Dict with 256 lists of 256 dicts with 1 int 17.45x 15.26x  11.81x  9.74x         1.00x   1602.67 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.10.15

    .. only:: latex

        .. rubric:: decode (Python 3.10.15)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         4.46x  5.23x   3.30x  1.59x         1.00x      1.39 μs
    List of 256 ASCII strings                    9.39x  5.60x   4.33x  4.05x         1.00x      3.30 μs
    List of 256 floats                           9.68x  9.14x   2.14x  1.63x         1.00x      6.14 μs
    List of 256 dicts with 1 int                10.25x  9.64x   6.93x  5.62x         1.00x      7.03 μs
    Medium complex object                       13.11x 10.90x   4.80x  4.00x         1.00x      8.19 μs
    List of 256 strings                          4.77x  3.20x   7.17x  6.34x         1.00x     19.28 μs
    Complex object                               8.16x  8.01x   8.57x  7.70x         1.00x    131.47 μs
    Dict with 256 lists of 256 dicts with 1 int 17.06x 15.47x  12.44x 10.46x         1.00x   1643.52 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. tab:: Python 3.9.20

    .. only:: latex

        .. rubric:: decode (Python 3.9.20)

    .. tabularcolumns:: lrrrrrr

    =========================================== ====== ====== ======= ====== ============= ============
    decode                                        json jsonyx msgspec orjson simdjson [2]_ fastest time
    =========================================== ====== ====== ======= ====== ============= ============
    List of 256 booleans                         3.95x  4.71x   2.33x  1.41x         1.00x      1.55 μs
    List of 256 ASCII strings                   10.23x  7.18x   4.42x  4.29x         1.00x      2.94 μs
    List of 256 floats                           8.53x  7.72x   1.75x  1.23x         1.00x      7.14 μs
    List of 256 dicts with 1 int                11.40x 10.61x   6.14x  4.26x         1.00x      6.23 μs
    Medium complex object                       11.20x 11.02x   4.34x  3.84x         1.00x      8.20 μs
    List of 256 strings                         10.64x  4.34x  10.13x  8.59x         1.00x     17.99 μs
    Complex object                               8.86x  7.89x   9.05x  7.80x         1.00x    133.17 μs
    Dict with 256 lists of 256 dicts with 1 int 18.23x 16.57x  13.60x 12.13x         1.00x   1662.84 μs
    =========================================== ====== ====== ======= ====== ============= ============

.. warning:: The Python version of :mod:`jsonyx` is up to 8.03x slower for
    encoding and up to 46.71x slower for decoding, so make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.

.. rubric:: Footnotes

.. [1] failed due to recursion error
.. [2] delays creation of Python objects until they are accessed