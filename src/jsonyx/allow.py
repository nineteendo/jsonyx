# Copyright (C) 2024 Nice Zombies
"""Allow JSON deviations that don't require human intervention."""
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

#: Allow nothing
#:
#: Raises an error for all JSON deviations.
NOTHING: frozenset[str] = frozenset()

#: Allow comments
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("0 // line comment", allow=jsonyx.allow.COMMENTS)
#: 0
COMMENTS: frozenset[str] = frozenset({"comments"})

#: Allow duplicate keys
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS)
#: {'key': 'value 1', 'key': 'value 2'}
#:
#: See :class:`jsonyx.DuplicateKey` for more information.
DUPLICATE_KEYS: frozenset[str] = frozenset({"duplicate_keys"})

#: Allow missing commas
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("[1 2 3]", allow=jsonyx.allow.MISSING_COMMAS)
#: [1, 2, 3]
#:
#: .. note::
#:     Whitespace or a comment must be present if the comma is missing.
MISSING_COMMAS: frozenset[str] = frozenset({"missing_commas"})

#: Allow NaN and infinity
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads("NaN", allow=jsonyx.allow.NAN_AND_INFINITY)
#: nan
#: >>> json.dump(float("nan"), allow=jsonyx.allow.NAN_AND_INFINITY)
#: NaN
#:
#: .. note::
#:     ``Decimal("sNan")`` can't be (de)serialised this way.
NAN_AND_INFINITY: frozenset[str] = frozenset({"nan_and_infinity"})

#: Allow surrogates
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('"\ud800"', allow=jsonyx.allow.SURROGATES)
#: '\ud800'
#: >>> json.dump("\ud800", allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
#: "\ud800"
#:
#: .. note::
#:     If you're not using ``read()`` or ``write()``, you still need to set
#:     the unicode error handler to "surrogatepass".
SURROGATES: frozenset[str] = frozenset({"surrogates"})

#: Allow trailing comma
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('[0,]', allow=jsonyx.allow.TRAILING_COMMA)
#: [0]
TRAILING_COMMA: frozenset[str] = frozenset({"trailing_comma"})

#: Allow unquoted keys
#:
#: >>> import jsonyx as json
#: >>> import jsonyx.allow
#: >>> json.loads('{key: "value"}', allow=jsonyx.allow.UNQUOTED_KEYS)
#: {'key': 'value'}
#:
#: .. versionadded:: 2.0
UNQUOTED_KEYS: frozenset[str] = frozenset({"unquoted_keys"})

#: Allow everything
#:
#: Equivalent to ``COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS |
#: NAN_AND_INFINITY | SURROGATES | TRAILING_COMMA | UNQUOTED_KEYS``.
EVERYTHING: frozenset[str] = (
    COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS | NAN_AND_INFINITY | SURROGATES
    | TRAILING_COMMA | UNQUOTED_KEYS
)
