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

| encode                                                |   json |   jsonyx |   orjson |   simplejson |   unit (μs) |
|-------------------------------------------------------|--------|----------|----------|--------------|-------------|
| Array with 256 doubles                                |  22.67 |    22.22 |     1.00 |        23.98 |        9.07 |
| Array with 256 UTF-8 strings                          |  20.64 |     9.07 |     1.00 |        15.72 |       17.76 |
| Array with 256 strings                                |  12.39 |    11.28 |     1.00 |        13.32 |        4.26 |
| Medium complex object                                 |   9.97 |    12.54 |     1.00 |        15.95 |       14.27 |
| Array with 256 True values                            |   4.73 |     4.23 |     1.00 |         6.97 |        1.80 |
| Array with 256 dict{string, int} pairs                |  11.31 |    24.53 |     1.00 |        34.79 |        8.34 |
| Dict with 256 arrays with 256 dict{string, int} pairs |   9.26 |    20.32 |     1.00 |        29.77 |     2594.64 |
| Complex object                                        |   1.16 |     1.00 |  inf[^1] |         1.56 |     1384.86 |

| decode                                                |   json |   jsonyx |   orjson |   simplejson |   unit (μs) |
|-------------------------------------------------------|--------|----------|----------|--------------|-------------|
| Array with 256 doubles                                |   6.84 |     7.19 |     1.00 |         6.86 |        9.95 |
| Array with 256 UTF-8 strings                          |   1.17 |     1.00 |     2.02 |         1.31 |       64.42 |
| Array with 256 strings                                |   1.70 |     1.74 |     1.00 |         2.39 |       12.80 |
| Medium complex object                                 |   2.92 |     3.60 |     1.00 |         3.67 |       34.57 |
| Array with 256 True values                            |   3.07 |     4.94 |     1.00 |         7.25 |        2.18 |
| Array with 256 dict{string, int} pairs                |   3.38 |     2.83 |     1.00 |         3.44 |       36.09 |
| Dict with 256 arrays with 256 dict{string, int} pairs |   1.61 |     1.91 |     1.00 |         1.80 |    19592.58 |
| Complex object                                        |   1.16 |     1.06 |     1.00 |         1.29 |     1075.54 |

[^1]: recursion error