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

## Benchmark

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |  json | jsonyx | msgspec |  orjson | unit (μs) |
|:--------------------------------------------|------:|-------:|--------:|--------:|----------:|
| List of 256 booleans                        |  4.60 |   3.92 |    1.08 |    1.00 |      1.95 |
| List of 256 ASCII strings                   | 11.57 |  12.67 |    1.52 |    1.00 |      4.27 |
| List of 256 floats                          | 22.02 |  23.15 |    1.41 |    1.00 |      9.14 |
| List of 256 dicts with 1 int                | 10.33 |  11.31 |    1.52 |    1.00 |      8.85 |
| Medium complex object                       |  9.68 |  10.13 |    1.22 |    1.00 |     15.26 |
| List of 256 strings                         | 21.84 |  11.63 |    2.12 |    1.00 |     14.97 |
| Complex object                              |  7.49 |   5.32 |    1.00 | inf[^1] |    207.61 |
| Dict with 256 lists of 256 dicts with 1 int |  8.40 |   9.14 |    1.20 |    1.00 |   2743.09 |

| decode                                      |  json | jsonyx | msgspec | orjson | simdjson | unit (μs) |
|:--------------------------------------------|------:|-------:|--------:|-------:|---------:|----------:|
| List of 256 booleans                        |  4.63 |   7.15 |    2.88 |   1.49 |     1.00 |      1.44 |
| List of 256 ASCII strings                   |  6.51 |   7.98 |    4.32 |   3.81 |     1.00 |      3.37 |
| List of 256 floats                          | 10.81 |  11.92 |    2.28 |   1.57 |     1.00 |      6.20 |
| List of 256 dicts with 1 int                | 12.04 |  14.29 |    6.73 |   4.98 |     1.00 |      6.31 |
| Medium complex object                       | 11.84 |  15.33 |    5.02 |   4.00 |     1.00 |      8.25 |
| List of 256 strings                         |  4.68 |   3.22 |    8.06 |   6.49 |     1.00 |     20.25 |
| Complex object                              |  9.12 |   8.55 |    8.99 |   8.16 |     1.00 |    132.89 |
| Dict with 256 lists of 256 dicts with 1 int | 17.42 |  19.91 |   11.83 |  11.09 |     1.00 |   1752.60 |

[^1]: failed due to recursion error