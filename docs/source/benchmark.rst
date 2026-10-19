Benchmark (Oct 19, 2026)
========================

Benchmark code: https://github.com/nineteendo/jsonyx/blob/main/bench/__main__.py

We recommend to use :pypi:`orjson` or :pypi:`msgspec` or :pypi:`fastsimdjson`
for performance critical applications:

.. tab:: Python 3.15.0

    .. only:: latex

        .. rubric:: encode (Python 3.15.0)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         6.72x  4.07x        1.26x     1.00x    1.18x      0.39 ns
        8-bit character         2.14x  1.12x        1.08x     1.00x    1.06x      2.47 ns
        11-bit character        2.62x  1.26x        1.08x     1.00x    1.06x      2.40 ns
        16-bit character        1.57x  1.01x        1.05x     1.00x    1.04x      4.01 ns
        21-bit character        2.23x  1.00x        1.09x     1.01x    1.07x      4.76 ns
        7-in-16-bit character   3.03x  2.34x        1.09x     1.00x    1.09x      1.05 ns
        7-in-32-bit character   2.44x  2.04x        1.04x     1.00x    1.03x      1.70 ns
        11-in-32-bit character  2.63x  1.37x        1.08x     1.00x    1.07x      2.68 ns
        16-in-32-bit character  1.77x  1.12x        1.07x     1.00x    1.07x      3.99 ns
        double quote escape     1.24x  1.00x        1.93x     1.66x    1.66x      3.04 ns
        backslash escape        1.12x  1.00x        1.88x     1.59x    1.59x      3.16 ns
        character escape        1.11x  1.00x        1.99x     1.70x    1.73x      2.96 ns
        7-bit escape            1.02x  1.00x        1.06x     1.46x    1.03x      5.18 ns
        null                    5.23x  5.21x        1.00x     1.35x    1.15x      4.39 ns
        boolean                 4.75x  4.90x        1.00x     1.32x    1.01x      5.58 ns
        empty string            5.46x  5.97x        1.51x     1.83x    1.00x      4.93 ns
        fixed-point float      12.68x 14.10x        1.32x     1.00x    1.11x      7.32 ns
        scientific float       13.05x 13.47x        1.12x     1.81x    1.00x     29.43 ns
        minimum float          25.71x 26.07x        1.07x     1.00x    1.33x     24.83 ns
        maximum float          79.89x 80.30x        1.00x     1.28x    1.03x     30.29 ns
        32-bit (+) integer      5.23x  5.44x        1.14x     1.04x    1.00x      5.95 ns
        32-bit (-) integer      5.39x  5.59x        1.14x     1.02x    1.00x      5.94 ns
        64-bit (+) integer      4.77x  4.96x        1.41x     1.00x    2.64x     13.54 ns
        64-bit (-) integer      4.38x  4.39x        1.29x     1.00x    2.48x     14.75 ns
        >64-bit (+) integer     1.00x  1.03x     DNF [1]_     1.09x DNF [1]_     86.16 ns
        >64-bit (-) integer     1.06x  1.00x     DNF [1]_     1.05x DNF [1]_     89.78 ns
        empty list              5.97x  7.46x        1.35x     1.00x    1.03x      5.41 ns
        non-empty list         11.65x  4.42x        1.00x     1.24x    1.14x     11.68 ns
        empty dictionary        5.98x  7.89x        1.38x     1.00x    1.11x      5.01 ns
        non-empty dictionary    8.40x  4.01x        1.15x     1.31x    1.00x     20.44 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.14.8

    .. only:: latex

        .. rubric:: encode (Python 3.14.8)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         7.78x  4.79x        1.19x     1.00x    1.22x      0.39 ns
        8-bit character         2.73x  1.08x        1.07x     1.00x    1.06x      2.39 ns
        11-bit character        3.14x  1.35x        1.07x     1.00x    1.06x      2.42 ns
        16-bit character        1.91x  1.07x        1.06x     1.00x    1.06x      3.97 ns
        21-bit character        2.58x  1.00x        1.09x     1.02x    1.08x      4.27 ns
        7-in-16-bit character   3.53x  2.57x        1.08x     1.00x    1.10x      1.05 ns
        7-in-32-bit character   2.52x  2.01x        1.04x     1.00x    1.04x      1.69 ns
        11-in-32-bit character  3.46x  1.40x        1.05x     1.00x    1.07x      2.28 ns
        16-in-32-bit character  2.17x  1.10x        1.06x     1.00x    1.07x      3.62 ns
        double quote escape     1.00x  1.07x        1.64x     1.46x    1.54x      3.29 ns
        backslash escape        1.28x  1.00x        1.70x     1.56x    1.53x      3.29 ns
        character escape        1.19x  1.00x        1.65x     1.48x    1.53x      3.27 ns
        7-bit escape            1.30x  1.10x        1.00x     1.79x    1.05x      5.02 ns
        null                    5.03x  4.85x        1.01x     1.05x    1.00x      5.12 ns
        boolean                 4.92x  4.62x        1.10x     1.20x    1.00x      5.70 ns
        empty string            9.95x  4.97x        1.16x     1.45x    1.00x      5.89 ns
        fixed-point float      14.95x 15.85x        1.26x     1.15x    1.00x      8.17 ns
        scientific float       13.52x 11.77x        1.17x     1.90x    1.00x     28.62 ns
        minimum float          26.27x 26.63x        1.20x     1.00x    1.43x     23.13 ns
        maximum float          66.23x 66.84x        1.00x     1.25x    1.03x     30.40 ns
        32-bit (+) integer      6.32x  6.44x        1.17x     1.00x    1.09x      5.43 ns
        32-bit (-) integer      6.37x  6.53x        1.20x     1.00x    1.10x      5.41 ns
        64-bit (+) integer      5.83x  5.76x        1.60x     1.00x    2.78x     12.93 ns
        64-bit (-) integer      5.66x  5.59x        1.56x     1.00x    2.70x     13.44 ns
        >64-bit (+) integer     1.00x  1.02x     DNF [1]_     1.11x DNF [1]_     98.87 ns
        >64-bit (-) integer     1.02x  1.00x     DNF [1]_     1.05x DNF [1]_    104.98 ns
        empty list              6.60x  7.55x        1.38x     1.00x    1.08x      5.18 ns
        non-empty list         10.84x  3.80x        1.03x     1.04x    1.00x     13.25 ns
        empty dictionary        6.35x  8.15x        1.44x     1.00x    1.14x      4.92 ns
        non-empty dictionary   11.38x  4.44x        1.16x     1.39x    1.00x     19.49 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.13.16

    .. only:: latex

        .. rubric:: encode (Python 3.13.16)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         8.78x  4.78x        1.19x     1.00x    1.21x      0.39 ns
        8-bit character         3.22x  1.69x        1.08x     1.00x    1.12x      1.93 ns
        11-bit character        2.71x  1.36x        1.06x     1.00x    1.06x      2.42 ns
        16-bit character        1.66x  1.09x        1.06x     1.00x    1.05x      3.95 ns
        21-bit character        2.00x  1.00x        1.07x     1.01x    1.07x      5.23 ns
        7-in-16-bit character   3.07x  2.24x        1.06x     1.00x    1.08x      1.34 ns
        7-in-32-bit character   2.61x  1.90x        1.03x     1.00x    1.03x      1.94 ns
        11-in-32-bit character  3.35x  1.46x        1.09x     1.00x    1.09x      2.21 ns
        16-in-32-bit character  1.58x  1.10x        1.06x     1.00x    1.06x      4.70 ns
        double quote escape     1.23x  1.00x        1.54x     1.53x    1.43x      3.51 ns
        backslash escape        1.40x  1.00x        1.70x     1.64x    1.54x      3.26 ns
        character escape        1.34x  1.00x        1.65x     1.53x    1.53x      3.28 ns
        7-bit escape            1.24x  1.11x        1.00x     1.60x    1.05x      5.04 ns
        null                    5.91x  5.28x        1.00x     1.28x    1.13x      4.48 ns
        boolean                 4.60x  4.39x        1.03x     1.27x    1.00x      5.65 ns
        empty string           11.14x  5.53x        1.40x     1.76x    1.00x      4.93 ns
        fixed-point float      12.32x 13.28x        1.32x     1.00x    1.05x      7.70 ns
        scientific float       10.75x 11.01x        1.19x     1.91x    1.00x     28.48 ns
        minimum float          24.14x 24.66x        1.23x     1.00x    1.46x     22.61 ns
        maximum float          71.24x 71.06x        1.00x     1.22x    1.01x     30.42 ns
        32-bit (+) integer     11.08x 12.52x        1.09x     1.00x    1.04x      5.71 ns
        32-bit (-) integer     11.47x 12.84x        1.12x     1.00x    1.06x      5.57 ns
        64-bit (+) integer      6.79x  7.49x        1.50x     1.00x    2.77x     13.01 ns
        64-bit (-) integer      6.80x  7.28x        1.44x     1.00x    2.66x     13.83 ns
        >64-bit (+) integer     1.29x  1.37x     DNF [1]_     1.00x DNF [1]_     92.83 ns
        >64-bit (-) integer     1.34x  1.41x     DNF [1]_     1.00x DNF [1]_     90.12 ns
        empty list              7.00x  7.87x        1.63x     1.00x    1.16x      4.78 ns
        non-empty list          9.42x  3.63x        1.00x     1.06x    1.02x     14.93 ns
        empty dictionary        9.01x  7.28x        1.36x     1.00x    1.08x      5.18 ns
        non-empty dictionary   11.33x  3.99x        1.08x     1.34x    1.00x     20.94 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.12.15

    .. only:: latex

        .. rubric:: encode (Python 3.12.15)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         7.94x  4.78x        1.19x     1.00x    1.16x      0.39 ns
        8-bit character         3.16x  1.27x        1.05x     1.00x    1.05x      2.21 ns
        11-bit character        2.62x  1.29x        1.06x     1.00x    1.06x      3.04 ns
        16-bit character        2.24x  1.08x        1.05x     1.00x    1.08x      3.55 ns
        21-bit character        2.31x  1.00x        1.08x     1.00x    1.08x      4.78 ns
        7-in-16-bit character   2.39x  1.84x        1.33x     1.00x    1.08x      1.64 ns
        7-in-32-bit character   2.27x  1.84x        1.03x     1.12x    1.00x      1.99 ns
        11-in-32-bit character  2.84x  1.34x        1.07x     1.00x    1.07x      2.94 ns
        16-in-32-bit character  2.08x  1.12x        1.06x     1.00x    1.07x      3.99 ns
        double quote escape     1.12x  1.00x        1.56x     1.36x    1.45x      3.52 ns
        backslash escape        1.29x  1.00x        1.70x     1.61x    1.55x      3.27 ns
        character escape        1.33x  1.00x        1.66x     1.48x    1.54x      3.27 ns
        7-bit escape            1.38x  1.11x        1.00x     1.59x    1.05x      5.05 ns
        null                    4.82x  5.24x        1.00x     1.15x    1.10x      4.44 ns
        boolean                 4.08x  4.77x        1.16x     1.29x    1.00x      5.43 ns
        empty string           10.59x  5.50x        1.36x     1.53x    1.00x      4.91 ns
        fixed-point float      11.77x 13.41x        1.40x     1.00x    1.05x      7.55 ns
        scientific float       10.68x 11.65x        1.19x     1.87x    1.00x     28.50 ns
        minimum float          23.84x 24.31x        1.22x     1.00x    1.45x     22.69 ns
        maximum float          68.42x 68.93x        1.00x     1.22x    1.02x     30.20 ns
        32-bit (+) integer     13.94x 16.49x        1.29x     1.28x    1.00x      4.80 ns
        32-bit (-) integer     13.95x 16.44x        1.27x     1.18x    1.00x      4.82 ns
        64-bit (+) integer      7.44x  8.50x        1.45x     1.00x    2.79x     12.86 ns
        64-bit (-) integer      6.76x  7.69x        1.31x     1.00x    2.67x     14.15 ns
        >64-bit (+) integer     1.00x  1.73x     DNF [1]_     1.05x DNF [1]_    130.69 ns
        >64-bit (-) integer     1.19x  1.36x     DNF [1]_     1.00x DNF [1]_    111.96 ns
        empty list              7.03x  7.86x        1.52x     1.00x    1.09x      5.39 ns
        non-empty list         12.33x  4.79x        1.41x     1.35x    1.00x     11.17 ns
        empty dictionary        5.84x  7.63x        1.41x     1.00x    1.30x      4.90 ns
        non-empty dictionary   10.38x  4.41x        1.11x     1.43x    1.00x     18.70 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.11.17

    .. only:: latex

        .. rubric:: encode (Python 3.11.17)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         9.37x  5.29x        1.20x     1.00x    1.18x      0.39 ns
        8-bit character         3.47x  1.46x        1.08x     1.00x    1.08x      2.14 ns
        11-bit character        3.10x  1.33x        1.07x     1.00x    1.06x      2.64 ns
        16-bit character        2.07x  1.08x        1.06x     1.00x    1.06x      3.95 ns
        21-bit character        2.35x  1.04x        1.07x     1.00x    1.06x      5.07 ns
        7-in-16-bit character   4.37x  2.59x        1.08x     1.00x    1.09x      1.05 ns
        7-in-32-bit character   3.13x  2.02x        1.04x     1.00x    1.04x      1.69 ns
        11-in-32-bit character  2.71x  1.40x        1.06x     1.00x    1.07x      3.16 ns
        16-in-32-bit character  2.11x  1.16x        1.04x     1.00x    1.05x      4.05 ns
        double quote escape     1.35x  1.00x        1.68x     1.48x    1.53x      3.27 ns
        backslash escape        1.48x  1.00x        1.71x     1.59x    1.55x      3.27 ns
        character escape        1.12x  1.00x        1.50x     1.31x    1.38x      3.65 ns
        7-bit escape            1.43x  1.20x        1.00x     1.68x    1.02x      5.16 ns
        null                   10.79x  4.95x        1.00x     1.38x    1.09x      4.47 ns
        boolean                 9.30x  4.20x        1.02x     1.33x    1.00x      5.45 ns
        empty string           16.04x  5.27x        1.52x     1.70x    1.00x      4.87 ns
        fixed-point float      14.83x 12.12x        1.25x     1.00x    1.11x      7.71 ns
        scientific float       10.57x 10.28x        1.18x     1.93x    1.00x     28.33 ns
        minimum float          26.57x 26.35x        1.21x     1.00x    1.49x     22.28 ns
        maximum float          66.91x 66.90x        1.00x     1.25x    1.04x     29.71 ns
        32-bit (+) integer     15.24x 11.54x        1.72x     1.00x    2.12x      6.24 ns
        32-bit (-) integer     16.11x 11.95x        1.83x     1.00x    2.23x      6.03 ns
        64-bit (+) integer      8.51x  7.09x        1.35x     1.00x    2.44x     14.34 ns
        64-bit (-) integer      7.73x  6.13x        1.25x     1.00x    2.29x     15.69 ns
        >64-bit (+) integer     1.59x  1.35x     DNF [1]_     1.00x DNF [1]_     90.55 ns
        >64-bit (-) integer     1.55x  1.30x     DNF [1]_     1.00x DNF [1]_     93.31 ns
        empty list             11.33x  7.48x        1.54x     1.00x    1.06x      4.82 ns
        non-empty list         15.41x  4.60x        1.00x     1.35x    1.05x     11.24 ns
        empty dictionary       10.31x  7.00x        1.33x     1.00x    1.03x      5.18 ns
        non-empty dictionary   17.22x  4.37x        1.19x     1.41x    1.00x     18.97 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.10.22

    .. only:: latex

        .. rubric:: encode (Python 3.10.22)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ========= ======== ============
        encode                   json jsonyx fastsimdjson   msgspec   orjson fastest time
        ====================== ====== ====== ============ ========= ======== ============
        7-bit character         8.39x  4.78x        1.19x     1.00x    1.19x      0.38 ns
        8-bit character         2.41x  1.22x        1.07x     1.00x    1.06x      2.29 ns
        11-bit character        2.57x  1.49x        1.07x     1.00x    1.06x      2.64 ns
        16-bit character        1.65x  1.16x        1.05x     1.00x    1.04x      4.09 ns
        21-bit character        1.95x  1.00x        1.08x     1.02x    1.08x      5.00 ns
        7-in-16-bit character   3.93x  2.87x        1.08x     1.00x    1.08x      1.12 ns
        7-in-32-bit character   2.31x  1.88x        1.03x     1.00x    1.03x      1.94 ns
        11-in-32-bit character  2.08x  1.31x        1.05x     1.00x    1.07x      3.16 ns
        16-in-32-bit character  1.65x  1.11x        1.07x     1.00x    1.06x      4.00 ns
        double quote escape     1.00x  1.01x        1.60x     1.45x    1.45x      3.46 ns
        backslash escape        1.20x  1.00x        1.72x     1.54x    1.54x      3.26 ns
        character escape        1.00x  1.05x        1.77x     1.62x    1.62x      3.12 ns
        7-bit escape            1.06x  1.07x        1.00x     1.65x    1.02x      5.18 ns
        null                   10.08x  5.44x        1.00x     1.31x    1.13x      4.34 ns
        boolean                 8.28x  4.28x        1.02x     1.28x    1.00x      5.47 ns
        empty string           15.68x  5.56x        1.28x     1.34x    1.00x      4.92 ns
        fixed-point float      13.90x 12.39x        1.28x     1.00x    1.10x      7.81 ns
        scientific float        9.92x  9.73x        1.17x     1.86x    1.00x     28.54 ns
        minimum float          23.34x 22.90x        1.20x     1.00x    1.45x     22.96 ns
        maximum float          70.28x 70.30x        1.00x     1.24x    1.04x     29.76 ns
        32-bit (+) integer     15.56x 12.82x        1.72x     1.00x    2.31x      5.85 ns
        32-bit (-) integer     15.34x 12.33x        1.65x     1.00x    2.26x      6.03 ns
        64-bit (+) integer      8.24x  7.18x        1.48x     1.00x    2.58x     13.75 ns
        64-bit (-) integer      8.03x  6.89x        1.45x     1.00x    2.51x     14.41 ns
        >64-bit (+) integer     1.46x  1.38x     DNF [1]_     1.00x DNF [1]_     89.52 ns
        >64-bit (-) integer     1.60x  1.36x     DNF [1]_     1.00x DNF [1]_     90.99 ns
        empty list             10.74x  7.19x        1.19x     1.01x    1.00x      5.09 ns
        non-empty list         12.73x  4.43x        1.05x     1.13x    1.00x     11.88 ns
        empty dictionary       10.30x  7.79x        1.21x     1.00x    1.06x      5.06 ns
        non-empty dictionary   15.41x  4.24x        1.10x     1.32x    1.00x     19.65 ns
        ====================== ====== ====== ============ ========= ======== ============

