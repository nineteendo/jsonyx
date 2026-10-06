Benchmark (Sep 30, 2026)
========================

We recommend to use :pypi:`orjson` or :pypi:`msgspec` or :pypi:`yyjson` for
performance critical applications:

.. tab:: Python 3.15.0

    .. only:: latex

        .. rubric:: encode (Python 3.15.0)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.20x  1.00x    1.64x    1.20x DNF [1]_    264.49 μs
        65,536 ASCII characters   31.93x 19.13x    3.29x    1.00x DNF [1]_      6.03 μs
        65,536 Unicode characters 26.71x 14.64x    3.29x    1.00x DNF [1]_     11.83 μs
        65,536 non-BMP characters 20.41x 12.13x    3.33x    1.00x DNF [1]_     23.24 μs
        65,536 nulls               5.39x  5.35x    1.15x    1.00x    2.20x    261.32 μs
        65,536 booleans            5.22x  5.03x    1.32x    1.00x    2.05x    283.87 μs
        65,536 empty strings       6.00x  5.60x    1.85x    1.00x    3.47x    295.92 μs
        65,536 ASCII keys          4.58x  4.41x    1.11x    1.00x    2.41x    958.28 μs
        65,536 fixed-point floats 14.30x 15.58x    1.00x    1.18x    1.85x    421.64 μs
        65,536 scientific floats  10.73x 11.14x    2.07x    1.03x    1.00x   1752.30 μs
        65,536 subnormal floats   25.19x 25.86x    1.11x    1.44x    1.00x   1433.06 μs
        65,536 31-bit integers     5.68x 11.18x    1.00x    1.12x    1.88x    349.85 μs
        65,536 32-bit integers     5.08x  7.75x    1.00x    2.69x    1.31x    761.52 μs
        65,536 63-bit integers     5.50x  8.27x    1.00x    2.87x    1.41x    714.54 μs
        65,536 64-bit integers     5.11x  6.62x    1.00x    2.24x    2.20x   1032.57 μs
        65,536 >64-bit integers    1.03x  1.63x    1.00x DNF [2]_    3.05x   4932.19 μs
        65,536 empty lists         7.01x 26.05x    1.00x    1.15x    1.67x    296.54 μs
        65,536 empty dictionaries  6.53x 25.92x    1.00x    1.26x    7.61x    294.85 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.14.7

    .. only:: latex

        .. rubric:: encode (Python 3.14.7)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.54x  1.00x    2.18x    1.44x DNF [1]_    225.71 μs
        65,536 ASCII characters   30.50x 17.10x    3.49x    1.00x DNF [1]_      6.00 μs
        65,536 Unicode characters 29.32x 15.27x    3.42x    1.00x DNF [1]_     11.83 μs
        65,536 non-BMP characters 24.41x  9.87x    3.58x    1.00x DNF [1]_     22.59 μs
        65,536 nulls               5.15x  4.62x    1.02x    1.00x    2.13x    264.22 μs
        65,536 booleans            5.14x  4.47x    1.18x    1.00x    2.03x    286.60 μs
        65,536 empty strings      12.97x  5.38x    1.59x    1.00x    3.45x    295.25 μs
        65,536 ASCII keys          7.24x  4.76x    1.21x    1.00x    2.47x    927.93 μs
        65,536 fixed-point floats 15.35x 16.43x    1.00x    1.15x    1.87x    421.49 μs
        65,536 scientific floats  12.06x 12.15x    1.99x    1.00x    1.01x   1730.87 μs
        65,536 subnormal floats   27.17x 27.32x    1.00x    1.47x    1.02x   1393.21 μs
        65,536 31-bit integers     6.93x 14.42x    1.00x    1.21x    2.39x    314.64 μs
        65,536 32-bit integers     6.50x 10.00x    1.00x    3.24x    1.68x    654.34 μs
        65,536 63-bit integers     6.54x 10.10x    1.00x    3.34x    1.70x    648.33 μs
        65,536 64-bit integers     5.75x  8.37x    1.00x    2.74x    3.03x    935.40 μs
        65,536 >64-bit integers    1.00x  1.43x    1.09x DNF [2]_    3.35x   5598.67 μs
        65,536 empty lists         7.24x 29.92x    1.00x    1.21x    1.58x    293.90 μs
        65,536 empty dictionaries  6.98x 33.23x    1.00x    1.34x    2.27x    263.01 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.13.15

    .. only:: latex

        .. rubric:: encode (Python 3.13.15)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.38x  1.00x    1.78x    1.33x DNF [1]_    238.08 μs
        65,536 ASCII characters   35.65x 19.09x    3.31x    1.00x DNF [1]_      6.04 μs
        65,536 Unicode characters 50.70x 16.91x    3.08x    1.00x DNF [1]_     14.49 μs
        65,536 non-BMP characters 26.00x 14.30x    3.52x    1.00x DNF [1]_     23.47 μs
        65,536 nulls               5.02x  5.01x    1.11x    1.00x    2.16x    270.94 μs
        65,536 booleans            4.88x  5.09x    1.19x    1.00x    2.11x    293.09 μs
        65,536 empty strings      12.33x  5.33x    1.74x    1.00x    3.27x    300.33 μs
        65,536 ASCII keys          6.86x  4.73x    1.23x    1.00x    2.39x    933.29 μs
        65,536 fixed-point floats 13.79x 14.85x    1.00x    1.11x    1.64x    444.04 μs
        65,536 scientific floats  11.99x 12.42x    2.46x    1.04x    1.00x   1671.10 μs
        65,536 subnormal floats   26.55x 27.01x    1.01x    1.51x    1.00x   1360.75 μs
        65,536 31-bit integers    13.09x 14.36x    1.00x    1.16x    2.08x    338.32 μs
        65,536 32-bit integers     8.80x  9.70x    1.00x    3.37x    1.61x    636.86 μs
        65,536 63-bit integers     8.81x  9.77x    1.00x    3.43x    1.60x    634.29 μs
        65,536 64-bit integers     6.64x  7.24x    1.00x    2.57x    2.82x    995.31 μs
        65,536 >64-bit integers    1.22x  1.32x    1.00x DNF [2]_    3.21x   5660.67 μs
        65,536 empty lists         7.91x 31.96x    1.00x    1.41x    1.72x    264.96 μs
        65,536 empty dictionaries  7.13x 34.17x    1.00x    1.35x    2.28x    278.28 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.12.10

    .. only:: latex

        .. rubric:: encode (Python 3.12.10)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.57x  1.00x    1.90x    1.32x DNF [1]_    239.93 μs
        65,536 ASCII characters   18.08x 11.87x    2.36x    1.00x DNF [1]_     10.26 μs
        65,536 Unicode characters 35.40x 19.65x    3.27x    1.00x DNF [1]_     12.00 μs
        65,536 non-BMP characters 23.09x 10.98x    3.51x    1.00x DNF [1]_     24.02 μs
        65,536 nulls               1.86x  1.92x    1.29x    1.00x    1.30x    633.77 μs
        65,536 booleans            5.26x  5.21x    1.17x    1.00x    2.16x    286.61 μs
        65,536 empty strings      10.00x  4.52x    1.31x    1.00x    2.74x    353.43 μs
        65,536 ASCII keys          6.97x  4.96x    1.27x    1.00x    2.67x    861.25 μs
        65,536 fixed-point floats 14.15x 16.25x    1.00x    1.14x    1.76x    414.14 μs
        65,536 scientific floats  11.40x 12.08x    1.89x    1.00x    1.03x   1788.81 μs
        65,536 subnormal floats   30.95x 28.23x    1.00x    1.52x    1.03x   1354.29 μs
        65,536 31-bit integers    14.46x 16.46x    1.08x    1.00x    2.23x    311.17 μs
        65,536 32-bit integers     9.12x 10.31x    1.00x    3.28x    1.62x    649.44 μs
        65,536 63-bit integers     9.64x 10.31x    1.00x    3.39x    1.80x    646.33 μs
        65,536 64-bit integers     7.02x  7.71x    1.00x    2.53x    2.70x   1010.60 μs
        65,536 >64-bit integers    1.15x  1.27x    1.00x DNF [2]_    3.02x   6284.11 μs
        65,536 empty lists         6.66x 28.81x    1.00x    1.13x    1.50x    286.06 μs
        65,536 empty dictionaries  6.19x 30.29x    1.00x    1.40x    2.16x    275.75 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.11.12

    .. only:: latex

        .. rubric:: encode (Python 3.11.12)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.77x  1.00x    2.21x    1.55x DNF [1]_    203.50 μs
        65,536 ASCII characters   45.79x 15.98x    3.78x    1.00x DNF [1]_      5.26 μs
        65,536 Unicode characters 29.80x 13.33x    3.27x    1.00x DNF [1]_     12.19 μs
        65,536 non-BMP characters 24.23x 11.46x    3.51x    1.00x DNF [1]_     23.26 μs
        65,536 nulls               9.62x  4.87x    1.23x    1.00x    2.39x    257.02 μs
        65,536 booleans            9.13x  4.70x    1.26x    1.00x    2.03x    276.26 μs
        65,536 empty strings      13.18x  5.18x    1.61x    1.00x    3.38x    298.69 μs
        65,536 ASCII keys         13.70x  4.84x    1.34x    1.00x    2.44x    890.27 μs
        65,536 fixed-point floats 13.77x 13.28x    1.00x    1.25x    1.71x    431.32 μs
        65,536 scientific floats  11.03x 11.15x    2.05x    1.05x    1.00x   1685.53 μs
        65,536 subnormal floats   25.96x 26.38x    1.00x    1.54x    1.03x   1356.37 μs
        65,536 31-bit integers    13.15x 12.71x    1.00x    2.32x    1.96x    367.11 μs
        65,536 32-bit integers     8.80x  8.39x    1.00x    2.98x    1.49x    707.53 μs
        65,536 63-bit integers     8.73x  8.36x    1.00x    3.02x    1.50x    707.56 μs
        65,536 64-bit integers     7.19x  6.94x    1.00x    2.44x    2.58x   1031.64 μs
        65,536 >64-bit integers    1.30x  1.25x    1.00x DNF [2]_    2.28x   5746.44 μs
        65,536 empty lists        12.63x 27.96x    1.00x    1.26x    1.80x    257.05 μs
        65,536 empty dictionaries 11.40x 27.55x    1.00x    1.25x    2.45x    270.92 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.10.17

    .. only:: latex

        .. rubric:: encode (Python 3.10.17)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ======== ======== ======== ============
        encode                      json jsonyx  msgspec   orjson   yyjson fastest time
        ========================= ====== ====== ======== ======== ======== ============
        65,536 control characters  1.20x  1.00x    1.88x    1.19x DNF [1]_    266.91 μs
        65,536 ASCII characters   34.20x 21.73x    3.73x    1.00x DNF [1]_      5.32 μs
        65,536 Unicode characters 26.04x 14.67x    3.36x    1.00x DNF [1]_     12.12 μs
        65,536 non-BMP characters 21.46x 11.40x    3.35x    1.00x DNF [1]_     23.25 μs
        65,536 nulls               8.93x  5.12x    1.02x    1.00x    2.70x    270.28 μs
        65,536 booleans            8.82x  5.20x    1.25x    1.00x    2.71x    270.88 μs
        65,536 empty strings      12.85x  5.57x    1.27x    1.00x    3.84x    291.55 μs
        65,536 ASCII keys         11.80x  5.36x    1.23x    1.00x    2.73x    980.01 μs
        65,536 fixed-point floats 13.86x 14.15x    1.00x    1.25x    1.96x    426.19 μs
        65,536 scientific floats  10.36x 10.49x    1.93x    1.00x    1.00x   1739.19 μs
        65,536 subnormal floats   25.27x 25.35x    1.01x    1.58x    1.00x   1334.49 μs
        65,536 31-bit integers    13.35x 13.41x    1.00x    2.32x    2.01x    360.17 μs
        65,536 32-bit integers     9.92x 10.27x    1.00x    3.30x    1.85x    642.34 μs
        65,536 63-bit integers     9.81x 10.20x    1.00x    3.32x    1.89x    648.86 μs
        65,536 64-bit integers     7.79x  8.24x    1.00x    2.49x    2.70x   1019.14 μs
        65,536 >64-bit integers    1.28x  1.31x    1.00x DNF [2]_    2.14x   6222.18 μs
        65,536 empty lists        12.33x 25.88x    1.00x    1.23x    1.83x    275.22 μs
        65,536 empty dictionaries 13.05x 26.40x    1.00x    1.20x    2.50x    269.11 μs
        ========================= ====== ====== ======== ======== ======== ============

