"""JSON benchmark."""
from __future__ import annotations

__all__: list[str] = []

import json
import sys
from functools import partial
from math import inf
from timeit import Timer
from typing import TYPE_CHECKING, Any

import msgspec
import orjson
import yyjson
from tabulate import tabulate  # type: ignore[import-untyped]

if sys.version_info >= (3, 10):
    from test.support.import_helper import import_fresh_module  # type: ignore
else:
    from test.support import import_fresh_module


if not (
    (jsonyx := import_fresh_module("jsonyx", fresh=["_jsonyx"]))
    and (pyjsonyx := import_fresh_module("jsonyx", blocked=["_jsonyx"]))
):
    raise ImportError

if TYPE_CHECKING:
    from collections.abc import Callable

    _Func = Callable[[Any], Any]

_ENCODE_CASES: dict[str, Any] = {
    # characters
    "65,536 control characters": "\x00" * 65_536,
    "65,536 ASCII characters": "\x20" * 65_536,
    "65,536 Unicode characters": "\x80" * 65_536,
    "65,536 non-BMP characters": "\U00010000" * 65_536,

    # constants
    "65,536 nulls": [None] * 65_536,
    "65,536 booleans": [False] * 65_536,

    # strings and keys
    "65,536 empty strings": [""] * 65_536,
    "65,536 ASCII keys": {f"{i}": None for i in range(65_536)},

    # floats
    "65,536 fixed-point floats": [0.0] * 65_536,
    "65,536 scientific floats": [1e-05] * 65_536,
    "65,536 subnormal floats": [5e-324] * 65_536,

    # integers
    "65,536 31-bit integers": [0] * 65_536,
    "65,536 32-bit integers": [2 ** 31] * 65_536,
    "65,536 63-bit integers": [2 ** 32] * 65_536,
    "65,536 64-bit integers": [2 ** 63] * 65_536,
    "65,536 >64-bit integers": [2 ** 64] * 65_536,

    # lists and dictionaries
    "65,536 empty lists": [[]] * 65_536,
    "65,536 empty dictionaries": [{}] * 65_536,
}
_DECODE_CASES: dict[str, bytes] = {
    case: json.dumps(obj).encode() for case, obj in _ENCODE_CASES.items()
}


def _make_dumpb(func: _Func) -> _Func:
    return lambda obj: func(obj).encode()


_ENCODE_FUNCS: dict[str, _Func] = {
    "json": _make_dumpb(json.JSONEncoder().encode),
    "jsonyx": _make_dumpb(jsonyx.Encoder().dumps),
    "pyjsonyx": _make_dumpb(pyjsonyx.Encoder().dumps),
    "msgspec": msgspec.json.Encoder().encode,
    # pylint: disable-next=E1101
    "orjson": orjson.dumps,
    "yyjson": _make_dumpb(yyjson.dumps),  # type: ignore
}
_DECODE_FUNCS: dict[str, _Func] = {
    "json": json.loads,
    "jsonyx": jsonyx.Decoder().loads,
    "pyjsonyx": pyjsonyx.Decoder().loads,
    "msgspec": msgspec.json.Decoder().decode,
    # pylint: disable-next=E1101
    "orjson": orjson.loads,
    "yyjson": yyjson.loads,  # type: ignore
}


def _run_benchmark(
    name: str, cases: dict[str, Any], funcs: dict[str, _Func],
) -> None:
    rows: list[list[str]] = []
    speedups: list[float] = []
    for case, obj in cases.items():
        times: dict[str, float] = {}
        for lib, func in funcs.items():
            print(end=".", flush=True)
            try:
                timer: Timer = Timer(partial(func, obj))
                number, time_taken = timer.autorange()
                times[lib] = time_taken / number
            except (ValueError, TypeError):
                times[lib] = inf

        speedups.append(times["pyjsonyx"] / times["jsonyx"])
        del times["pyjsonyx"]
        fastest_time: float = min(times.values())
        row: list[str] = [case]
        row.extend(f"{time / fastest_time:.02f}x" for time in times.values())
        row.append(f"{1_000_000 * fastest_time:.02f} \u03bcs")
        rows.append(row)

    del funcs["pyjsonyx"]
    headers: list[str] = [name, *funcs.keys(), "fastest time"]
    colalign: list[str] = ["left"] + ["right"] * (len(funcs) + 1)
    print()
    print(tabulate(rows, headers, "rst", colalign=colalign))
    print(f"max {name} speedup: {max(speedups):.02f}x")


if __name__ == "__main__":
    _run_benchmark("encode", _ENCODE_CASES, _ENCODE_FUNCS)
    _run_benchmark("decode", _DECODE_CASES, _DECODE_FUNCS)
