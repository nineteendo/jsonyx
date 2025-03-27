# jsonyx

[![pypi](https://img.shields.io/pypi/v/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jsonyx.svg)](https://anaconda.org/conda-forge/jsonyx)
[![python](https://img.shields.io/pypi/pyversions/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![license](https://img.shields.io/pypi/l/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg?branch=2.0.x)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)
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

## Benchmark (Mar 17, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |   json | jsonyx | msgspec |  orjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|--------:|-------------:|
| List of 256 booleans                        |  4.69x |  5.64x |   1.00x |   1.04x |      1.92 μs |
| List of 256 ASCII strings                   | 13.08x | 15.03x |   1.62x |   1.00x |      3.67 μs |
| List of 256 floats                          | 24.38x | 24.69x |   1.35x |   1.00x |      7.89 μs |
| List of 256 dicts with 1 int                | 11.34x | 14.32x |   1.35x |   1.00x |      7.67 μs |
| Medium complex object                       | 10.64x | 12.05x |   1.15x |   1.00x |     13.38 μs |
| List of 256 strings                         | 21.28x | 15.85x |   1.95x |   1.00x |     15.16 μs |
| Complex object                              |  7.14x |  7.65x |   1.00x |     DNF |    213.74 μs |
| Dict with 256 lists of 256 dicts with 1 int |  9.03x | 11.34x |   1.14x |   1.00x |   2423.70 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.65x |  7.19x |   3.02x |  1.41x |    1.00x |      1.43 μs |
| List of 256 ASCII strings                   |  7.35x | 12.65x |   4.73x |  4.42x |    1.00x |      2.98 μs |
| List of 256 floats                          | 10.85x | 12.17x |   2.16x |  1.66x |    1.00x |      6.10 μs |
| List of 256 dicts with 1 int                | 13.56x | 16.11x |   6.92x |  5.24x |    1.00x |      6.17 μs |
| Medium complex object                       | 12.47x | 18.84x |   5.25x |  4.34x |    1.00x |      7.68 μs |
| List of 256 strings                         |  4.01x |  3.41x |  14.99x |  8.04x |    1.00x |     23.47 μs |
| Complex object                              |  8.92x |  7.75x |   9.09x |  9.16x |    1.00x |    145.17 μs |
| Dict with 256 lists of 256 dicts with 1 int | 17.95x | 22.36x |  12.42x | 10.53x |    1.00x |   1621.17 μs |
