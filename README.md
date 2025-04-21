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
| List of 256 booleans                        |  4.34x |  3.97x |   1.00x |  1.07x |      1.93 μs |
| List of 256 ASCII strings                   | 26.98x | 14.11x |   2.34x |  1.00x |      4.33 μs |
| List of 256 floats                          | 19.75x | 19.73x |   1.13x |  1.00x |     10.28 μs |
| List of 256 dicts with 1 int                | 13.76x | 13.65x |   1.34x |  1.00x |      7.85 μs |
| Medium complex object                       | 10.37x | 10.43x |   1.13x |  1.00x |     13.97 μs |
| List of 256 strings                         | 26.04x | 20.88x |   2.30x |  1.00x |     14.32 μs |
| Complex object                              |  7.66x |  7.29x |   1.00x |    DNF |    221.42 μs |
| Dict with 256 lists of 256 dicts with 1 int | 10.84x | 10.85x |   1.66x |  1.00x |   2296.56 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.68x |  5.55x |   2.85x |  1.43x |    1.00x |      1.44 μs |
| List of 256 ASCII strings                   |  5.86x |  4.74x |   2.96x |  2.71x |    1.00x |      5.03 μs |
| List of 256 floats                          | 15.50x | 12.11x |   2.19x |  1.99x |    1.00x |      6.49 μs |
| List of 256 dicts with 1 int                | 12.58x | 11.25x |   7.30x |  5.25x |    1.00x |      6.24 μs |
| Medium complex object                       | 13.70x | 13.10x |   5.58x |  4.66x |    1.00x |      7.57 μs |
| List of 256 strings                         |  6.87x |  3.75x |  11.21x |  7.78x |    1.00x |     16.74 μs |
| Complex object                              |  9.57x |  7.63x |   8.86x |  7.81x |    1.00x |    132.61 μs |
| Dict with 256 lists of 256 dicts with 1 int | 18.10x | 15.43x |  12.12x | 10.61x |    1.00x |   1652.20 μs |
