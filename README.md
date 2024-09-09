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

We recommend to use `orjson` for performance critical applications:

| encode                                      |   json |   jsonyx |   orjson |   simplejson |   unit (μs) |
|---------------------------------------------|--------|----------|----------|--------------|-------------|
| List of 256 booleans                        |   4.25 |     3.77 |     1.00 |         6.04 |        2.02 |
| List of 256 ASCII strings                   |  15.04 |    13.59 |     1.00 |        15.62 |        3.59 |
| List of 256 dicts with 1 int                |  11.01 |    24.97 |     1.00 |        33.83 |        8.21 |
| List of 256 doubles                         |  24.72 |    24.65 |     1.00 |        24.90 |        8.39 |
| Medium complex object                       |  10.14 |    12.76 |     1.00 |        16.06 |       14.08 |
| List of 256 strings                         |  24.91 |    11.64 |     1.00 |        19.59 |       14.22 |
| Complex object                              |   1.17 |     1.00 |   inf    |         1.48 |     1390.97 |
| Dict with 256 lists of 256 dicts with 1 int |   9.70 |    20.34 |     1.00 |        31.16 |     2538.13 |

| decode                                      |   json |   jsonyx |   orjson |   simplejson |   unit (μs) |
|---------------------------------------------|--------|----------|----------|--------------|-------------|
| List of 256 booleans                        |   3.42 |     4.98 |     1.00 |         4.29 |        2.00 |
| List of 256 ASCII strings                   |   1.67 |     1.71 |     1.00 |         2.39 |       13.00 |
| List of 256 dicts with 1 int                |   2.28 |     2.76 |     1.00 |         3.22 |       33.16 |
| List of 256 doubles                         |   6.69 |     7.59 |     1.00 |         6.67 |       10.11 |
| Medium complex object                       |   2.93 |     3.66 |     1.00 |         3.69 |       33.71 |
| List of 256 strings                         |   1.02 |     1.00 |     2.02 |         1.30 |       64.05 |
| Complex object                              |   1.13 |     1.07 |     1.00 |         1.22 |     1068.31 |
| Dict with 256 lists of 256 dicts with 1 int |   1.57 |     1.82 |     1.00 |         1.92 |    18632.05 |

[^1]: recursion error