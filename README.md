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

## Benchmark (Apr 20, 2025)

We recommend to use [`orjson`](https://pypi.org/project/orjson),
[`msgspec`](https://pypi.org/project/msgspec) or
[`pysimdjson`](https://pypi.org/project/pysimdjson) for performance critical
applications:

| encode                                      |   json | jsonyx | msgspec | orjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|-------------:|
| List of 256 booleans                        |  4.58x |  4.13x |   1.05x |  1.00x |      1.84 μs |
| List of 256 ASCII strings                   | 14.00x | 11.60x |   1.57x |  1.00x |      3.92 μs |
| List of 256 floats                          | 24.93x | 25.59x |   1.34x |  1.00x |      8.28 μs |
| List of 256 dicts with 1 int                | 11.58x | 12.28x |   1.38x |  1.00x |      7.84 μs |
| Medium complex object                       | 10.12x | 10.40x |   1.16x |  1.00x |     13.87 μs |
| List of 256 strings                         | 19.70x | 14.69x |   1.73x |  1.00x |     18.10 μs |
| Complex object                              |  7.68x |  7.55x |   1.00x |    DNF |    211.43 μs |
| Dict with 256 lists of 256 dicts with 1 int |  4.52x |  5.43x |   3.20x |  1.00x |   5082.41 μs |

| decode                                      |   json | jsonyx | msgspec | orjson | simdjson | fastest time |
|:--------------------------------------------|-------:|-------:|--------:|-------:|---------:|-------------:|
| List of 256 booleans                        |  5.62x |  5.07x |   3.59x |  1.48x |    1.00x |      1.50 μs |
| List of 256 ASCII strings                   |  7.01x |  6.08x |   3.69x |  3.37x |    1.00x |      4.07 μs |
| List of 256 floats                          | 10.84x | 11.22x |   2.25x |  1.73x |    1.00x |      6.11 μs |
| List of 256 dicts with 1 int                | 12.94x | 11.52x |   7.11x |  5.16x |    1.00x |      6.12 μs |
| Medium complex object                       | 13.06x | 12.24x |   5.27x |  4.47x |    1.00x |      7.83 μs |
| List of 256 strings                         |  6.80x |  3.69x |   9.48x |  7.88x |    1.00x |     16.98 μs |
| Complex object                              |  9.89x |  7.84x |   9.01x |  8.00x |    1.00x |    130.54 μs |
| Dict with 256 lists of 256 dicts with 1 int | 18.73x | 15.92x |  11.58x |  9.65x |    1.00x |   1624.49 μs |
