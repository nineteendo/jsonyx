How-to Guide
============

Specializing JSON object encoding
---------------------------------

To specialize JSON object encoding, you can write a converter function::

    >>> import jsonyx as json
    >>> from collections.abc import Mapping, Sequence
    >>> 
    >>> def to_json(obj):
    ...     if isinstance(obj, Sequence):
    ...         return [to_json(value) for value in obj]
    ...     if isinstance(obj, Mapping):
    ...         return {key: to_json(value) for key, value in obj.items()}
    ...     if isinstance(obj, complex):
    ...         return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    ...     return obj
    ... 
    >>> json.dump(to_json(1 + 2j))
    {"__complex__": true, "real": 1.0, "imag": 2.0}

Specializing JSON object decoding
---------------------------------

To specialize JSON object decoding, you can write a converter function::

    >>> import jsonyx as json
    >>> 
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         if "__complex__" in obj:
    ...             return complex(obj["real"], obj["imag"])
    ...         return {key: from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> from_json(json.loads('{"__complex__": true, "real": 1.0, "imag": 2.0}'))
    (1+2j)

Removing duplicate keys
^^^^^^^^^^^^^^^^^^^^^^^

To remove duplicate keys, they can be converted to regular strings::

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> 
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {str(key): from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> from_json(json.loads('{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS))
    {'key': 'value 2'}