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
| List of 256 booleans                        |  4.36x |  3.91x |   1.00x |  1.03x |      1.97 μs |
| List of 256 ASCII strings                   | 10.42x | 10.08x |   1.37x |  1.00x |      4.53 μs |
| List of 256 floats                          | 23.27x | 23.37x |   1.33x |  1.00x |      8.06 μs |
| List of 256 dicts with 1 int                | 10.91x | 11.43x |   1.31x |  1.00x |      8.11 μs |
| Medium complex object                       |  9.99x | 10.46x |   1.14x |  1.00x |     13.60 μs |
| List of 256 strings                         | 17.98x | 14.32x |   1.64x |  1.00x |     18.59 μs |
| Complex object                              |  7.44x |  7.75x |   1.00x |    DNF |    205.09 μs |
| Dict with 256 lists of 256 dicts with 1 int |  8.87x |  9.70x |   1.16x |  1.00x |   2453.00 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.86x |  5.37x |   2.97x |  1.41x |    1.00x |      1.40 μs |
| List of 256 ASCII strings                   |  7.04x |  7.85x |   4.80x |  4.36x |    1.00x |      3.05 μs |
| List of 256 floats                          | 10.91x | 11.18x |   2.21x |  1.67x |    1.00x |      6.12 μs |
| List of 256 dicts with 1 int                | 12.05x | 11.64x |   6.86x |  5.00x |    1.00x |      6.24 μs |
| Medium complex object                       | 11.85x | 11.81x |   4.88x |  4.16x |    1.00x |      8.11 μs |
| List of 256 strings                         |  5.57x |  3.74x |   9.82x |  7.53x |    1.00x |     16.86 μs |
| Complex object                              |  8.78x |  7.45x |   8.56x |  7.60x |    1.00x |    137.30 μs |
| Dict with 256 lists of 256 dicts with 1 int | 17.32x | 14.97x |  11.67x | 10.68x |    1.00x |   1704.53 μs |