.. tab:: Python 3.15.0
    :new-set:

    .. only:: latex

        .. rubric:: decode (Python 3.15.0)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  5.58x  3.73x        3.39x      1.01x      1.00x    252.06 μs
        65,536 ASCII characters    4.54x  3.69x        1.05x      1.00x      1.02x     22.21 μs
        65,536 Unicode characters  3.52x  3.27x        3.80x      1.19x      1.00x    247.51 μs
        65,536 non-BMP characters  2.95x  2.99x        2.82x      1.36x      1.00x    497.04 μs
        65,536 nulls               2.17x  2.96x        1.32x      1.00x      1.13x    534.66 μs
        65,536 booleans            2.32x  3.13x        1.43x      1.00x      1.24x    544.46 μs
        65,536 empty strings       2.92x  3.75x        1.80x      1.00x      1.61x    627.41 μs
        65,536 ASCII keys          1.71x  1.37x        1.14x      1.05x      1.00x   6179.19 μs
        65,536 fixed-point floats  3.25x  3.66x        1.34x      1.00x      1.13x   1677.02 μs
        65,536 scientific floats   3.15x  3.53x        1.20x      1.00x      1.04x   1977.94 μs
        65,536 subnormal floats   11.27x 11.63x 150.63x [3]_      1.00x      1.12x   2508.46 μs
        65,536 31-bit integers     5.61x  6.33x        1.74x      1.00x      1.45x    705.62 μs
        65,536 32-bit integers     3.42x  3.34x        1.28x      1.00x      1.09x   2026.58 μs
        65,536 63-bit integers     3.43x  3.34x        1.28x      1.00x      1.09x   2023.00 μs
        65,536 64-bit integers     3.54x  3.37x        1.26x      1.00x      1.00x   2553.79 μs
        65,536 >64-bit integers    2.96x  2.80x        2.67x 1.01x [4]_ 1.00x [4]_   3156.81 μs
        65,536 empty lists         1.38x  1.69x        1.17x      1.00x      1.05x   2336.05 μs
        65,536 empty dictionaries  1.41x  1.68x        1.22x      1.00x      1.04x   2407.44 μs
        ========================= ====== ====== ============ ========== ========== ============

