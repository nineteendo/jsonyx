"""JSON test utils."""
from __future__ import annotations

__all__: list[str] = ["check_syntax_err"]

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pytest


def check_syntax_err(
    exc_info: pytest.ExceptionInfo[Any],
    msg: str,
    colno: int = 1,
    end_colno: int = -1,
) -> None:
    """Check truncated syntax error."""
    exc: Any = exc_info.value
    if end_colno < 0:
        end_colno = colno

    assert exc.msg == msg
    assert exc.lineno == 1
    assert exc.end_lineno == 1
    assert exc.colno == colno
    assert exc.end_colno == end_colno
