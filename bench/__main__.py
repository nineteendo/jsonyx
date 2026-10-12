"""JSON benchmark."""
# TODO(Nice Zombies): re-run benchmark
from __future__ import annotations

__all__: list[str] = []

import json
import sys
from functools import partial
from math import inf
from timeit import timeit
from typing import TYPE_CHECKING, Any

import fastsimdjson  # type: ignore[import-not-found]
import msgspec
import orjson
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
    _Factory = Callable[[int], Any]


def _raws(obj: str | list[Any] | dict[str, Any]) -> str:
    if isinstance(obj, str):
        return f'"{obj}"'

    if isinstance(obj, list):
        return f'[{",".join(map(str, obj))}]'

    return f"""{{{
        ",".join([f"{_raws(key)}:{value}" for key, value in obj.items()])
    }}}"""


def _rawb(obj: str | list[Any] | dict[str, Any]) -> bytes:
    return _raws(obj).encode()


_ENCODE_CASES: dict[str, _Factory] = {
    # characters
    "5-bit character": lambda n: "\x00" * n,
    "7-bit character": lambda n: "\x20" * n,
    "8-bit character": lambda n: "\x80" * n,
    "11-bit character": lambda n: "\u0100" * n,
    "16-bit character": lambda n: "\u0800" * n,
    "21-bit character": lambda n: "\U00010000" * n,

    # constants
    "null": lambda n: [None] * n,
    "boolean": lambda n: [False] * n,

    # strings and keys
    "empty string": lambda n: [""] * n,
    "7-digit key": lambda n: {f"{i:07x}": None for i in range(n)},

    # floats
    "fixed-point float": lambda n: [0.0] * n,
    "scientific float": lambda n: [1e-05] * n,
    "subnormal float": lambda n: [5e-324] * n,
    "near-overflow float": lambda n: [1e308] * n,

    # integers
    "31-bit integer": lambda n: [0] * n,
    "32-bit integer": lambda n: [2 ** 31] * n,
    "63-bit integer": lambda n: [2 ** 32] * n,
    "64-bit integer": lambda n: [2 ** 63] * n,
    ">64-bit integer": lambda n: [2 ** 64] * n,

    # lists
    "empty list": lambda n: [[]] * n,  # type: ignore
    "non-empty list": lambda n: [[None]] * n,

    # dictionaries
    "empty dictionary": lambda n: [{}] * n,  # type: ignore
    "non-empty dictionary": lambda n: [{"": None}] * n,
}
_DECODE_CASES: dict[str, _Factory] = {
    # characters
    "7-bit character": lambda n: _rawb("\x20" * n),
    "8-bit character": lambda n: _rawb("\x80" * n),
    "11-bit character": lambda n: _rawb("\u0100" * n),
    "16-bit character": lambda n: _rawb("\u0800" * n),
    "21-bit character": lambda n: _rawb("\U00010000" * n),

    # escapes
    "7-bit escape": lambda n: _rawb(r"\u0020" * n),
    "8-bit escape": lambda n: _rawb(r"\u0080" * n),
    "11-bit escape": lambda n: _rawb(r"\u0100" * n),
    "16-bit escape": lambda n: _rawb(r"\u0800" * n),
    "21-bit escape": lambda n: _rawb(r"\ud800\udc00" * n),

    # constants
    "null": lambda n: _rawb(["null"] * n),
    "boolean": lambda n: _rawb(["false"] * n),

    # strings and keys
    "empty string": lambda n: _rawb(['""'] * n),
    "7-digit key": lambda n: _rawb({f"{i:07x}": "null" for i in range(n)}),

    # floats
    "fixed-point float": lambda n: _rawb(["0.0"] * n),
    "scientific float": lambda n: _rawb(["1e-05"] * n),
    "subnormal float": lambda n: _rawb(["5e-324"] * n),
    "near-overflow float": lambda n: _rawb(["1e308"] * n),
    "overflow float": lambda n: _rawb(["1e309"] * n),

    # integers
    "31-bit integer": lambda n: _rawb([0] * n),
    "32-bit integer": lambda n: _rawb([2 ** 31] * n),
    "63-bit integer": lambda n: _rawb([2 ** 32] * n),
    "64-bit integer": lambda n: _rawb([2 ** 63] * n),
    ">64-bit integer": lambda n: _rawb([2 ** 64] * n),

    # lists and dictionaries
    "empty list": lambda n: _rawb(["[]"] * n),
    "empty dictionary": lambda n: _rawb(["{}"] * n),
}


def _make_dumpb(func: _Func) -> _Func:
    return lambda obj: func(obj).encode()


_ENCODE_FUNCS: dict[str, _Func] = {
    "json": _make_dumpb(json.JSONEncoder().encode),
    "jsonyx": _make_dumpb(jsonyx.Encoder().dumps),
    "pyjsonyx": _make_dumpb(pyjsonyx.Encoder().dumps),
    # pylint: disable-next=I1101
    "fastsimdjson": fastsimdjson.dumpb,  # type: ignore
    "msgspec": msgspec.json.Encoder().encode,
    # pylint: disable-next=E1101
    "orjson": orjson.dumps,
}
_DECODE_FUNCS: dict[str, _Func] = {
    "json": json.loads,
    "jsonyx": jsonyx.Decoder().loads,
    "pyjsonyx": pyjsonyx.Decoder().loads,
    # pylint: disable-next=I1101
    "fastsimdjson": fastsimdjson.loads,  # type: ignore
    "msgspec": msgspec.json.Decoder().decode,
    # pylint: disable-next=E1101
    "orjson": orjson.loads,
}


def _run_benchmark(
    name: str, cases: dict[str, _Factory], funcs: dict[str, _Func],
) -> None:
    rows: list[list[str]] = []
    speedups: list[float] = []
    for case, make_obj in cases.items():
        times: dict[str, float] = {}
        for lib, func in funcs.items():
            print(end=".", flush=True)
            try:
                n: int = 1
                while True:
                    obj: Any = make_obj(n)
                    time_taken: float = timeit(partial(func, obj), number=1)
                    if time_taken >= 0.2 or n >= 2 ** 26:
                        times[lib] = time_taken / n
                        break

                    n *= 2
            except (ValueError, TypeError):
                times[lib] = inf

        speedups.append(times["pyjsonyx"] / times["jsonyx"])
        del times["pyjsonyx"]
        fastest_time: float = min(times.values())
        row: list[str] = [case]
        row.extend(f"{time / fastest_time:.02f}x" for time in times.values())
        row.append(f"{1e9 * fastest_time:.02f} ns")
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