.. tab:: Python 3.14.7

    .. only:: latex

        .. rubric:: decode (Python 3.14.7)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  4.46x  3.66x        3.38x      1.00x      1.02x    226.74 μs
        65,536 ASCII characters    4.86x  1.96x        1.00x      1.03x      1.03x     22.11 μs
        65,536 Unicode characters  3.91x  3.14x        3.48x      1.19x      1.00x    264.08 μs
        65,536 non-BMP characters  9.85x  4.67x        3.37x      1.49x      1.00x    533.10 μs
        65,536 nulls               2.41x  2.85x        1.27x      1.00x      1.12x    557.17 μs
        65,536 booleans            2.20x  2.79x        1.21x      1.00x      1.20x    564.83 μs
        65,536 empty strings       3.53x  3.29x        1.59x      1.00x      1.66x    684.02 μs
        65,536 ASCII keys          1.64x  1.19x        1.07x      1.05x      1.00x   7474.38 μs
        65,536 fixed-point floats  3.25x  3.50x        1.12x      1.00x      1.16x   1864.39 μs
        65,536 scientific floats   3.08x  3.34x        1.09x      1.00x      1.06x   2175.37 μs
        65,536 subnormal floats    9.79x 10.15x 135.96x [3]_      1.00x      1.10x   2803.95 μs
        65,536 31-bit integers     5.63x  6.13x        1.34x      1.00x      1.39x    734.49 μs
        65,536 32-bit integers     3.10x  2.99x        1.13x      1.00x      1.05x   2344.99 μs
        65,536 63-bit integers     3.09x  2.98x        1.12x      1.00x      1.04x   2353.03 μs
        65,536 64-bit integers     3.09x  2.97x        1.10x      1.01x      1.00x   2895.33 μs
        65,536 >64-bit integers    2.76x  2.64x        2.57x 1.00x [4]_ 1.01x [4]_   3375.14 μs
        65,536 empty lists         1.25x  1.49x        1.09x      1.00x      1.06x   2962.93 μs
        65,536 empty dictionaries  1.31x  1.57x        1.16x      1.00x      1.07x   2659.40 μs
        ========================= ====== ====== ============ ========== ========== ============

