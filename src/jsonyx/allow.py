# Copyright (C) 2024 Nice Zombies
"""Allow JSON deviations not requiring human intervention."""
from __future__ import annotations

__all__: list[str] = [
    "COMMENTS",
    "DUPLICATE_KEYS",
    "EVERYTHING",
    "MISSING_COMMAS",
    "NAN_AND_INFINITY",
    "NOTHING",
    "SURROGATES",
    "TRAILING_COMMA",
    "UNQUOTED_KEYS",
]

#: Raise an error for all JSON deviations.
NOTHING: frozenset[str] = frozenset()

#: Allow block and line comments.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("0 /* Block */ // and line comment", allow=jsonyx.allow.COMMENTS)
#: 0
COMMENTS: frozenset[str] = frozenset({"comments"})

#: Allow duplicate keys in objects.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads(
#: ...     '{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS
#: ... )
#: {'key': 'value 1', 'key': 'value 2'}
#:
#: See :class:`jsonyx.DuplicateKey` for more information.
DUPLICATE_KEYS: frozenset[str] = frozenset({"duplicate_keys"})

#: Allow separating items with whitespace.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("[1 2 3]", allow=jsonyx.allow.MISSING_COMMAS)
#: [1, 2, 3]
MISSING_COMMAS: frozenset[str] = frozenset({"missing_commas"})

#: Allow NaN and (negative) infinity
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("[NaN, Infinity, -Infinity]", allow=jsonyx.allow.NAN_AND_INFINITY)
#: [nan, inf, -inf]
#: >>> from math import inf, nan
#: >>> json.dump([nan, inf, -inf], allow=jsonyx.allow.NAN_AND_INFINITY)
#: [NaN, Infinity, -Infinity]
#:
#: .. note::
#:     ``Decimal("sNan")`` can't be (de)serialised this way.
NAN_AND_INFINITY: frozenset[str] = frozenset({"nan_and_infinity"})

#: Allow unpaired surrogates in strings.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('"\ud800"', allow=jsonyx.allow.SURROGATES)
#: '\ud800'
#: >>> json.dump("\ud800", allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
#: "\ud800"
#:
#: .. hint::
#:     If you're not using ``read()`` or ``write()``, you still need to set
#:     the unicode error handler to "surrogatepass".
SURROGATES: frozenset[str] = frozenset({"surrogates"})

#: Allow a trailing comma at the end of arrays and objects.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('[0,]', allow=jsonyx.allow.TRAILING_COMMA)
#: [0]
TRAILING_COMMA: frozenset[str] = frozenset({"trailing_comma"})

#: Allow unquoted keys in objects which are identifiers.
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('{key: "value"}', allow=jsonyx.allow.UNQUOTED_KEYS)
#: {'key': 'value'}
#:
#: .. versionadded:: 2.0
UNQUOTED_KEYS: frozenset[str] = frozenset({"unquoted_keys"})

#: Allow all JSON deviations provided by :mod:`jsonyx`.
#:
#: Equivalent to ``COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS |
#: NAN_AND_INFINITY | SURROGATES | TRAILING_COMMA | UNQUOTED_KEYS``.
EVERYTHING: frozenset[str] = (
    COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS | NAN_AND_INFINITY | SURROGATES
    | TRAILING_COMMA | UNQUOTED_KEYS
)
