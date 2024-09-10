# jsonyx

[![pypi](https://img.shields.io/pypi/v/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/jsonyx.svg)](https://anaconda.org/conda-forge/jsonyx)
[![python](https://img.shields.io/pypi/pyversions/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![license](https://img.shields.io/pypi/l/jsonyx.svg)](http://pypi.org/project/jsonyx)
[![pytest](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml/badge.svg)](https://github.com/nineteendo/jsonyx/actions/workflows/pytest.yml)
[![docs](https://readthedocs.org/projects/jsonyx/badge/?version=stable)](https://jsonyx.readthedocs.io/en/stable/?badge=stable)
[![downloads](https://img.shields.io/pypi/dm/jsonyx.svg)](http://pypi.org/project/jsonyx)

`jsonyx` is a customizable [JSON](http://json.org) library for Python 3.10+. It
is written in pure Python with an optional C extension for better performance
and no dependencies. The documentation for `jsonyx` is available online at:
https://jsonyx.readthedocs.io/en/stable/usage.html

## Key Features

- JSON decoding, encoding and patching
- Pretty printing:
    ```json
    {
        "foo": [1, 2, 3],
        "bar": {"a": 1, "b": 2, "c": 3}
    }
    ```
- Optionally supports these JSON deviations using `jsonyx.allow`:
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
      File "C:\Users\wanne\Downloads\broken.json", line 2, column 15-19
         "path": "c:\users"
                      ^^^^
    jsonyx.JSONSyntaxError: Expecting 4 hex digits
    ```
- Dedicated functions for reading and writing files and pretty printing

## Benchmark

We recommend to use `orjson` or `msgspec` for performance critical applications:

| encode                                      |  json | jsonyx | msgspec |  orjson | rapidjson | unit (μs) |
|:--------------------------------------------| -----:|-------:|--------:|--------:|----------:|----------:|
| List of 256 booleans                        |  4.94 |   4.15 |    1.14 |    1.00 |      3.16 |      1.85 |
| List of 256 ASCII strings                   | 14.71 |  12.79 |    1.71 |    1.00 |     10.33 |      3.61 |
| List of 256 dicts with 1 int                | 11.02 |  12.28 |    1.50 |    1.00 |      6.49 |      8.32 |
| List of 256 floats                          | 23.31 |  23.15 |    1.36 |    1.00 |     24.79 |      8.67 |
| Medium complex object                       | 10.02 |  10.01 |    1.27 |    1.00 |      7.52 |     14.17 |
| List of 256 strings                         | 26.59 |  15.08 |    2.24 |    1.00 |     33.19 |     13.74 |
| Complex object                              |  7.72 |   5.53 |    1.00 | inf[^1] |      6.84 |    207.87 |
| Dict with 256 lists of 256 dicts with 1 int |  9.91 |  10.96 |    1.32 |    1.00 |      5.92 |   2449.84 |


| decode                                      | json | jsonyx | msgspec | orjson | rapidjson | unit (μs) |
|:--------------------------------------------|-----:|-------:|--------:|-------:|----------:|----------:|
| List of 256 booleans                        | 3.40 |   4.96 |    2.03 |   1.00 |      2.44 |      2.04 |
| List of 256 ASCII strings                   | 1.71 |   2.08 |    1.13 |   1.00 |      1.60 |     12.81 |
| List of 256 dicts with 1 int                | 2.44 |   2.88 |    1.39 |   1.00 |      2.15 |     33.17 |
| List of 256 floats                          | 6.26 |   6.96 |    1.40 |   1.00 |      5.40 |     10.79 |
| Medium complex object                       | 2.94 |   3.72 |    1.25 |   1.00 |      2.89 |     33.55 |
| List of 256 strings                         | 1.02 |   1.00 |    2.62 |   2.02 |      2.99 |     64.47 |
| Complex object                              | 1.12 |   1.05 |    1.07 |   1.00 |      1.23 |   1057.24 |
| Dict with 256 lists of 256 dicts with 1 int | 1.53 |   1.80 |    1.12 |   1.00 |      9.69 |  18954.53 |

[^1]: failed due to recursion error