.. tab:: Python 3.13.15

    .. only:: latex

        .. rubric:: decode (Python 3.13.15)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  3.72x  3.50x        3.53x      1.00x      1.01x    227.70 μs
        65,536 ASCII characters    4.64x  3.19x        1.03x      1.10x      1.00x     22.49 μs
        65,536 Unicode characters  3.35x  3.09x        3.65x      1.23x      1.00x    253.73 μs
        65,536 non-BMP characters  2.97x  2.66x        2.76x      1.33x      1.00x    526.50 μs
        65,536 nulls               4.71x  4.09x        1.25x      1.00x      1.20x    586.23 μs
        65,536 booleans            2.59x  3.21x        1.25x      1.00x      1.21x    542.93 μs
        65,536 empty strings       3.54x  3.56x        1.84x      1.00x      1.80x    591.24 μs
        65,536 ASCII keys          1.60x  1.21x        1.09x      1.04x      1.00x   7301.99 μs
        65,536 fixed-point floats  3.24x  3.60x        1.19x      1.00x      1.16x   1770.80 μs
        65,536 scientific floats   2.98x  3.33x        1.04x      1.00x      1.03x   2169.76 μs
        65,536 subnormal floats   10.01x 10.35x 140.41x [3]_      1.00x      1.10x   2726.46 μs
        65,536 31-bit integers     6.58x  7.04x        1.41x      1.00x      1.39x    713.87 μs
        65,536 32-bit integers     3.09x  2.93x        1.15x      1.00x      1.06x   2241.38 μs
        65,536 63-bit integers     3.07x  2.91x        1.14x      1.00x      1.06x   2257.57 μs
        65,536 64-bit integers     3.26x  2.95x        1.12x      1.01x      1.00x   2768.16 μs
        65,536 >64-bit integers    2.81x  2.51x        2.48x 1.03x [4]_ 1.00x [4]_   3343.82 μs
        65,536 empty lists         1.49x  1.69x        1.18x      1.00x      1.07x   2522.42 μs
        65,536 empty dictionaries  1.51x  1.69x        1.19x      1.00x      1.08x   2585.46 μs
        ========================= ====== ====== ============ ========== ========== ============

