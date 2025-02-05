# jsonyx

[![pypi](https://img.shields.io/pypi/v/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jsonyx.svg)](https://anaconda.org/conda-forge/jsonyx)
[![python](https://img.shields.io/pypi/pyversions/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![license](https://img.shields.io/pypi/l/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)
[![docs](https://readthedocs.org/projects/jsonyx/badge/?version=stable)](https://jsonyx.readthedocs.io/en/stable/?badge=stable)
[![downloads](https://img.shields.io/pypi/dm/jsonyx.svg)](http://pypi.org/project/jsonyx)

`jsonyx` is a customizable [JSON](http://json.org) library for Python 3.8+. It
is written in pure Python with an optional C extension for better performance
and no dependencies. The documentation for `jsonyx` is available online at:
https://jsonyx.readthedocs.io

## Key Features

- JSON decoding, encoding and patching
- Pretty printing:
    ```json
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }
    ```
- Optionally supports these JSON deviations:
    ```javascript
    {
        /* Block */ // and line comments
        "Decimal numbers": [1.0000000000000001, 1e400],
        "Duplicate keys": {"key": "value 1", "key": "value 2"},
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

## Benchmark (Feb 5, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |  json | jsonyx | msgspec |  orjson | unit (μs) |
|:--------------------------------------------|------:|-------:|--------:|--------:|----------:|
| List of 256 booleans                        |  4.49 |   4.47 |    1.00 |    1.07 |      1.95 |
| List of 256 ASCII strings                   | 12.41 |  14.20 |    1.55 |    1.00 |      3.76 |
| List of 256 floats                          | 23.03 |  23.68 |    1.31 |    1.00 |      8.08 |
| List of 256 dicts with 1 int                | 11.08 |  13.61 |    1.33 |    1.00 |      7.86 |
| Medium complex object                       | 10.29 |  11.47 |    1.14 |    1.00 |     13.71 |
| List of 256 strings                         | 22.45 |  14.65 |    2.15 |    1.00 |     14.31 |
| Complex object                              |  7.11 |   5.47 |    1.00 | inf[^1] |    212.52 |
| Dict with 256 lists of 256 dicts with 1 int |  9.32 |  11.44 |    1.31 |    1.00 |   2359.82 |

| decode                                      |  json | jsonyx | msgspec | orjson | simdjson | unit (μs) |
|:--------------------------------------------|------:|-------:|--------:|-------:|---------:|----------:|
| List of 256 booleans                        |  4.64 |   7.19 |    2.99 |   1.40 |     1.00 |      1.42 |
| List of 256 ASCII strings                   |  7.61 |  12.30 |    5.04 |   4.66 |     1.00 |      2.87 |
| List of 256 floats                          | 11.04 |  12.00 |    2.18 |   1.64 |     1.00 |      6.23 |
| List of 256 dicts with 1 int                | 12.14 |  15.93 |    6.82 |   5.02 |     1.00 |      6.22 |
| Medium complex object                       | 12.53 |  19.08 |    5.24 |   4.46 |     1.00 |      7.72 |
| List of 256 strings                         |  5.37 |   4.11 |    9.40 |   7.26 |     1.00 |     17.52 |
| Complex object                              |  9.21 |   8.66 |    8.91 |   7.95 |     1.00 |    130.93 |
| Dict with 256 lists of 256 dicts with 1 int | 18.00 |  22.32 |   12.38 |  10.84 |     1.00 |   1622.21 |

[^1]: failed due to recursion error