.. tab:: Python 3.15.0
    :new-set:

    .. only:: latex

        .. rubric:: decode (Python 3.15.0)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ============ ========== ============
        decode                   json jsonyx fastsimdjson      msgspec     orjson fastest time
        ====================== ====== ====== ============ ============ ========== ============
        outer space            28.81x  9.67x        1.00x        5.48x      8.15x      0.10 ns
        inner space             7.22x  9.54x        1.00x        4.87x      6.34x      0.10 ns
        7-bit character         3.72x  1.81x        1.01x        1.00x      2.02x      0.50 ns
        8-bit character         1.39x  1.00x        1.29x        1.06x      1.09x      2.50 ns
        11-bit character        1.54x  1.19x        1.14x        1.00x      1.03x      2.72 ns
        16-bit character        1.44x  1.19x        1.22x        1.01x      1.00x      3.85 ns
        21-bit character        1.61x  1.40x        1.57x        1.11x      1.00x      4.48 ns
        7-in-16-bit character   3.33x  2.35x        1.59x        1.00x      1.45x      0.97 ns
        7-in-32-bit character   2.47x  1.86x        1.13x        1.41x      1.00x      1.58 ns
        11-in-32-bit character  1.91x  1.60x        1.10x        1.12x      1.00x      2.96 ns
        16-in-32-bit character  1.85x  1.61x        1.19x        1.13x      1.00x      3.96 ns
        utf-8-sig character     3.64x  1.77x        1.00x        1.42x      2.33x      0.52 ns
        utf-16le character      1.56x  1.00x        3.06x        2.77x      2.75x      1.74 ns
        utf-16be character      1.51x  1.00x        2.82x        2.62x      2.61x      1.89 ns
        utf-32le character      1.27x  1.00x        3.48x        2.90x      2.70x      3.51 ns
        utf-32be character      1.23x  1.00x        3.13x        2.64x      2.44x      4.07 ns
        double quote escape     2.50x  2.26x        1.86x        2.41x      1.00x      2.91 ns
        backslash escape        2.30x  2.07x        1.71x        2.21x      1.00x      3.17 ns
        character escape        2.41x  2.08x        1.75x        2.22x      1.00x      3.16 ns
        7-bit escape            4.00x  3.93x        1.00x        3.42x      1.80x      3.60 ns
        8-bit escape            2.45x  2.42x        1.00x        2.50x      1.26x      5.85 ns
        11-bit escape           2.53x  2.57x        1.00x        2.54x      1.29x      5.79 ns
        16-bit escape           1.93x  1.96x        1.00x        2.19x      1.13x      7.58 ns
        21-bit escape           2.10x  2.16x        1.00x        1.93x      1.23x     12.07 ns
        null                    2.39x  2.84x        1.00x        1.40x      1.70x      9.01 ns
        boolean                 2.21x  2.75x        1.00x        1.41x      1.56x      9.83 ns
        empty string            2.47x  2.99x        1.00x        1.67x      1.27x     12.35 ns
        fixed-point float       2.64x  2.09x        1.14x        1.27x      1.00x     37.06 ns
        scientific float        2.82x  2.31x        1.08x        1.21x      1.00x     39.16 ns
        minimum float           9.29x  8.82x        1.00x 124.77x [2]_      1.08x     45.95 ns
        <minimum float         13.54x 13.03x        1.00x 151.55x [2]_      1.08x     45.02 ns
        maximum float           8.32x  8.14x        1.00x 183.23x [2]_      1.32x     54.56 ns
        >maximum float          1.03x  1.00x   1.03x [3]_     DNF [4]_   DNF [4]_    675.87 ns
        32-bit (+) integer      5.50x  2.95x        1.30x        1.78x      1.00x     11.53 ns
        32-bit (-) integer      4.36x  2.42x        1.00x        1.36x      1.11x     15.26 ns
        64-bit (+) integer      2.48x  1.47x        1.00x        1.14x      1.07x     47.99 ns
        64-bit (-) integer      2.56x  1.54x        1.00x        1.23x      1.10x     47.58 ns
        >64-bit (+) integer     2.30x  1.79x        1.69x        2.00x 1.00x [5]_     70.20 ns
        >64-bit (-) integer     2.24x  1.75x        1.60x        1.93x 1.00x [5]_     73.51 ns
        empty list              1.29x  1.68x        1.02x        1.16x      1.00x     62.65 ns
        empty dictionary        1.36x  1.41x        1.12x        1.13x      1.00x     62.57 ns
        ====================== ====== ====== ============ ============ ========== ============