.. tab:: Python 3.12.10

    .. only:: latex

        .. rubric:: decode (Python 3.12.10)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  2.90x  3.50x        3.22x      1.13x      1.00x    227.86 μs
        65,536 ASCII characters    4.73x  3.27x        1.00x      1.01x      1.03x     22.04 μs
        65,536 Unicode characters  2.66x  3.23x        4.16x      1.44x      1.00x    247.30 μs
        65,536 non-BMP characters  2.78x  2.88x        3.10x      1.21x      1.00x    495.49 μs
        65,536 nulls               2.36x  2.97x        1.32x      1.00x      1.35x    480.84 μs
        65,536 booleans            2.67x  3.87x        1.41x      1.00x      1.26x    541.29 μs
        65,536 empty strings       2.46x  2.92x        1.49x      1.00x      1.49x    756.74 μs
        65,536 ASCII keys          1.66x  1.21x        1.09x      1.01x      1.00x   7099.67 μs
        65,536 fixed-point floats  3.32x  3.66x        1.26x      1.00x      1.18x   1735.22 μs
        65,536 scientific floats   3.55x  3.86x        1.26x      1.00x      1.33x   1842.00 μs
        65,536 subnormal floats   10.44x 10.94x 144.94x [3]_      1.00x      1.16x   2637.02 μs
        65,536 31-bit integers     6.72x  7.38x        1.54x      1.00x      1.50x    648.12 μs
        65,536 32-bit integers     3.31x  3.10x        1.23x      1.00x      1.15x   2092.92 μs
        65,536 63-bit integers     3.42x  3.21x        1.26x      1.00x      1.20x   2045.10 μs
        65,536 64-bit integers     3.42x  2.98x        1.14x      1.00x      1.06x   2751.58 μs
        65,536 >64-bit integers    3.01x  2.62x        2.85x 1.00x [4]_ 1.04x [4]_   3224.49 μs
        65,536 empty lists         1.36x  1.81x        1.19x      1.00x      1.09x   2487.83 μs
        65,536 empty dictionaries  1.35x  1.65x        1.21x      1.00x      1.04x   2474.14 μs
        ========================= ====== ====== ============ ========== ========== ============

