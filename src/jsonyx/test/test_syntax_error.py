"""TruncatedSyntaxError tests."""
from __future__ import annotations

__all__: list[str] = []

import pytest

from jsonyx import TruncatedSyntaxError


@pytest.mark.parametrize(
    ("doc", "start", "end", "lineno", "end_lineno", "end_colno"), [
        # Offset
        ("line ", 5, -1, 1, 1, 6),  # ln 1, col 6
        #      ^
        ("line \nline 2", 5, -1, 1, 1, 6),  # ln 1, col 6
        #      ^
        ("line \rline 2", 5, -1, 1, 1, 6),  # ln 1, col 6
        #      ^
        ("line \r\nline 2", 5, -1, 1, 1, 6),  # ln 1, col 6
        #      ^
        ("line ?", 5, -1, 1, 1, 7),  # ln 1, col 6-7
        #      ^
        ("line ?\nline 2", 5, -1, 1, 1, 7),  # ln 1, col 6-7
        #      ^
        ("line ?\rline 2", 5, -1, 1, 1, 7),  # ln 1, col 6-7
        #      ^
        ("line ?\r\nline 2", 5, -1, 1, 1, 7),  # ln 1, col 6-7
        #      ^

        # Range
        ("line 1", 5, 5, 1, 1, 6),  # ln 1, col 6
        #      ^
        ("line 1\nline 2", 12, 13, 2, 2, 7),  # ln 2, col 6-7
        #              ^
        ("line 1\rline 2", 12, 13, 2, 2, 7),  # ln 2, col 6-7
        #              ^
        ("line 1\r\nline 2", 13, 14, 2, 2, 7),  # ln 2, col 6-7
        #                ^
        ("line 1\nline 2\nline 3", 12, 19, 2, 3, 6),  # ln 2-3, col 6
        #              ^^^^^^^^
        ("line 1\rline 2\rline 3", 12, 19, 2, 3, 6),  # ln 2-3, col 6
        #              ^^^^^^^^
        ("line 1\r\nline 2\r\nline 3", 13, 21, 2, 3, 6),  # ln 2-3, col 6
        #                ^^^^^^^^^^
        ("line 1\nline 2\nline 3", 12, 20, 2, 3, 7),  # ln 2-3, col 6-7
        #              ^^^^^^^^^
        ("line 1\rline 2\rline 3", 12, 20, 2, 3, 7),  # ln 2-3, col 6-7
        #              ^^^^^^^^^
        ("line 1\r\nline 2\r\nline 3", 13, 22, 2, 3, 7),  # ln 2-3, col 6-7
        #                ^^^^^^^^^^^
    ],
)
def test_start_and_end_position(
    doc: str,
    start: int,
    end: int,
    lineno: int,
    end_lineno: int,
    end_colno: int,
) -> None:
    """Test start and end position."""
    exc: TruncatedSyntaxError = TruncatedSyntaxError("", "", doc, start, end)
    assert exc.lineno == lineno
    assert exc.end_lineno == end_lineno
    assert exc.colno == 6
    assert exc.end_colno == end_colno


