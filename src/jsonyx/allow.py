"""Allow JSON deviations not requiring human intervention."""
from __future__ import annotations

__all__: list[str] = [
    "COMMENTS",
    "EVERYTHING",
    "MISSING_COMMAS",
    "NAN_AND_INFINITY",
    "NOTHING",
    "SURROGATES",
    "TRAILING_COMMA",
    "UNQUOTED_KEYS",
]

NOTHING: frozenset[str] = frozenset()
"""Raise an error for all JSON deviations."""

COMMENTS: frozenset[str] = frozenset({"comments"})
"""Allow block and line comments.

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads("0 /* Block */ // and line comment", allow=jsonyx.allow.COMMENTS)
0
"""

MISSING_COMMAS: frozenset[str] = frozenset({"missing_commas"})
"""Allow separating items with whitespace.

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads("[1 2 3]", allow=jsonyx.allow.MISSING_COMMAS)
[1, 2, 3]
"""

NAN_AND_INFINITY: frozenset[str] = frozenset({"nan_and_infinity"})
"""Allow ``NaN``, ``Infinity`` and ``-Infinity``

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads("[NaN, Infinity, -Infinity]", allow=jsonyx.allow.NAN_AND_INFINITY)
[nan, inf, -inf]
>>> from math import inf, nan
>>> json.dump([nan, inf, -inf], allow=jsonyx.allow.NAN_AND_INFINITY)
[NaN, Infinity, -Infinity]

.. note:: ``Decimal("sNan")`` can't be (de)serialised this way.
"""

SURROGATES: frozenset[str] = frozenset({"surrogates"})
r"""Allow unpaired surrogates in strings.

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads('"\ud800"', allow=jsonyx.allow.SURROGATES)
'\ud800'
>>> json.dump("\ud800", allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
"\ud800"

.. tip:: If you're not using ``read()`` or ``write()``, you still need to
    set the unicode error handler to ``"surrogatepass"``.
"""

TRAILING_COMMA: frozenset[str] = frozenset({"trailing_comma"})
"""Allow a trailing comma at the end of arrays and objects.

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads('[0,]', allow=jsonyx.allow.TRAILING_COMMA)
[0]
"""

UNQUOTED_KEYS: frozenset[str] = frozenset({"unquoted_keys"})
"""Allow unquoted keys in objects which are identifiers.

.. versionadded:: 2.0

>>> import jsonyx as json
>>> import jsonyx.allow
>>> json.loads('{key: "value"}', allow=jsonyx.allow.UNQUOTED_KEYS)
{'key': 'value'}
"""

EVERYTHING: frozenset[str] = (
    COMMENTS | MISSING_COMMAS | NAN_AND_INFINITY | SURROGATES | TRAILING_COMMA
    | UNQUOTED_KEYS
)
"""Allow all JSON deviations.

.. versionchanged:: 2.0 Excluded :data:`!jsonyx.allow.DUPLICATE_KEYS`.
    Included :data:`jsonyx.allow.UNQUOTED_KEYS`.

This is equivalent to ``COMMENTS | MISSING_COMMAS | NAN_AND_INFINITY
| SURROGATES | TRAILING_COMMA | UNQUOTED_KEYS``.
"""