.. tab:: Python 3.11.12

    .. only:: latex

        .. rubric:: decode (Python 3.11.12)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  3.72x  3.56x        3.55x      1.12x      1.00x    230.74 μs
        65,536 ASCII characters    2.61x  1.84x        1.00x      1.02x      1.02x     21.97 μs
        65,536 Unicode characters  3.44x  3.30x        3.59x      1.42x      1.00x    249.04 μs
        65,536 non-BMP characters  3.16x  2.98x        2.94x      1.18x      1.00x    489.94 μs
        65,536 nulls               2.60x  3.01x        1.39x      1.00x      1.32x    490.03 μs
        65,536 booleans            2.70x  3.21x        1.35x      1.00x      1.26x    501.87 μs
        65,536 empty strings       2.99x  3.20x        1.56x      1.00x      1.51x    680.03 μs
        65,536 ASCII keys          1.62x  1.28x        1.12x      1.01x      1.00x   7196.88 μs
        65,536 fixed-point floats  3.74x  4.03x        1.39x      1.00x      1.18x   1351.04 μs
        65,536 scientific floats   3.28x  3.59x        1.15x      1.00x      1.05x   1762.21 μs
        65,536 subnormal floats   11.54x 11.80x 166.11x [3]_      1.00x      1.11x   2299.86 μs
        65,536 31-bit integers     6.45x  7.00x        1.65x      1.00x      1.51x    642.60 μs
        65,536 32-bit integers     3.19x  3.06x        1.19x      1.00x      1.09x   1899.09 μs
        65,536 63-bit integers     3.17x  3.07x        1.19x      1.00x      1.10x   1893.80 μs
        65,536 64-bit integers     2.93x  2.69x        1.13x      1.00x      1.03x   2822.15 μs
        65,536 >64-bit integers    3.13x  2.89x        2.88x 1.00x [4]_ 1.07x [4]_   2713.91 μs
        65,536 empty lists         1.43x  1.62x        1.15x      1.00x      1.06x   2327.10 μs
        65,536 empty dictionaries  1.38x  1.66x        1.16x      1.00x      1.03x   2057.13 μs
        ========================= ====== ====== ============ ========== ========== ============

.. tab:: Python 3.10.17

    .. only:: latex

        .. rubric:: decode (Python 3.10.17)

    .. table::
        :widths: grid
        :class: longtable

        ========================= ====== ====== ============ ========== ========== ============
        decode                      json jsonyx      msgspec     orjson     yyjson fastest time
        ========================= ====== ====== ============ ========== ========== ============
        65,536 control characters  2.82x  3.24x        3.04x      1.03x      1.00x    251.60 μs
        65,536 ASCII characters    4.17x  2.94x        1.00x      1.11x      1.00x     26.14 μs
        65,536 Unicode characters  2.95x  3.20x        3.73x      1.37x      1.00x    281.08 μs
        65,536 non-BMP characters  2.87x  2.90x        3.17x      1.17x      1.00x    492.81 μs
        65,536 nulls               2.33x  3.15x        1.55x      1.00x      1.58x    501.29 μs
        65,536 booleans            2.33x  3.15x        1.60x      1.00x      1.45x    516.88 μs
        65,536 empty strings       3.58x  4.26x        1.91x      1.00x      1.95x    601.92 μs
        65,536 ASCII keys          1.56x  1.36x        1.09x      1.05x      1.00x   7033.64 μs
        65,536 fixed-point floats  3.87x  4.26x        1.52x      1.00x      1.29x   1267.41 μs
        65,536 scientific floats   4.04x  4.37x        1.46x      1.00x      1.33x   1399.34 μs
        65,536 subnormal floats   11.72x 12.07x 181.49x [3]_      1.00x      1.22x   2100.83 μs
        65,536 31-bit integers     6.24x  6.97x        1.78x      1.00x      1.62x    621.01 μs
        65,536 32-bit integers     3.28x  3.48x        1.43x      1.00x      1.22x   1710.41 μs
        65,536 63-bit integers     3.27x  3.48x        1.42x      1.00x      1.24x   1713.59 μs
        65,536 64-bit integers     2.99x  3.07x        1.22x      1.00x      1.03x   2381.40 μs
        65,536 >64-bit integers    2.77x  2.83x        2.83x 1.00x [4]_ 1.16x [4]_   2642.02 μs
        65,536 empty lists         1.42x  1.77x        1.27x      1.00x      1.17x   2258.97 μs
        65,536 empty dictionaries  1.56x  1.97x        1.33x      1.00x      1.21x   1795.75 μs
        ========================= ====== ====== ============ ========== ========== ============

.. warning:: The Python version of :mod:`jsonyx` is up to 82.11x slower for
    encoding and up to 92.54x slower for decoding, so make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installed on
    Windows.

.. rubric:: Footnotes

.. [1] tried to deserialize
.. [2] integer exceeds 64-bit range
.. [3] see :issue:`msgspec/msgspec#1232`
.. [4] converted to a float