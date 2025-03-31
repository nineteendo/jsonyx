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

## Benchmark (Mar 31, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |   json | jsonyx | msgspec |  orjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|--------:|-------------:|
| List of 256 booleans                        |  4.56x |  5.33x |   1.00x |   1.06x |      1.90 μs |
| List of 256 ASCII strings                   | 12.12x | 13.65x |   1.50x |   1.00x |      3.95 μs |
| List of 256 floats                          | 23.41x | 25.95x |   1.30x |   1.00x |      8.03 μs |
| List of 256 dicts with 1 int                | 11.10x | 13.61x |   1.32x |   1.00x |      7.75 μs |
| Medium complex object                       | 10.76x | 11.80x |   1.16x |   1.00x |     13.30 μs |
| List of 256 strings                         | 23.08x | 19.66x |   2.04x |   1.00x |     14.42 μs |
| Complex object                              |  7.36x |  7.95x |   1.00x |     DNF |    209.74 μs |
| Dict with 256 lists of 256 dicts with 1 int |  9.23x | 11.34x |   1.21x |   1.00x |   2361.90 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.40x |  6.26x |   2.60x |  1.28x |    1.00x |      1.54 μs |
| List of 256 ASCII strings                   |  9.08x | 12.57x |   5.43x |  5.03x |    1.00x |      2.89 μs |
| List of 256 floats                          | 10.99x | 12.47x |   2.32x |  1.78x |    1.00x |      6.14 μs |
| List of 256 dicts with 1 int                | 12.11x | 15.16x |   6.87x |  5.08x |    1.00x |      6.17 μs |
| Medium complex object                       | 12.65x | 17.63x |   5.26x |  4.40x |    1.00x |      7.62 μs |
| List of 256 strings                         |  5.68x |  4.38x |   9.92x |  8.00x |    1.00x |     16.76 μs |
| Complex object                              |  8.58x |  7.54x |   8.32x |  7.56x |    1.00x |    136.79 μs |
| Dict with 256 lists of 256 dicts with 1 int | 17.65x | 19.13x |  12.07x | 10.78x |    1.00x |   1658.37 μs |