.. tab:: Python 3.14.8

    .. only:: latex

        .. rubric:: decode (Python 3.14.8)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ============ ========== ============
        decode                   json jsonyx fastsimdjson      msgspec     orjson fastest time
        ====================== ====== ====== ============ ============ ========== ============
        outer space            34.86x 10.32x        1.00x        5.78x      8.66x      0.10 ns
        inner space            12.69x 10.34x        1.00x        5.14x      6.77x      0.10 ns
        7-bit character         3.76x  1.85x        1.05x        1.00x      2.00x      0.50 ns
        8-bit character         1.92x  1.39x        1.00x        1.44x      1.53x      1.80 ns
        11-bit character        2.66x  2.00x        1.00x        1.71x      1.52x      1.87 ns
        16-bit character        2.55x  2.08x        1.00x        1.87x      1.51x      2.56 ns
        21-bit character        1.87x  1.53x        1.00x        1.41x      1.02x      4.38 ns
        7-in-16-bit character   4.26x  2.78x        1.00x        1.20x      1.78x      0.82 ns
        7-in-32-bit character   2.73x  1.82x        1.32x        1.44x      1.00x      1.58 ns
        11-in-32-bit character  3.30x  2.57x        1.00x        2.25x      2.24x      1.97 ns
        16-in-32-bit character  2.98x  2.55x        1.00x        1.60x      1.48x      3.24 ns
        utf-8-sig character     3.51x  1.73x        1.00x        1.40x      2.25x      0.54 ns
        utf-16le character      1.71x  1.00x        2.19x        3.03x      2.79x      1.73 ns
        utf-16be character      1.65x  1.00x        2.13x        2.89x      2.67x      1.85 ns
        utf-32le character      1.32x  1.00x        2.20x        2.48x      2.21x      4.46 ns
        utf-32be character      1.42x  1.00x        2.39x        2.66x      2.35x      4.00 ns
        double quote escape     2.89x  1.77x        1.87x        2.19x      1.00x      2.93 ns
        backslash escape        2.67x  1.63x        1.73x        2.02x      1.00x      3.18 ns
        character escape        2.55x  1.70x        1.77x        2.04x      1.00x      3.18 ns
        7-bit escape            4.28x  3.34x        1.00x        3.13x      1.70x      3.82 ns
        8-bit escape            3.20x  2.49x        1.00x        2.85x      1.45x      5.14 ns
        11-bit escape           3.35x  2.63x        1.00x        3.05x      1.51x      5.04 ns
        16-bit escape           2.66x  2.10x        1.00x        2.70x      1.38x      6.33 ns
        21-bit escape           2.86x  2.34x        1.00x        2.50x      1.47x     10.18 ns
        null                    2.46x  3.10x        1.00x        1.36x      1.89x      8.21 ns
        boolean                 2.46x  3.20x        1.00x        1.38x      1.82x      8.49 ns
        empty string            2.72x  2.50x        1.00x        1.29x      1.11x     14.17 ns
        fixed-point float       2.61x  2.04x        1.11x        1.12x      1.00x     39.57 ns
        scientific float        2.63x  2.12x        1.02x        1.12x      1.00x     42.71 ns
        minimum float          10.02x  9.55x        1.00x 123.46x [2]_      1.11x     47.04 ns
        <minimum float         14.74x 14.22x        1.00x 145.54x [2]_      1.10x     47.22 ns
        maximum float           9.13x  8.81x        1.00x 177.44x [2]_      1.39x     53.71 ns
        >maximum float          1.02x  1.00x   1.02x [3]_     DNF [4]_   DNF [4]_    742.71 ns
        32-bit (+) integer      5.10x  2.70x        1.25x        1.41x      1.00x     12.28 ns
        32-bit (-) integer      4.41x  2.34x        1.00x        1.04x      1.10x     15.37 ns
        64-bit (+) integer      2.39x  1.58x        1.00x        1.13x      1.13x     46.20 ns
        64-bit (-) integer      2.42x  1.60x        1.00x        1.15x      1.13x     46.50 ns
        >64-bit (+) integer     2.06x  1.85x        1.64x        1.97x 1.00x [5]_     72.59 ns
        >64-bit (-) integer     2.06x  1.80x        1.61x        1.99x 1.00x [5]_     72.71 ns
        empty list              1.17x  1.32x        1.00x        1.11x      1.02x     63.29 ns
        empty dictionary        1.22x  1.27x        1.03x        1.12x      1.00x     63.78 ns
        ====================== ====== ====== ============ ============ ========== ============

