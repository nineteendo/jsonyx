"""pytest fixtures."""
from __future__ import annotations

__all__: list[str] = ["get_big_num", "get_json"]

import sys
from typing import TYPE_CHECKING

import pytest

from jsonyx import JSONSyntaxError

if TYPE_CHECKING:
    from types import ModuleType


if sys.version_info >= (3, 10):
    from test.support.import_helper import import_fresh_module  # type: ignore
else:
    from test.support import import_fresh_module

pyjson: ModuleType | None = import_fresh_module("jsonyx", blocked=["_jsonyx"])
if cjson := import_fresh_module("jsonyx", fresh=["_jsonyx"]):
    # JSONSyntaxError is not cached inside the _jsonyx module
    cjson.JSONSyntaxError = JSONSyntaxError  # type: ignore


@pytest.fixture(name="big_num")
def get_big_num() -> str:
    """Get big number."""
    if not hasattr(sys, "get_int_max_str_digits"):
        pytest.skip("requires integer string conversion length limit")

    return "1" + "0" * sys.get_int_max_str_digits()


@pytest.fixture(params=[cjson, pyjson], ids=["cjson", "pyjson"], name="json")
def get_json(request: pytest.FixtureRequest) -> ModuleType:
    """Get JSON module."""
    json: ModuleType | None
    if (json := request.param) is None:
        pytest.xfail("module unavailable")
        # pylint: disable-next=W0101
        pytest.fail("module unavailable")

    return json  # type: ignore[no-any-return]
