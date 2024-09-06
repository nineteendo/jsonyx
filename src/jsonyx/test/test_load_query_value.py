# Copyright (C) 2024 Nice Zombies
"""JSON load_query_value tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []


from typing import Any

import pytest

# pylint: disable-next=W0611
from jsonyx import JSONSyntaxError, load_query_value


def _check_syntax_err(
    exc_info: pytest.ExceptionInfo[Any], msg: str, colno: int,
    end_colno: int = 0,
) -> None:
    exc: Any = exc_info.value
    if not end_colno:
        end_colno = colno

    assert exc.msg == msg
    assert exc.lineno == 1
    assert exc.end_lineno == 1
    assert exc.colno == colno
    assert exc.end_colno == end_colno


@pytest.mark.parametrize("s", ["", "foo"])
def test_expecting_value(s: str) -> None:
    """Test expecting JSON value."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s)

    _check_syntax_err(exc_info, "Expecting value", 1)
