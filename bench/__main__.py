"""JSON benchmark."""
from __future__ import annotations

__all__: list[str] = []

import json
from math import inf
from pathlib import Path
from random import random, seed
from sys import maxsize
from timeit import Timer
from typing import TYPE_CHECKING, Any

import msgspec
import orjson
import simdjson
from tabulate import tabulate  # type: ignore

import jsonyx

if TYPE_CHECKING:
    from collections.abc import Callable

    _Func = Callable[[Any], Any]

seed(0)
_USER: dict[str, Any] = {
    "userId": 3381293,
    "age": 213,
    "username": "johndoe",
    "fullname": "John Doe the Second",
    "isAuthorized": True,
    "liked": 31231.31231202,
    "approval": 31.1471,
    "jobs": [1, 2],
    "currJob": None,
}
_FRIENDS: list[dict[str, Any]] = [_USER] * 8
_ENCODE_CASES: dict[str, Any] = {
    "List of 256 booleans": [True] * 256,
    "List of 256 ASCII strings": [
        "A pretty long string which is in a list",
    ] * 256,
    "List of 256 floats": [
        maxsize * random() for _ in range(256)  # noqa: S311
    ],
    "List of 256 dicts with 1 int": [
        {str(random() * 20): int(random() * 1_000_000)}  # noqa: S311
        for _ in range(256)
    ],
    "Medium complex object": [[_USER, _FRIENDS]] * 6,
    "List of 256 strings": [
        "\u0646\u0638\u0627\u0645 \u0627\u0644\u062d\u0643\u0645 \u0633\u0644"
        "\u0637\u0627\u0646\u064a \u0648\u0631\u0627\u062b\u064a \u0641\u064a "
        "\u0627\u0644\u0630\u0643\u0648\u0631 \u0645\u0646 \u0630\u0631\u064a"
        "\u0629 \u0627\u0644\u0633\u064a\u062f \u062a\u0631\u0643\u064a \u0628"
        "\u0646 \u0633\u0639\u064a\u062f \u0628\u0646 \u0633\u0644\u0637\u0627"
        "\u0646 \u0648\u064a\u0634\u062a\u0631\u0637 \u0641\u064a\u0645\u0646 "
        "\u064a\u062e\u062a\u0627\u0631 \u0644\u0648\u0644\u0627\u064a\u0629 "
        "\u0627\u0644\u062d\u0643\u0645 \u0645\u0646 \u0628\u064a\u0646\u0647"
        "\u0645 \u0627\u0646 \u064a\u0643\u0648\u0646 \u0645\u0633\u0644\u0645"
        "\u0627 \u0631\u0634\u064a\u062f\u0627 \u0639\u0627\u0642\u0644\u0627 "
        "\u064b\u0648\u0627\u0628\u0646\u0627 \u0634\u0631\u0639\u064a\u0627 "
        "\u0644\u0627\u0628\u0648\u064a\u0646 \u0639\u0645\u0627\u0646\u064a"
        "\u064a\u0646 ",
    ] * 256,
    "Complex object": jsonyx.read(Path(__file__).parent / "sample.json"),
    "Dict with 256 lists of 256 dicts with 1 int": {
        str(random() * 20): [  # noqa: S311
            {str(random() * 20): int(random() * 1_000_000)}  # noqa: S311
            for _ in range(256)
        ]
        for _ in range(256)
    },
}
_ENCODE_FUNCS: dict[str, _Func] = {
    "json": json.JSONEncoder().encode,
    "jsonyx": jsonyx.Encoder().dumps,
    "msgspec": msgspec.json.Encoder().encode,
    # pylint: disable-next=E1101
    "orjson": orjson.dumps,
}
_DECODE_CASES: dict[str, Any] = {
    case: jsonyx.dumps(obj) for case, obj in _ENCODE_CASES.items()
}
_DECODE_FUNCS: dict[str, _Func] = {
    "json": json.JSONDecoder().decode,
    "jsonyx": jsonyx.Decoder().loads,
    "msgspec": msgspec.json.Decoder().decode,
    # pylint: disable-next=E1101
    "orjson": orjson.loads,
    "simdjson": simdjson.Parser().parse,
}


def _run_benchmark(
    name: str, cases: dict[str, Any], funcs: dict[str, _Func],
) -> None:
    results: list[list[str]] = []
    for case, obj in cases.items():
        times: dict[str, float] = {}
        for lib, func in funcs.items():
            print(end=".", flush=True)
            try:
                # pylint: disable-next=W0640
                timer: Timer = Timer(lambda: func(obj))  # noqa: B023
                number, time_taken = timer.autorange()
                times[lib] = time_taken / number
            except TypeError:
                times[lib] = inf

        unit: float = min(times.values())
        row: list[Any] = [case]
        for time in times.values():
            normalized_time = time / unit
            row.append(normalized_time)

        row.append(1_000_000 * unit)
        results.append(row)

    headers: list[str] = [name, *funcs.keys(), "fastest time"]
    print()
    print(tabulate(results, headers, tablefmt="pipe", floatfmt=".02f"))
    print(tabulate(results, headers, tablefmt="rst", floatfmt=".02f"))


if __name__ == "__main__":
    _run_benchmark("encode", _ENCODE_CASES, _ENCODE_FUNCS)
    _run_benchmark("decode", _DECODE_CASES, _DECODE_FUNCS)
