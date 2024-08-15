#!/usr/bin/env python
# Copyright (C) 2024 Nice Zombies
"""A command line utility to validate and pretty-print JSON objects."""
from __future__ import annotations

__all__: list[str] = []

import sys
from argparse import ArgumentParser
from sys import stderr, stdin

from jsonyx import (
    Decoder, Encoder, JSONSyntaxError, apply_patch, format_syntax_error,
)
from jsonyx.allow import EVERYTHING, NOTHING


# pylint: disable-next=R0903
class _Namespace:
    compact: bool
    ensure_ascii: bool
    indent: int | str | None
    input_filename: str | None
    no_commas: bool
    nonstrict: bool
    output_filename: str | None
    patch_filename: str | None
    sort_keys: bool
    trailing_comma: bool
    use_decimal: bool


def _register(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-a",
        "--ensure-ascii",
        action="store_true",
        help="escape non-ascii characters",
    )
    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        help='don\'t add unnecessary whitespace after "," and ":"',
    )
    comma_group = parser.add_mutually_exclusive_group()
    comma_group.add_argument(
        "-C",
        "--no-commas",
        action="store_true",
        help="separate items by whitespace instead of commas",
    )
    parser.add_argument(
        "-d",
        "--use-decimal",
        action="store_true",
        help="use decimal instead of float",
    )
    indent_group = parser.add_mutually_exclusive_group()
    indent_group.add_argument(
        "-i",
        "--indent",
        type=int,
        metavar="SPACES",
        help="indent using spaces",
    )
    parser.add_argument(
        "-s",
        "--sort-keys",
        action="store_true",
        help="sort the keys of objects",
    )
    parser.add_argument(
        "-S",
        "--nonstrict",
        action="store_true",
        help="allow all JSON deviations",
    )
    comma_group.add_argument(
        "-t",
        "--trailing-comma",
        action="store_true",
        help="add a trailing comma if indented",
    )
    indent_group.add_argument(
        "-T",
        "--indent-tab",
        action="store_const",
        const="\t",
        dest="indent",
        help="indent using tabs",
    )
    parser.add_argument(
        "input_filename",
        nargs="?",
        help='the path to the input JSON file, or "-" for standard input',
    )
    parser.add_argument(
        "output_filename",
        nargs="?",
        help="the path to the output JSON file",
    )
    parser.add_argument(
        "patch_filename",
        nargs="?",
        help="the path to the patch JSON file",
    )


def _run(args: _Namespace) -> None:
    decoder: Decoder = Decoder(
        allow=EVERYTHING if args.nonstrict else NOTHING,
        use_decimal=args.use_decimal,
    )
    # TODO(Nice Zombies): only add newline at EOF when writing to stdout
    encoder: Encoder = Encoder(
        allow=EVERYTHING if args.nonstrict else NOTHING,
        ensure_ascii=args.ensure_ascii,
        indent=args.indent,
        item_separator=" " if args.no_commas else (
            "," if args.compact else ", "
        ),
        key_separator=":" if args.compact else ": ",
        sort_keys=args.sort_keys,
        trailing_comma=args.trailing_comma,
    )
    try:
        if args.input_filename and args.input_filename != "-":
            obj: object = decoder.read(args.input_filename)
        elif stdin.isatty():
            obj = decoder.loads("\n".join(iter(input, "")), filename="<stdin>")
        else:
            obj = decoder.load(stdin)

        if args.patch_filename:
            obj = apply_patch(obj, decoder.read(args.patch_filename))
    except JSONSyntaxError as exc:
        stderr.write("".join(format_syntax_error(exc)))
        sys.exit(1)

    if args.output_filename and args.output_filename != "-":
        encoder.write(obj, args.output_filename)
    else:
        encoder.dump(obj)


def _main() -> None:
    parser: ArgumentParser = ArgumentParser(
        description="a command line utility to validate and pretty-print JSON "
                    "objects.",
    )
    _register(parser)
    try:
        _run(parser.parse_args(namespace=_Namespace()))
    except BrokenPipeError as exc:
        sys.exit(exc.errno)


if __name__ == "__main__":
    _main()