.. tab:: Python 3.13.16

    .. only:: latex

        .. rubric:: decode (Python 3.13.16)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ============ ========== ============
        decode                   json jsonyx fastsimdjson      msgspec     orjson fastest time
        ====================== ====== ====== ============ ============ ========== ============
        outer space            33.07x 10.30x        1.00x        5.89x      8.92x      0.09 ns
        inner space             5.12x 11.10x        1.00x        5.60x      5.13x      0.15 ns
        7-bit character         4.12x  2.77x        1.06x        1.00x      1.97x      0.50 ns
        8-bit character         1.99x  1.74x        1.00x        1.42x      1.50x      1.86 ns
        11-bit character        2.17x  1.90x        1.00x        1.49x      1.54x      1.83 ns
        16-bit character        1.97x  1.78x        1.00x        1.60x      1.45x      2.57 ns
        21-bit character        1.65x  1.42x        1.00x        1.40x      1.02x      4.40 ns
        7-in-16-bit character   3.32x  2.73x        1.00x        1.24x      1.85x      0.83 ns
        7-in-32-bit character   2.17x  1.54x        1.32x        1.46x      1.00x      1.55 ns
        11-in-32-bit character  2.89x  2.36x        1.00x        2.35x      1.65x      1.85 ns
        16-in-32-bit character  2.60x  2.22x        1.00x        1.95x      1.48x      2.63 ns
        utf-8-sig character     3.43x  2.54x        1.00x        1.34x      2.21x      0.54 ns
        utf-16le character      1.29x  1.00x        2.17x        2.77x      2.74x      1.73 ns
        utf-16be character      1.25x  1.00x        2.06x        2.61x      2.54x      1.94 ns
        utf-32le character      1.30x  1.00x        3.02x        3.62x      3.04x      3.32 ns
        utf-32be character      1.32x  1.00x        3.19x        3.89x      3.20x      3.06 ns
        double quote escape     2.56x  2.12x        1.89x        2.09x      1.00x      2.92 ns
        backslash escape        2.56x  2.12x        1.88x        2.08x      1.00x      2.92 ns
        character escape        2.06x  1.97x        1.74x        1.95x      1.00x      3.15 ns
        7-bit escape            3.93x  3.72x        1.00x        3.33x      1.79x      3.60 ns
        8-bit escape            2.86x  2.71x        1.00x        3.10x      1.57x      4.90 ns
        11-bit escape           2.91x  2.79x        1.00x        3.17x      1.93x      4.94 ns
        16-bit escape           2.94x  2.79x        1.00x        3.24x      1.65x      5.95 ns
        21-bit escape           2.91x  2.47x        1.00x        2.49x      1.67x      9.55 ns
        null                    2.91x  3.27x        1.00x        1.58x      1.93x      7.78 ns
        boolean                 2.55x  3.26x        1.00x        1.39x      1.81x      8.27 ns
        empty string            2.46x  2.56x        1.00x        1.27x      1.10x     13.70 ns
        fixed-point float       2.56x  2.13x        1.15x        1.17x      1.00x     37.69 ns
        scientific float        2.58x  2.22x        1.08x        1.14x      1.00x     40.53 ns
        minimum float           8.93x  8.64x        1.00x 125.91x [2]_      1.10x     46.13 ns
        <minimum float         13.30x 12.83x        1.00x 153.79x [2]_      1.10x     44.87 ns
        maximum float           8.16x  8.07x        1.00x 189.96x [2]_      1.34x     53.36 ns
        >maximum float          1.01x  1.00x   1.01x [3]_     DNF [4]_   DNF [4]_    652.76 ns
        32-bit (+) integer      5.53x  2.92x        1.30x        1.52x      1.00x     11.57 ns
        32-bit (-) integer      4.65x  2.53x        1.00x        1.18x      1.13x     15.04 ns
        64-bit (+) integer      2.31x  1.59x        1.00x        1.08x      1.07x     46.20 ns
        64-bit (-) integer      2.33x  1.63x        1.00x        1.16x      1.12x     46.42 ns
        >64-bit (+) integer     2.26x  1.68x        1.56x        1.90x 1.00x [5]_     72.34 ns
        >64-bit (-) integer     1.98x  1.80x        1.52x        1.85x 1.00x [5]_     71.70 ns
        empty list              1.25x  1.35x        1.00x        1.12x      1.00x     60.15 ns
        empty dictionary        1.26x  1.41x        1.02x        1.16x      1.00x     59.80 ns
        ====================== ====== ====== ============ ============ ========== ============

