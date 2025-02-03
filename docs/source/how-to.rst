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

Encoding :mod:`numpy` objects
-----------------------------

>>> import jsonyx as json
>>> import numpy as np
>>> 
>>> obj = np.array([
...     np.bool(), np.int8(), np.uint8(), np.int16(), np.uint16(), np.int32(),
...     np.uint32(), np.intp(), np.uintp(), np.int64(), np.uint64(), np.float16(),
...     np.float32(), np.float64(), np.float128()
... ], dtype="O")
>>> types = {
...     "bool": np.bool,
...     "float": np.floating,
...     "int": np.integer,
...     "sequence": np.ndarray
... }
>>> json.dump(obj, types=types)
[false, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]

.. note:: If needed, you can also specify ``"mapping"`` or ``"str"``.

Specializing JSON object encoding
---------------------------------

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
>>> json.dump(to_json(1 + 2j))
{"__complex__": true, "real": 1.0, "imag": 2.0}

.. tip:: You can use :func:`functools.singledispatch` to make this extensible.

Specializing JSON object decoding
---------------------------------

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
>>> from_json(json.loads('{"__complex__": true, "real": 1.0, "imag": 2.0}'))
(1+2j)

.. note:: ``mapping_type`` is not intended for this purpose.

Disabling the integer string conversion length limit
----------------------------------------------------

>>> import jsonyx as json
>>> from sys import set_int_max_str_digits
>>> set_int_max_str_digits(0)
>>> json.loads("9" * 5_000) == 10 ** 5_000 - 1
True
>>> len(json.dumps(10 ** 5_000))
5002

See :ref:`int_max_str_digits` for more information.
