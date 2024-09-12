How-to Guide
============

Better error messages for other JSON libraries
----------------------------------------------

>>> import jsonyx
>>> from json import JSONDecodeError, loads
>>> try:
...     loads("[,]")
... except JSONDecodeError as exc:
...     raise jsonyx.JSONSyntaxError(exc.msg, "<string>", exc.doc, exc.pos) from None
...
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "<string>", line 1
    [,]
     ^
jsonyx.JSONSyntaxError: Expecting value

.. tip::
    Use :func:`jsonyx.format_syntax_error` for formatting the exception.

Specializing JSON object encoding
---------------------------------

.. tab:: without classes

    >>> import jsonyx as json
    >>> def to_json(obj):
    ...     if isinstance(obj, list):
    ...         return [to_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {key: to_json(value) for key, value in obj.items()}
    ...     if isinstance(obj, complex):
    ...         return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    ...     return obj
    ... 
    >>> 
    >>> json.dump(to_json(1 + 2j))
    {"__complex__": true, "real": 1.0, "imag": 2.0}

.. tab:: with classes

    >>> import jsonyx as json
    >>> def to_json(obj):
    ...     if isinstance(obj, list):
    ...         return [to_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {key: to_json(value) for key, value in obj.items()}
    ...     if isinstance(obj, complex):
    ...         return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    ...     return obj
    ... 
    >>> encoder = json.Encoder()
    >>> encoder.dump(to_json(1 + 2j))
    {"__complex__": true, "real": 1.0, "imag": 2.0}

Specializing JSON object decoding
---------------------------------

.. tab:: without classes

    >>> import jsonyx as json
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         if "__complex__" in obj:
    ...             return complex(obj["real"], obj["imag"])
    ...         return {key: from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> 
    >>> from_json(json.loads('{"__complex__": true, "real": 1.0, "imag": 2.0}'))
    (1+2j)

.. tab:: with classes

    >>> import jsonyx as json
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         if "__complex__" in obj:
    ...             return complex(obj["real"], obj["imag"])
    ...         return {key: from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> decoder = json.Decoder()
    >>> from_json(decoder.loads('{"__complex__": true, "real": 1.0, "imag": 2.0}'))
    (1+2j)

Removing duplicate keys
^^^^^^^^^^^^^^^^^^^^^^^

.. tab:: without classes

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {str(key): from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> from_json(json.loads(
    ...     '{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS
    ... ))
    {'key': 'value 2'}

.. tab:: with classes

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {str(key): from_json(value) for key, value in obj.items()}
    ...     return obj
    ... 
    >>> 
    >>> decoder = json.Decoder(allow=jsonyx.allow.DUPLICATE_KEYS)
    >>> from_json(decoder.loads('{"key": "value 1", "key": "value 2"}'))
    {'key': 'value 2'}

.. _use_multidict:

Using :class:`multidict.MultiDict` instead of :class:`dict`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After installing :pypi:`multidict`, it can be used like this:

.. tab:: without classes

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> from multidict import MultiDict
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return MultiDict({key: from_json(value) for key, value in obj.items()})
    ...     return obj
    ... 
    >>> from_json(json.loads(
    ...     '{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS
    ... ))
    <MultiDict('key': 'value 1', 'key': 'value 2')>

.. tab:: with classes

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> from multidict import MultiDict
    >>> def from_json(obj):
    ...     if isinstance(obj, list):
    ...         return [from_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return MultiDict({key: from_json(value) for key, value in obj.items()})
    ...     return obj
    ... 
    >>> 
    >>> decoder = json.Decoder(allow=jsonyx.allow.DUPLICATE_KEYS)
    >>> from_json(decoder.loads('{"key": "value 1", "key": "value 2"}'))
    <MultiDict('key': 'value 1', 'key': 'value 2')>
