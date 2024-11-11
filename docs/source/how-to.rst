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

.. seealso:: :func:`jsonyx.format_syntax_error` for formatting the exception.

Specializing JSON object encoding
---------------------------------

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

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

    .. only:: latex

        .. rubric:: with classes

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

    .. only:: latex

        .. rubric:: without classes

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

    .. only:: latex

        .. rubric:: with classes

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

Disabling the integer string conversion length limit
----------------------------------------------------

.. tab:: without classes

    .. only:: latex

        .. rubric:: without classes

    >>> import jsonyx as json
    >>> from sys import set_int_max_str_digits
    >>>
    >>>
    >>> set_int_max_str_digits(0)
    >>> json.loads("9" * 5_000) == 10 ** 5_000 - 1
    True
    >>> len(json.dumps(10 ** 5_000))
    5002

.. tab:: with classes

    .. only:: latex

        .. rubric:: with classes

    >>> import jsonyx as json
    >>> from sys import set_int_max_str_digits
    >>> decoder = json.Decoder()
    >>> encoder = json.Encoder()
    >>> set_int_max_str_digits(0)
    >>> decoder.loads("9" * 5_000) == 10 ** 5_000 - 1
    True
    >>> len(encoder.dumps(10 ** 5_000))
    5002

See :ref:`int_max_str_digits` for more information.
