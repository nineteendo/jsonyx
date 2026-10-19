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


def _raw(obj: bytes | list[bytes], encoding: str = "utf-8") -> bytes:
    if isinstance(obj, bytes):
        return '"'.encode(encoding) + obj + '"'.encode(encoding)

    return (
        "[".encode(encoding)
        + ",".encode(encoding).join(obj)
        + "]".encode(encoding)
    )


_ENCODE_CASES: dict[str, _Factory] = {
    # characters
    "7-bit character": lambda n: "\u0020" * n,
    "8-bit character": lambda n: "\u0080" * n,
    "11-bit character": lambda n: "\u0100" * n,
    "16-bit character": lambda n: "\u0800" * n,
    "21-bit character": lambda n: "\U00010000" * n,

    # variable length characters
    "7-in-16-bit character": lambda n: "\u0020" * n + "\u0100",
    "7-in-32-bit character": lambda n: "\u0020" * n + "\U00010000",
    "11-in-32-bit character": lambda n: "\u0100" * n + "\U00010000",
    "16-in-32-bit character": lambda n: "\u0800" * n + "\U00010000",

    # escapes
    "double quote escape": lambda n: '"' * n,
    "backslash escape": lambda n: "\\" * n,
    "character escape": lambda n: "\b" * n,
    "7-bit escape": lambda n: "\u0000" * n,

    # constants
    "null": lambda n: [None] * n,
    "boolean": lambda n: [False] * n,

    # strings
    "empty string": lambda n: [""] * n,

    # floats
    "fixed-point float": lambda n: [0.0] * n,
    "scientific float": lambda n: [1e-05] * n,
    "minimum float": lambda n: [5e-324] * n,
    "maximum float": lambda n: [1.7976931348623157e+308] * n,

    # integers
    "32-bit positive integer": lambda n: [0] * n,
    "32-bit negative integer": lambda n: [-0] * n,
    "64-bit positive integer": lambda n: [4294967296] * n,
    "64-bit negative integer": lambda n: [-4294967296] * n,
    ">64-bit positive integer": lambda n: [18446744073709551616] * n,
    ">64-bit negative integer": lambda n: [-18446744073709551616] * n,

    # lists
    "empty list": lambda n: [[]] * n,  # type: ignore
    "non-empty list": lambda n: [[None]] * n,

    # dictionaries
    "empty dictionary": lambda n: [{}] * n,  # type: ignore
    "non-empty dictionary": lambda n: [{"": None}] * n,
}
_DECODE_CASES: dict[str, _Factory] = {
    # whitespace
    "outer space": lambda n: b" " * n + b"null",
    "inner space": lambda n: b"[" + b" " * n + b"]",

    # characters
    "7-bit character": lambda n: _raw(b"\x20" * n),
    "8-bit character": lambda n: _raw(b"\xc2\x80" * n),
    "11-bit character": lambda n: _raw(b"\xc4\x80" * n),
    "16-bit character": lambda n: _raw(b"\xe0\xa0\x80" * n),
    "21-bit character": lambda n: _raw(b"\xf0\x90\x80\x80" * n),

    # variable length characters
    "7-in-16-bit character": lambda n: _raw(b"\x20" * n + b"\xc4\x80"),
    "7-in-32-bit character": lambda n: _raw(b"\x20" * n + b"\xf0\x90\x80\x80"),
    "11-in-32-bit character": lambda n: _raw(
        b"\xc4\x80" * n + b"\xf0\x90\x80\x80",
    ),
    "16-in-32-bit character": lambda n: _raw(
        b"\xe0\xa0\x80" * n + b"\xf0\x90\x80\x80",
    ),

    # encodings
    "utf-8-sig character": lambda n: b"\xef\xbb\xbf" + _raw(b"\x20" * n),
    "utf-16le character": lambda n: _raw(b"\x00\x01" * n, "utf-16le"),
    "utf-16be character": lambda n: _raw(b"\x01\x00" * n, "utf-16be"),
    "utf-32le character": lambda n: _raw(b"\x00\x00\x01\x00" * n, "utf-32le"),
    "utf-32be character": lambda n: _raw(b"\x00\x01\x00\x00" * n, "utf-32be"),

    # escapes
    "double quote escape": lambda n: _raw(rb"\"" * n),
    "backslash escape": lambda n: _raw(rb"\\" * n),
    "character escape": lambda n: _raw(rb"\b" * n),
    "7-bit escape": lambda n: _raw(rb"\u0000" * n),
    "8-bit escape": lambda n: _raw(rb"\u0080" * n),
    "11-bit escape": lambda n: _raw(rb"\u0100" * n),
    "16-bit escape": lambda n: _raw(rb"\u0800" * n),
    "21-bit escape": lambda n: _raw(rb"\ud800\udc00" * n),

    # constants
    "null": lambda n: _raw([b"null"] * n),
    "boolean": lambda n: _raw([b"false"] * n),

    # strings
    "empty string": lambda n: _raw([b'""'] * n),

    # floats
    "fixed-point float": lambda n: _raw([b"0.0"] * n),
    "scientific float": lambda n: _raw([b"1e-05"] * n),
    "minimum float": lambda n: _raw([b"5e-324"] * n),
    "<minimum float": lambda n: _raw([b"2e-324"] * n),
    "maximum float": lambda n: _raw([b"1.7976931348623157e+308"] * n),
    ">maximum float": lambda n: _raw([b"1.7976931348623159e+308"] * n),

    # integers
    "32-bit positive integer": lambda n: _raw([b"0"] * n),
    "32-bit negative integer": lambda n: _raw([b"-0"] * n),
    "64-bit positive integer": lambda n: _raw([b"4294967296"] * n),
    "64-bit negative integer": lambda n: _raw([b"-4294967296"] * n),
    ">64-bit positive integer": lambda n: _raw([b"18446744073709551616"] * n),
    ">64-bit negative integer": lambda n: _raw([b"-18446744073709551616"] * n),

    # lists and dictionaries
    "empty list": lambda n: _raw([b"[]"] * n),
    "empty dictionary": lambda n: _raw([b"{}"] * n),
}


def _make_dumpb(func: _Func) -> _Func:
    return lambda obj: func(obj).encode()


def _make_loadb(func: _Func, encodings: set[str]) -> _Func:
    def loadb(s: Any) -> Any:
        encoding: str = jsonyx.detect_encoding(s)  # type: ignore
        if encoding not in encodings:
            s = s.decode(encoding)

        return func(s)

    return loadb


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
    "fastsimdjson": _make_loadb(
        # pylint: disable-next=I1101
        fastsimdjson.loads, {"utf-8", "utf-8-sig"},  # type: ignore
    ),
    "msgspec": _make_loadb(msgspec.json.Decoder().decode, {"utf-8"}),
    # pylint: disable-next=E1101
    "orjson": _make_loadb(orjson.loads, {"utf-8"}),
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
                    if (time_taken := timeit(
                        partial(func, make_obj(n)), number=1,
                    )) >= 0.2 or n >= 2 ** 26:
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
    print(f"Python {sys.version}")
    _run_benchmark("encode", _ENCODE_CASES, _ENCODE_FUNCS)
    _run_benchmark("decode", _DECODE_CASES, _DECODE_FUNCS)
