# jsonyx

[![pypi](https://img.shields.io/pypi/v/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jsonyx.svg)](https://anaconda.org/conda-forge/jsonyx)
[![python](https://img.shields.io/pypi/pyversions/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![license](https://img.shields.io/pypi/l/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg?branch=2.2.x)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)
[![docs](https://readthedocs.org/projects/jsonyx/badge/?version=stable)](https://jsonyx.readthedocs.io/en/stable/?badge=stable)
[![downloads](https://img.shields.io/pypi/dm/jsonyx.svg)](http://pypi.org/project/jsonyx)

`jsonyx` is a customizable [JSON](http://json.org) library for Python 3.8+. It
is written in pure Python with an optional C extension for better performance
and no dependencies.

The documentation for `jsonyx` is available online at: https://jsonyx.readthedocs.io

## Key Features

- JSON decoding, encoding and patching
- Pretty printing:
    ```json
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }
    ```
- Optionally supports these JSON deviations (specified in the documentation):
    ```javascript
    {
        /* Block */ // and line comments
        "Missing commas": [1 2 3],
        "NaN and infinity": [NaN, Infinity, -Infinity],
        "Surrogates": "\ud800",
        "Trailing comma": [0,],
        "Unquoted keys": {key: "value"}
    }
    ```
- Detailed error messages:
    ```none
    Traceback (most recent call last):
      File "/Users/wannes/Downloads/broken.json", line 1, column 99-381
        ...sList": {"GlossEntry": {"ID": "SGM..."GML", "XML"]}, "GlossSee": "markup"
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    jsonyx.JSONSyntaxError: Unterminated object
    ```
- Dedicated functions for reading and writing files and pretty printing

## Benchmark (Apr 20, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |   json | jsonyx | msgspec | orjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|-------------:|
| List of 256 booleans                        |  4.54x |  4.06x |   1.04x |  1.00x |      1.85 μs |
| List of 256 ASCII strings                   | 11.76x | 10.42x |   1.33x |  1.00x |      4.34 μs |
| List of 256 floats                          | 24.82x | 25.10x |   1.30x |  1.00x |      8.09 μs |
| List of 256 dicts with 1 int                | 11.10x | 11.50x |   1.34x |  1.00x |      7.92 μs |
| Medium complex object                       | 10.25x | 11.05x |   1.14x |  1.00x |     13.77 μs |
| List of 256 strings                         | 22.19x | 17.00x |   1.86x |  1.00x |     15.81 μs |
| Complex object                              |  7.54x |  7.41x |   1.00x |    DNF |    215.37 μs |
| Dict with 256 lists of 256 dicts with 1 int |  9.34x |  9.74x |   1.29x |  1.00x |   2394.91 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.36x |  5.26x |   2.76x |  1.40x |    1.00x |      1.46 μs |
| List of 256 ASCII strings                   |  8.54x |  6.93x |   4.28x |  3.96x |    1.00x |      3.46 μs |
| List of 256 floats                          | 10.85x | 11.25x |   2.23x |  1.74x |    1.00x |      6.05 μs |
| List of 256 dicts with 1 int                | 12.79x | 11.43x |   7.12x |  5.19x |    1.00x |      6.12 μs |
| Medium complex object                       | 12.70x | 12.01x |   5.16x |  4.60x |    1.00x |      7.98 μs |
| List of 256 strings                         |  7.11x |  3.82x |   9.70x |  7.80x |    1.00x |     16.52 μs |
| Complex object                              |  9.87x |  7.74x |   8.90x |  7.94x |    1.00x |    130.28 μs |
| Dict with 256 lists of 256 dicts with 1 int | 17.84x | 15.18x |  12.08x | 10.32x |    1.00x |   1674.28 μs |