.. tab:: Python 3.12.15

    .. only:: latex

        .. rubric:: encode (Python 3.12.15)

    .. table::
        :widths: grid
        :class: longtable

        ======================== ====== ====== ============ ============ ========== ============
        decode                     json jsonyx fastsimdjson      msgspec     orjson fastest time
        ======================== ====== ====== ============ ============ ========== ============
        outer space              29.60x  9.62x        1.00x        5.86x     10.32x      0.10 ns
        inner space              10.98x  8.81x        1.00x        4.75x      6.24x      0.10 ns
        7-bit character           3.64x  2.68x        1.08x        1.00x      2.00x      0.50 ns
        8-bit character           2.17x  1.90x        1.00x        1.59x      1.52x      1.82 ns
        11-bit character          2.33x  1.68x        1.00x        1.26x      1.54x      1.84 ns
        16-bit character          2.35x  1.90x        1.00x        1.73x      1.42x      2.66 ns
        21-bit character          1.76x  1.33x        1.01x        1.30x      1.00x      4.38 ns
        7-in-16-bit character     4.19x  2.73x        1.00x        1.25x      1.74x      0.82 ns
        7-in-32-bit character     2.48x  1.40x        1.21x        1.34x      1.00x      1.71 ns
        11-in-32-bit character    3.12x  2.13x        1.00x        2.11x      1.59x      1.89 ns
        16-in-32-bit character    2.97x  2.27x        1.00x        2.02x      1.40x      2.79 ns
        utf-8-sig character       3.51x  2.62x        1.00x        1.41x      2.30x      0.54 ns
        utf-16le character        1.68x  1.00x        2.51x        2.85x      3.08x      1.78 ns
        utf-16be character        1.57x  1.00x        2.26x        2.57x      2.74x      2.13 ns
        utf-32le character        1.57x  1.00x        2.87x        3.37x      2.89x      3.32 ns
        utf-32be character        1.50x  1.00x        2.65x        3.08x      2.69x      3.78 ns
        double quote escape       1.92x  1.82x        1.77x        1.85x      1.00x      3.17 ns
        backslash escape          1.93x  1.82x        1.74x        1.86x      1.00x      3.17 ns
        character escape          2.01x  1.69x        1.65x        1.80x      1.00x      3.41 ns
        7-bit escape              3.01x  3.53x        1.00x        3.16x      1.94x      3.61 ns
        8-bit escape              2.17x  2.59x        1.00x        2.93x      1.72x      4.91 ns
        11-bit escape             2.38x  2.77x        1.00x        2.93x      1.78x      4.80 ns
        16-bit escape             1.99x  2.29x        1.00x        2.94x      1.44x      5.74 ns
        21-bit escape             2.41x  2.45x        1.00x        2.56x      1.60x      9.51 ns
        null                      2.68x  3.45x        1.00x        1.58x      1.91x      7.55 ns
        boolean                   2.60x  3.39x        1.00x        1.61x      1.93x      8.02 ns
        empty string              2.22x  2.59x        1.00x        1.26x      1.16x     13.44 ns
        fixed-point float         2.63x  2.15x        1.16x        1.20x      1.00x     37.59 ns
        scientific float          2.53x  2.12x        1.02x        1.11x      1.00x     43.19 ns
        minimum float             8.89x  8.48x        1.00x 125.44x [2]_      1.10x     46.19 ns
        <minimum float           13.10x 12.79x        1.00x 152.60x [2]_      1.09x     45.29 ns
        maximum float             8.19x  8.02x        1.00x 177.46x [2]_      1.31x     53.70 ns
        >maximum float            1.01x  1.00x   1.03x [3]_     DNF [4]_   DNF [4]_    660.20 ns
        32-bit (+) integer        5.79x  3.07x        1.32x        1.51x      1.00x     11.17 ns
        32-bit (-) integer        4.56x  2.45x        1.00x        1.22x      1.09x     14.79 ns
        64-bit (+) integer        2.45x  1.60x        1.00x        1.09x      1.09x     46.83 ns
        64-bit (-) integer        2.42x  1.60x        1.00x        1.13x      1.10x     46.78 ns
        >64-bit (+) integer       2.20x  1.74x        1.55x        2.06x 1.00x [5]_     70.30 ns
        >64-bit (-) integer       2.22x  1.76x        1.50x        2.07x 1.00x [5]_     69.78 ns
        empty list                1.27x  1.39x        1.02x        1.15x      1.00x     59.26 ns
        empty dictionary          1.25x  1.36x        1.02x        1.16x      1.00x     59.21 ns
        ======================== ====== ====== ============ ============ ========== ============

