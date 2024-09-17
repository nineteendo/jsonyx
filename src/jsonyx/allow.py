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
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>> json.loads("0 /* Block */ // and line comment", allow=jsonyx.allow.COMMENTS)
#:     0
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.COMMENTS)
#:     >>> decoder.loads("0 /* Block */ // and line comment")
#:     0
COMMENTS: frozenset[str] = frozenset({"comments"})

#: Allow duplicate keys in objects.
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> json.loads(
#:     ...     '{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS
#:     ... )
#:     {'key': 'value 1', 'key': 'value 2'}
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.DUPLICATE_KEYS)
#:     >>> decoder.loads('{"key": "value 1", "key": "value 2"}')
#:     {'key': 'value 1', 'key': 'value 2'}
#:
#: See :class:`jsonyx.DuplicateKey` for more information.
DUPLICATE_KEYS: frozenset[str] = frozenset({"duplicate_keys"})

#: Allow separating items with whitespace.
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>> json.loads("[1 2 3]", allow=jsonyx.allow.MISSING_COMMAS)
#:     [1, 2, 3]
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.MISSING_COMMAS)
#:     >>> decoder.loads("[1 2 3]")
#:     [1, 2, 3]
#:
MISSING_COMMAS: frozenset[str] = frozenset({"missing_commas"})

#: Allow ``NaN``, ``Infinity`` and ``-Infinity``
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>>
#:     >>> json.loads("[NaN, Infinity, -Infinity]", allow=jsonyx.allow.NAN_AND_INFINITY)
#:     [nan, inf, -inf]
#:     >>> from math import inf, nan
#:     >>> json.dump([nan, inf, -inf], allow=jsonyx.allow.NAN_AND_INFINITY)
#:     [NaN, Infinity, -Infinity]
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.NAN_AND_INFINITY)
#:     >>> encoder = json.Encoder(allow=jsonyx.allow.NAN_AND_INFINITY)
#:     >>> decoder.loads("[NaN, Infinity, -Infinity]")
#:     [nan, inf, -inf]
#:     >>> from math import inf, nan
#:     >>> encoder.dump([nan, inf, -inf])
#:     [NaN, Infinity, -Infinity]
#:
#: .. note:: ``Decimal("sNan")`` can't be (de)serialised this way.
NAN_AND_INFINITY: frozenset[str] = frozenset({"nan_and_infinity"})

#: Allow unpaired surrogates in strings.
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>>
#:     >>> json.loads('"\ud800"', allow=jsonyx.allow.SURROGATES)
#:     '\ud800'
#:     >>> json.dump("\ud800", allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
#:     "\ud800"
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.SURROGATES)
#:     >>> encoder = json.Encoder(allow=jsonyx.allow.SURROGATES, ensure_ascii=True)
#:     >>> decoder.loads('"\ud800"')
#:     '\ud800'
#:     >>> encoder.dump("\ud800")
#:     "\ud800"
#:
#: .. tip:: If you're not using ``read()`` or ``write()``, you still need to
#      set the unicode error handler to ``"surrogatepass"``.
SURROGATES: frozenset[str] = frozenset({"surrogates"})

#: Allow a trailing comma at the end of arrays and objects.
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>> json.loads('[0,]', allow=jsonyx.allow.TRAILING_COMMA)
#:     [0]
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.TRAILING_COMMA)
#:     >>> decoder.loads('[0,]')
#:     [0]
TRAILING_COMMA: frozenset[str] = frozenset({"trailing_comma"})

#: Allow unquoted keys in objects which are identifiers.
#:
#: .. versionadded:: 2.0
#:
#: .. tab:: without classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: without classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>>
#:     >>> json.loads('{key: "value"}', allow=jsonyx.allow.UNQUOTED_KEYS)
#:     {'key': 'value'}
#:
#: .. tab:: with classes
#:
#:     .. only:: latex
#:
#:         .. rubric:: with classes
#:
#:     >>> import jsonyx as json
#:     >>> import jsonyx.allow
#:     >>> decoder = json.Decoder(allow=jsonyx.allow.UNQUOTED_KEYS)
#:     >>> decoder.loads('{key: "value"}')
#:     {'key': 'value'}
UNQUOTED_KEYS: frozenset[str] = frozenset({"unquoted_keys"})

#: Allow all JSON deviations provided by :mod:`jsonyx`.
#:
#: This is equivalent to ``COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS |
#: NAN_AND_INFINITY | SURROGATES | TRAILING_COMMA | UNQUOTED_KEYS``.
EVERYTHING: frozenset[str] = (
    COMMENTS | DUPLICATE_KEYS | MISSING_COMMAS | NAN_AND_INFINITY | SURROGATES
    | TRAILING_COMMA | UNQUOTED_KEYS
)
