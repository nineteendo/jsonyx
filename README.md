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
      File "/Users/wannes/Downloads/broken.json", line 1, column 99-381
        ...sList": {"GlossEntry": {"ID": "SGM..."GML", "XML"]}, "GlossSee": "markup"
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    jsonyx.JSONSyntaxError: Unterminated object
    ```
- Dedicated functions for reading and writing files and pretty printing

## Benchmark

We recommend to use [`orjson`](https://pypi.org/project/orjson) or
[`msgspec`](https://pypi.org/project/msgspec) for performance critical
applications:

| encode                                      |  json | jsonyx | msgspec |  orjson | rapidjson | unit (μs) |
|:--------------------------------------------| -----:|-------:|--------:|--------:|----------:|----------:|
| List of 256 booleans                        |  4.82 |   4.11 |    1.16 |    1.00 |      3.12 |      1.85 |
| List of 256 ASCII strings                   | 14.71 |  12.73 |    1.67 |    1.00 |     10.12 |      3.64 |
| List of 256 floats                          | 23.47 |  23.54 |    1.38 |    1.00 |     24.87 |      8.57 |
| List of 256 dicts with 1 int                | 10.87 |  11.17 |    1.48 |    1.00 |      6.30 |      8.54 |
| Medium complex object                       |  9.90 |   9.76 |    1.24 |    1.00 |      7.31 |     14.48 |
| List of 256 strings                         | 26.73 |  14.99 |    2.26 |    1.00 |     34.28 |     13.69 |
| Complex object                              |  7.80 |   5.55 |    1.00 | inf[^1] |      6.92 |    205.10 |
| Dict with 256 lists of 256 dicts with 1 int |  9.58 |  10.23 |    1.27 |    1.00 |      5.32 |   2517.22 |

| decode                                      | json | jsonyx | msgspec | orjson | rapidjson | unit (μs) |
|:--------------------------------------------|-----:|-------:|--------:|-------:|----------:|----------:|
| List of 256 booleans                        | 3.40 |   5.24 |    2.06 |   1.00 |      2.42 |      2.03 |
| List of 256 ASCII strings                   | 1.68 |   2.05 |    1.12 |   1.00 |      1.59 |     13.11 |
| List of 256 floats                          | 6.58 |   7.38 |    1.45 |   1.00 |      5.71 |     10.25 |
| List of 256 dicts with 1 int                | 2.36 |   2.84 |    1.38 |   1.00 |      2.22 |     32.11 |
| Medium complex object                       | 2.89 |   3.70 |    1.23 |   1.00 |      2.62 |     33.99 |
| List of 256 strings                         | 1.02 |   1.00 |    2.74 |   2.04 |      2.99 |     64.38 |
| Complex object                              | 1.12 |   1.04 |    1.06 |   1.00 |      1.23 |   1061.41 |
| Dict with 256 lists of 256 dicts with 1 int | 1.66 |   1.91 |    1.14 |   1.00 |      1.47 |  17536.25 |

[^1]: failed due to recursion error