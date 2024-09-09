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

| encode                                      |  json | jsonyx | msgspec | orjson | simplejson | unit (μs) |
|---------------------------------------------|-------|--------|---------|--------|------------|-----------|
| List of 256 booleans                        |  4.61 |   4.04 |    1.19 |   1.00 |       6.68 |      1.90 |
| List of 256 ASCII strings                   | 13.95 |  13.06 |    1.61 |   1.00 |      14.90 |      3.84 |
| List of 256 dicts with 1 int                | 11.05 |  24.26 |    1.49 |   1.00 |      33.30 |      8.62 |
| List of 256 doubles                         | 24.49 |  24.37 |    1.42 |   1.00 |      25.35 |      8.42 |
| Medium complex object                       |  9.69 |  12.41 |    1.21 |   1.00 |      15.21 |     14.98 |
| List of 256 strings                         | 26.80 |  11.97 |    2.39 |   1.00 |      20.71 |     13.99 |
| Complex object                              |  7.82 |   7.01 |    1.00 | inf[^1]|      10.00 |    207.82 |
| Dict with 256 lists of 256 dicts with 1 int | 10.50 |  22.88 |    1.42 |   1.00 |      34.15 |   2352.28 |

| decode                                      | json | jsonyx | msgspec | orjson | simplejson | unit (μs) |
|---------------------------------------------|------|--------|---------|--------|------------|-----------|
| List of 256 booleans                        | 3.37 |   4.86 |    2.05 |   1.00 |       4.26 |      2.07 |
| List of 256 ASCII strings                   | 1.69 |   1.72 |    1.12 |   1.00 |       2.35 |     13.21 |
| List of 256 dicts with 1 int                | 2.27 |   2.97 |    1.38 |   1.00 |       3.21 |     34.03 |
| List of 256 doubles                         | 6.52 |   7.00 |    1.44 |   1.00 |       6.55 |     10.43 |
| Medium complex object                       | 2.78 |   3.77 |    1.20 |   1.00 |       3.54 |     35.86 |
| List of 256 strings                         | 1.05 |   1.00 |    2.66 |   2.05 |       1.29 |     64.54 |
| Complex object                              | 1.14 |   1.11 |    1.08 |   1.00 |       1.23 |   1065.53 |
| Dict with 256 lists of 256 dicts with 1 int | 1.63 |   2.09 |    1.13 |   1.00 |       1.96 |  17974.34 |

[^1]: failed due to recursion error