.. tab:: Python 3.11.17

    .. only:: latex

        .. rubric:: decode (Python 3.11.17)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ============ ========== ============
        decode                   json jsonyx fastsimdjson      msgspec     orjson fastest time
        ====================== ====== ====== ============ ============ ========== ============
        outer space            37.44x  9.71x        1.00x        5.90x      9.60x      0.09 ns
        inner space             5.88x  8.57x        1.00x        4.27x      6.03x      0.12 ns
        7-bit character         4.00x  1.71x        1.07x        1.00x      1.97x      0.50 ns
        8-bit character         1.90x  1.37x        1.00x        1.33x      1.51x      1.82 ns
        11-bit character        2.67x  2.06x        1.00x        1.58x      1.80x      1.57 ns
        16-bit character        2.15x  1.77x        1.00x        1.57x      1.53x      2.46 ns
        21-bit character        1.80x  1.51x        1.00x        1.38x      1.07x      4.14 ns
        7-in-16-bit character   4.13x  2.87x        1.00x        1.35x      2.00x      0.76 ns
        7-in-32-bit character   2.54x  1.78x        1.29x        1.46x      1.00x      1.56 ns
        11-in-32-bit character  3.37x  2.72x        1.00x        2.40x      1.77x      1.71 ns
        16-in-32-bit character  2.79x  2.35x        1.00x        1.90x      1.54x      2.58 ns
        utf-8-sig character     3.50x  1.73x        1.00x        1.40x      2.24x      0.54 ns
        utf-16le character      1.52x  1.00x        2.27x        2.67x      2.78x      1.83 ns
        utf-16be character      1.47x  1.00x        2.13x        2.50x      2.60x      2.04 ns
        utf-32le character      1.24x  1.00x        2.18x        2.57x      2.24x      4.85 ns
        utf-32be character      1.24x  1.00x        2.17x        2.55x      2.23x      4.93 ns
        double quote escape     2.12x  2.08x        1.87x        2.20x      1.00x      2.92 ns
        backslash escape        2.11x  2.07x        1.87x        2.20x      1.00x      2.93 ns
        character escape        2.05x  2.23x        1.84x        2.29x      1.00x      2.94 ns
        7-bit escape            3.96x  3.75x        1.00x        3.55x      1.97x      3.60 ns
        8-bit escape            2.97x  2.85x        1.00x        3.19x      1.75x      4.79 ns
        11-bit escape           2.82x  2.64x        1.00x        2.98x      2.03x      5.55 ns
        16-bit escape           3.11x  3.03x        1.00x        3.02x      1.76x      5.66 ns
        21-bit escape           3.23x  2.99x        1.00x        2.51x      1.59x      9.35 ns
        null                    2.31x  2.85x        1.00x        1.37x      1.66x      9.03 ns
        boolean                 2.35x  2.81x        1.00x        1.30x      1.66x      9.32 ns
        empty string            2.40x  2.65x        1.00x        1.41x      1.19x     13.02 ns
        fixed-point float       2.80x  2.21x        1.12x        1.28x      1.00x     33.64 ns
        scientific float        2.62x  2.22x        1.00x        1.15x      1.14x     38.64 ns
        minimum float          10.87x 10.49x        1.00x 145.67x [2]_      1.21x     39.87 ns
        <minimum float         16.67x 16.26x        1.00x 175.40x [2]_      1.20x     39.25 ns
        maximum float           9.61x  9.12x        1.00x 210.77x [2]_      1.40x     47.96 ns
        >maximum float          1.04x  1.00x   1.04x [3]_     DNF [4]_   DNF [4]_    709.44 ns
        32-bit (+) integer      5.96x  3.04x        1.56x        1.55x      1.00x     11.01 ns
        32-bit (-) integer      3.92x  2.18x        1.01x        1.17x      1.00x     16.60 ns
        64-bit (+) integer      2.47x  1.48x        1.00x        1.08x      1.05x     45.33 ns
        64-bit (-) integer      2.52x  1.52x        1.00x        1.12x      1.10x     45.46 ns
        >64-bit (+) integer     2.43x  2.04x        1.91x        2.23x 1.00x [5]_     65.15 ns
        >64-bit (-) integer     2.38x  2.06x        1.85x        2.21x 1.00x [5]_     64.94 ns
        empty list              1.32x  1.47x        1.01x        1.14x      1.00x     53.03 ns
        empty dictionary        1.32x  1.47x        1.04x        1.17x      1.00x     51.98 ns
        ====================== ====== ====== ============ ============ ========== ============

