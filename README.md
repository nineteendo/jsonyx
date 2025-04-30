# jsonyx

[![pypi](https://img.shields.io/pypi/v/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jsonyx.svg)](https://anaconda.org/conda-forge/jsonyx)
[![python](https://img.shields.io/pypi/pyversions/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![license](https://img.shields.io/pypi/l/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg?branch=2.3.x)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)
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

## Benchmark (Apr 30, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |   json | jsonyx | msgspec | orjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|-------------:|
| List of 256 booleans                        |  4.62x |  4.17x |   1.06x |  1.00x |      1.82 μs |
| List of 256 ASCII strings                   | 14.09x |  8.10x |   1.66x |  1.00x |      3.66 μs |
| List of 256 floats                          | 25.20x | 25.18x |   1.33x |  1.00x |      8.07 μs |
| List of 256 dicts with 1 int                | 11.24x |  9.89x |   1.34x |  1.00x |      7.87 μs |
| Medium complex object                       | 10.21x |  8.85x |   1.17x |  1.00x |     13.87 μs |
| List of 256 strings                         | 26.46x | 15.18x |   2.23x |  1.00x |     13.37 μs |
| Complex object                              |  7.86x |  7.41x |   1.00x |    DNF |    207.83 μs |
| Dict with 256 lists of 256 dicts with 1 int |  9.87x |  8.72x |   1.24x |  1.00x |   2295.24 μs |

| decode                                      |   json |  jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|--------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  4.70x |   5.22x |   2.92x |  1.41x |    1.00x |      1.45 μs |
| List of 256 ASCII strings                   |  9.04x |   7.05x |   4.85x |  4.43x |    1.00x |      3.15 μs |
| List of 256 floats                          | 10.91x |  11.22x |   2.24x |  1.73x |    1.00x |      6.14 μs |
| List of 256 dicts with 1 int                | 12.99x |  11.65x |   7.35x |  5.30x |    1.00x |      6.11 μs |
| Medium complex object                       | 13.41x |  12.94x |   5.44x |  4.67x |    1.00x |      7.65 μs |
| List of 256 strings                         |  6.85x |   3.75x |   9.56x |  7.85x |    1.00x |     16.78 μs |
| Complex object                              |  9.36x |   7.63x |   8.55x |  7.67x |    1.00x |    136.11 μs |
| Dict with 256 lists of 256 dicts with 1 int | 19.03x |  15.62x |  11.58x |  9.87x |    1.00x |   1640.77 μs |
