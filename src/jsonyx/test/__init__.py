# Copyright (C) 2024 Nice Zombies
"""JSON test utils."""
from __future__ import annotations

__all__: list[str] = ["check_syntax_err", "get_json"]

from test.support.import_helper import import_fresh_module  # type: ignore
from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import JSONSyntaxError

if TYPE_CHECKING:
    from types import ModuleType

pyjson: ModuleType | None = import_fresh_module("jsonyx", blocked=["_jsonyx"])
if cjson := import_fresh_module("jsonyx", fresh=["_jsonyx"]):
    # JSONSyntaxError is not cached inside the _jsonyx module
    cjson.JSONSyntaxError = JSONSyntaxError  # type: ignore


def check_syntax_err(
    exc_info: pytest.ExceptionInfo[Any], msg: str, colno: int = 1,
    end_colno: int = -1,
) -> None:
    """Check JSON syntax error."""
    exc: Any = exc_info.value
    if end_colno < 0:
        end_colno = colno

    assert exc.msg == msg
    assert exc.lineno == 1
    assert exc.end_lineno == 1
    assert exc.colno == colno
    assert exc.end_colno == end_colno


@pytest.fixture(params=[cjson, pyjson], ids=["cjson", "pyjson"], name="json")
def get_json(request: pytest.FixtureRequest) -> ModuleType:
    """Get JSON module."""
    json: ModuleType | None
    if (json := request.param) is None:
        pytest.xfail("module unavailable")
        pytest.fail("module unavailable")

    return json  # type: ignore[no-any-return]
