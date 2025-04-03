#!/usr/bin/env python
"""A command line utility to manipulate JSON files."""
from __future__ import annotations

__all__: list[str] = ["main"]

import sys
from argparse import ArgumentParser
from decimal import Decimal
from sys import modules, stderr, stdin
from traceback import format_exception_only
from typing import Any, Literal, cast

from jsonyx import (
    Decoder, Encoder, Manipulator, TruncatedSyntaxError, __version__,
    format_syntax_error, make_patch,
)
from jsonyx.allow import EVERYTHING, NOTHING


# pylint: disable-next=R0903
class _Namespace:
    command: Literal["format", "patch", "diff"] | None
    commas: bool
    compact: bool
    ensure_ascii: bool
    indent: int | str | None
    indent_leaves: bool
    input_filename: str | None
    max_indent_level: int | None
    quoted_keys: bool
    nonstrict: bool
    output_filename: str | None
    sort_keys: bool
    trailing_comma: bool
    use_decimal: bool


# pylint: disable-next=R0903
class _DiffNameSpace(_Namespace):
    old_input_filename: str


# pylint: disable-next=R0903
class _PatchNameSpace(_Namespace):
    patch_filename: str


def _configure(parser: ArgumentParser) -> None:
    parser.add_argument("-v", "--version", action="version", version=(
        f"jsonyx {__version__} "
        f"({'C extension' if '_jsonyx' in modules else 'Python'})"
    ))
    parent_parser: ArgumentParser = ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-a",
        "--ensure-ascii",
        action="store_true",
        help="escape non-ASCII characters",
    )
    parent_parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        help='avoid unnecessary whitespace after "," and ":"',
    )
    comma_group = parent_parser.add_mutually_exclusive_group()
    comma_group.add_argument(
        "-C",
        "--no-commas",
        action="store_false",
        dest="commas",
        help="don't separate items by commas when indented",
    )
    parent_parser.add_argument(
        "-d",
        "--use-decimal",
        action="store_true",
        help="use decimal instead of float",
    )
    indent_group = parent_parser.add_mutually_exclusive_group()
    indent_group.add_argument(
        "-i",
        "--indent",
        type=int,
        help="indent using the specified number of spaces",
        metavar="SPACES",
    )
    parent_parser.add_argument(
        "-l",
        "--no-indent-leaves",
        action="store_false",
        dest="indent_leaves",
        help="don't indent leaf objects and arrays",
    )
    parent_parser.add_argument(
        "-L",
        "--max-indent-level",
        type=int,
        help="the level up to which to indent",
        metavar="LEVEL",
    )
    parent_parser.add_argument(
        "-s",
        "--sort-keys",
        action="store_true",
        help="sort the keys of objects",
    )
    parent_parser.add_argument(
        "-S",
        "--nonstrict",
        action="store_true",
        help="allow all JSON deviations provided by jsonyx",
    )
    comma_group.add_argument(
        "-t",
        "--trailing-comma",
        action="store_true",
        help="add a trailing comma when indented",
    )
    indent_group.add_argument(
        "-T",
        "--indent-tab",
        action="store_const",
        const="\t",
        dest="indent",
        help="indent using tabs",
    )
    parent_parser.add_argument(
        "-q",
        "--unquoted-keys",
        action="store_false",
        dest="quoted_keys",
        help="don't quote keys which are identifiers",
    )
    commands = parser.add_subparsers(title="commands", dest="command")

    format_parser = commands.add_parser(
        "format",
        help="re-format or validate a JSON file",
        description="re-format or validate a JSON file",
        parents=[parent_parser],
    )
    format_parser.add_argument(
        "input_filename",
        nargs="?",
        help='the path to the input JSON file, or "-" for standard input',
    )
    format_parser.add_argument(
        "output_filename",
        nargs="?",
        help="the path to the output JSON file",
    )

    patch_parser = commands.add_parser(
        "patch",
        help="apply a JSON patch to the input file",
        description="apply a JSON patch to the input file",
        parents=[parent_parser],
    )
    patch_parser.add_argument(
        "patch_filename", help="the path to the JSON patch file",
    )
    patch_parser.add_argument(
        "input_filename",
        nargs="?",
        help='the path to the input JSON file, or "-" for standard input',
    )
    patch_parser.add_argument(
        "output_filename",
        nargs="?",
        help="the path to the output JSON file",
    )

    diff_parser = commands.add_parser(
        "diff",
        help="compare two JSON files and generate a diff in JSON patch format",
        description="compare two JSON files and generate a diff in JSON patch "
                    "format",
        parents=[parent_parser],
    )
    diff_parser.add_argument(
        "old_input_filename", help="the path to the old input JSON file",
    )
    diff_parser.add_argument(
        "input_filename",
        nargs="?",
        help='the path to the input JSON file, or "-" for standard input',
    )
    diff_parser.add_argument(
        "output_filename",
        nargs="?",
        help="the path to the output JSON file",
    )


def _run(args: _Namespace) -> None:
    decoder: Decoder = Decoder(
        allow=EVERYTHING if args.nonstrict else NOTHING,
        hooks={"float": Decimal if args.use_decimal else float},
    )
    encoder: Encoder = Encoder(
        allow=EVERYTHING if args.nonstrict else NOTHING,
        commas=args.commas,
        ensure_ascii=args.ensure_ascii,
        indent=args.indent,
        indent_leaves=args.indent_leaves,
        max_indent_level=args.max_indent_level,
        quoted_keys=args.quoted_keys,
        separators=(",", ":") if args.compact else (", ", ": "),
        sort_keys=args.sort_keys,
        trailing_comma=args.trailing_comma,
        types={"float": Decimal},
    )
    manipulator: Manipulator = Manipulator(
        allow=EVERYTHING if args.nonstrict else NOTHING,
        use_decimal=args.use_decimal,
    )
    try:
        if args.input_filename and args.input_filename != "-":
            input_obj: object = decoder.read(args.input_filename)
        elif stdin.isatty():
            input_obj = decoder.loads(
                "\n".join(iter(input, "")), filename="<stdin>",
            )
        else:
            input_obj = decoder.load(stdin)

        if args.command == "format":
            output_obj: Any = input_obj
        elif args.command == "patch":
            args = cast("_PatchNameSpace", args)
            patch: Any = decoder.read(args.patch_filename)
            output_obj = manipulator.apply_patch(input_obj, patch)
        else:
            args = cast("_DiffNameSpace", args)
            old_input_obj: object = decoder.read(args.old_input_filename)
            output_obj = make_patch(old_input_obj, input_obj)
            if len(output_obj) == 1:
                output_obj = output_obj[0]
    except TruncatedSyntaxError as exc:
        stderr.write("".join(format_syntax_error(exc)))
        sys.exit(1)
    except (
        AssertionError, LookupError, RecursionError, TypeError, ValueError,
    ) as exc:
        stderr.write("".join(format_exception_only(None, exc)))
        sys.exit(1)

    if args.output_filename and args.output_filename != "-":
        encoder.write(output_obj, args.output_filename)
    else:
        encoder.dump(output_obj)


def main() -> None:
    """Start jsonyx."""
    parser: ArgumentParser = ArgumentParser(
        description="a command line utility to manipulate JSON files",
    )
    _configure(parser)
    args: _Namespace = parser.parse_args(namespace=_Namespace())
    if not args.command:
        parser.print_help()
    else:
        try:
            _run(args)
        except BrokenPipeError as exc:
            sys.exit(exc.errno)


if __name__ == "__main__":
    main()