.. tab:: Python 3.10.22

    .. only:: latex

        .. rubric:: decode (Python 3.10.22)

    .. table::
        :widths: grid
        :class: longtable

        ====================== ====== ====== ============ ============ ========== ============
        decode                   json jsonyx fastsimdjson      msgspec     orjson fastest time
        ====================== ====== ====== ============ ============ ========== ============
        outer space            44.39x  8.55x        1.00x        5.82x      8.75x      0.10 ns
        inner space            14.41x  8.57x        1.00x        7.71x      6.89x      0.10 ns
        7-bit character         3.16x  2.68x        1.08x        1.00x      2.01x      0.50 ns
        8-bit character         1.85x  1.72x        1.00x        1.39x      1.57x      1.74 ns
        11-bit character        2.35x  1.92x        1.00x        1.50x      1.69x      1.69 ns
        16-bit character        2.26x  1.95x        1.00x        1.76x      1.63x      2.35 ns
        21-bit character        1.70x  1.41x        1.00x        1.40x      1.07x      4.12 ns
        7-in-16-bit character   3.88x  2.94x        1.00x        1.38x      2.04x      0.75 ns
        7-in-32-bit character   2.23x  1.48x        1.25x        1.45x      1.00x      1.57 ns
        11-in-32-bit character  2.89x  2.21x        1.00x        2.19x      1.62x      1.87 ns
        16-in-32-bit character  2.88x  2.42x        1.00x        2.12x      1.64x      2.44 ns
        utf-8-sig character     3.08x  2.62x        1.00x        1.40x      2.30x      0.54 ns
        utf-16le character      1.40x  1.00x        2.22x        2.76x      2.88x      1.75 ns
        utf-16be character      1.36x  1.00x        2.06x        2.53x      2.64x      2.01 ns
        utf-32le character      1.28x  1.00x        2.49x        2.94x      2.57x      4.19 ns
        utf-32be character      1.27x  1.00x        2.44x        2.87x      2.53x      4.29 ns
        double quote escape     2.69x  2.10x        1.86x        2.11x      1.00x      2.94 ns
        backslash escape        2.69x  2.12x        1.85x        2.13x      1.00x      2.93 ns
        character escape        2.68x  2.10x        1.89x        2.10x      1.00x      2.95 ns
        7-bit escape            4.14x  3.77x        1.00x        3.31x      1.95x      3.60 ns
        8-bit escape            3.12x  2.84x        1.00x        3.11x      1.77x      4.77 ns
        11-bit escape           2.83x  2.67x        1.00x        2.74x      1.57x      5.43 ns
        16-bit escape           2.85x  2.61x        1.00x        2.97x      1.50x      5.43 ns
        21-bit escape           2.80x  2.58x        1.00x        2.73x      1.59x      9.35 ns
        null                    2.27x  2.63x        1.00x        1.31x      1.69x      9.00 ns
        boolean                 2.14x  2.86x        1.00x        1.53x      1.71x      9.14 ns
        empty string            2.10x  2.58x        1.00x        1.38x      1.07x     14.73 ns
        fixed-point float       2.97x  2.15x        1.14x        1.24x      1.00x     33.62 ns
        scientific float        2.59x  2.14x        1.00x        1.14x      1.14x     37.14 ns
        minimum float           9.68x  9.24x        1.00x 147.78x [2]_      1.18x     39.28 ns
        <minimum float         14.53x 14.02x        1.00x 177.75x [2]_      1.16x     38.67 ns
        maximum float           8.17x  7.34x        1.00x 206.30x [2]_      1.34x     49.57 ns
        >maximum float          1.07x  1.00x   1.07x [3]_     DNF [4]_   DNF [4]_    594.04 ns
        32-bit (+) integer      5.97x  3.15x        1.40x        1.64x      1.00x     10.55 ns
        32-bit (-) integer      4.34x  2.38x        1.00x        1.19x      1.12x     14.84 ns
        64-bit (+) integer      2.40x  1.48x        1.00x        1.11x      1.09x     44.55 ns
        64-bit (-) integer      2.45x  1.57x        1.00x        1.16x      1.07x     44.66 ns
        >64-bit (+) integer     2.45x  2.01x        1.85x        2.18x 1.00x [5]_     65.50 ns
        >64-bit (-) integer     2.28x  2.02x        1.80x        2.18x 1.00x [5]_     65.41 ns
        empty list              1.28x  1.51x        1.02x        1.17x      1.00x     52.06 ns
        empty dictionary        1.29x  1.53x        1.04x        1.30x      1.00x     50.45 ns
        ====================== ====== ====== ============ ============ ========== ============

.. warning:: The Python version of :mod:`jsonyx` is up to 90.64x slower for
    encoding an  up to 82.59x slower for decoding, so make sure you have a
    `C compiler <https://wiki.python.org/moin/WindowsCompilers>`_ installe  on
    Windows.

.. rubric:: Footnotes

.. [1] integer exceeds 64-bit range
.. [2] see :issue:`msgspec/msgspec#1232`
.. [3] overflow, reparse  with :mod:`json`
.. [4] overflow
.. [5] converted to a float