@pytest.mark.parametrize(
    ("columns", "doc", "start", "end", "offset", "text", "end_offset"), [
        # Only current line
        (7, "current", 0, 7, 1, "current", 8),
        #    ^^^^^^^             ^^^^^^^
        (12, "current\nnext", 0, 7, 1, "current", 8),
        #     ^^^^^^^                   ^^^^^^^
        (12, "current\rnext", 0, 7, 1, "current", 8),
        #     ^^^^^^^                   ^^^^^^^
        (13, "current\r\nnext", 0, 7, 1, "current", 8),
        #     ^^^^^^^                     ^^^^^^^
        (16, "previous\ncurrent", 9, 16, 1, "current", 8),
        #               ^^^^^^^              ^^^^^^^
        (16, "previous\rcurrent", 9, 16, 1, "current", 8),
        #               ^^^^^^^              ^^^^^^^
        (17, "previous\r\ncurrent", 10, 17, 1, "current", 8),
        #                 ^^^^^^^               ^^^^^^^

        # Remove leading space
        (8, " current", 0, 8, 1, " current", 9),
        #    ^^^^^^^^             ^^^^^^^^
        (8, "\tcurrent", 0, 8, 1, " current", 9),
        #    ^^^^^^^^^             ^^^^^^^^
        (8, " current", 1, 8, 1, "current", 8),
        #     ^^^^^^^             ^^^^^^^
        (8, "\tcurrent", 1, 8, 1, "current", 8),
        #      ^^^^^^^             ^^^^^^^

        # Remove trailing space
        (8, "current ", 0, 8, 1, "current ", 9),
        #    ^^^^^^^^             ^^^^^^^^
        (8, "current\t", 0, 8, 1, "current ", 9),
        #    ^^^^^^^^^             ^^^^^^^^
        (8, "current ", 0, 7, 1, "current", 8),
        #    ^^^^^^^              ^^^^^^^
        (8, "current\t", 0, 7, 1, "current", 8),
        #    ^^^^^^^               ^^^^^^^

        # No newline
        (9, "start-end", 0, 5, 1, "start-end", 6),
        #    ^^^^^                 ^^^^^
        (8, "current\nnext", 0, 12, 1, "current", 5),
        #    ^^^^^^^^^^^^^              ^^^^^^^
        (8, "current\rnext", 0, 12, 1, "current", 5),
        #    ^^^^^^^^^^^^^              ^^^^^^^
        (8, "current\r\nnext", 0, 13, 1, "current", 5),
        #    ^^^^^^^^^^^^^^^              ^^^^^^^

        # Newline
        (8, "current", 7, 7, 8, "current", 9),
        #           ^                   ^
        (8, "current", 7, 8, 8, "current", 9),
        #           ^                   ^
        (8, "current\nnext", 7, 12, 8, "current", 5),
        #           ^^^^^^                     ^
        (8, "current\rnext", 7, 12, 8, "current", 5),
        #           ^^^^^^                     ^
        (8, "current\r\nnext", 7, 13, 8, "current", 5),
        #           ^^^^^^^^                     ^

        # At least one character
        (9, "start-end", 5, 5, 6, "start-end", 7),
        #         ^                     ^

        # Expand tabs
        (9, "start\tend", 5, 6, 6, "start end", 7),
        #         ^^                     ^

        # Replace unprintable characters
        (9, "start\x00end", 5, 6, 6, "start\ufffdend", 7),
        #         ^^^^                     ^^^^^^
        (9, "start\x1fend", 5, 6, 6, "start\ufffdend", 7),
        #         ^^^^                     ^^^^^^
        (9, "start\x7fend", 5, 6, 6, "start\ufffdend", 7),
        #         ^^^^                     ^^^^^^
        (9, "start\ud800end", 5, 6, 6, "start\ufffdend", 7),
        #         ^^^^^^                     ^^^^^^
        (9, "start\udfffend", 5, 6, 6, "start\ufffdend", 7),  # noqa: PT014
        #         ^^^^^^                     ^^^^^^

        # Truncate start
        (6, "start-middle-end", 13, 16, 4, "...end", 7),  # line_end
        #                 ^^^                  ^^^
        (7, "start-middle-end", 16, 17, 7, "...end", 8),  # newline
        #                    ^                    ^

        # Truncate middle
        (12, "start-middle-end", 0, 16, 1, "start...-end", 13),
        #     ^^^^^^^^^^^^^^^^              ^^^^^^^^^^^^
        (13, "start-middle-end", 0, 16, 1, "start...e-end", 14),
        #     ^^^^^^^^^^^^^^^^              ^^^^^^^^^^^^^

        # Truncate end
        (8, "start-middle-end", 0, 5, 1, "start...", 6),  # line_start
        #    ^^^^^                        ^^^^^

        # Truncate start and end
        (7, "start-middle-end", 5, 6, 4, "...-...", 5),
        #         ^                          ^
        (8, "start-middle-end", 5, 6, 5, "...t-...", 6),
        #         ^                           ^
        (11, "start-middle-end", 7, 11, 5, "...middl...", 9),
        #            ^^^^                       ^^^^
        (12, "start-middle-end", 7, 11, 5, "...middle...", 9),
        #            ^^^^                       ^^^^
        (13, "start-middle-end", 7, 11, 6, "...-middle...", 10),
        #            ^^^^                        ^^^^
    ],
)
def test_err_context(
    monkeypatch: pytest.MonkeyPatch,
    columns: int,
    doc: str,
    start: int,
    end: int,
    offset: int,
    text: str,
    end_offset: int,
) -> None:
    """Test error context."""
    monkeypatch.setenv("COLUMNS", str(4 + columns))  # leading spaces
    exc: TruncatedSyntaxError = TruncatedSyntaxError("", "", doc, start, end)
    assert exc.offset == offset
    assert exc.text == text
    assert exc.end_offset == end_offset


@pytest.mark.parametrize(("doc", "end", "line_range", "column_range"), [
    ("line 1", 5, "1", "6"),
    #      ^
    ("line 1", 6, "1", "6-7"),
    #      ^
    ("line 1\nline 2", 12, "1-2", "6"),
    #      ^^^^^^^^
    ("line 1\nline 2", 13, "1-2", "6-7"),
    #      ^^^^^^^^^
])
def test_string(
    doc: str, end: int, line_range: str, column_range: str,
) -> None:
    """Test string representation."""
    exc: TruncatedSyntaxError = TruncatedSyntaxError(
        "msg", "<string>", doc, 5, end,
    )
    expected: str = f"msg (<string>, line {line_range}, column {column_range})"
    assert str(exc) == expected
