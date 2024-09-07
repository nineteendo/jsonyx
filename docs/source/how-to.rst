How-to Guide
============

Better error messages for other JSON libraries
----------------------------------------------

::

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

::

    >>> import jsonyx as json
    >>> 
    >>> def to_json(obj):
    ...     if isinstance(obj, list):
    ...         return [to_json(value) for value in obj]
    ...     if isinstance(obj, dict):
    ...         return {key: to_json(value) for key, value in obj.items()}
    ...     if isinstance(obj, complex):
    ...         return {"__complex__": True, "real": obj.real, "imag": obj.imag}
    ...     return obj
    ... 
    >>> json.dump(to_json(1 + 2j))
    {"__complex__": true, "real": 1.0, "imag": 2.0}

.. note::
    This simple example doesn't convert :class:`collections.abc.Mapping` and
    :class:`collections.abc.Sequence`.

Specializing JSON object decoding
---------------------------------

::

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

::

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
    >>> from_json(json.loads(
    ...     '{"key": "value 1", "key": "value 2"}', allow=jsonyx.allow.DUPLICATE_KEYS
    ... ))
    {'key': 'value 2'}

.. _use_multidict:

Using :class:`multidict.MultiDict` instead of :class:`dict`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After installing ``multidict``, it can be used like this::

    >>> import jsonyx as json
    >>> import jsonyx.allow
    >>> from multidict import MultiDict
    >>> 
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

.. note::
    :class:`multidict.MultiDict` can be natively serialized.