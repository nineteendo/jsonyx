How-to Guide
============

Better error messages
---------------------

Better error messages for other JSON libraries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import json, jsonyx
>>> try:
...     json.loads("[,]")
... except json.JSONDecodeError as exc:
...     raise jsonyx.JSONSyntaxError(exc.msg, "<string>", exc.doc, exc.pos) from None
...
Traceback (most recent call last):
  File "<string>", line 1, column 2
    [,]
     ^
jsonyx.JSONSyntaxError: Expecting value

Better error messages for encoding strings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> try:
...     "café".encode("ascii")
... except UnicodeEncodeError as exc:
...     raise json.TruncatedSyntaxError(
...         f"(unicode error) {exc}", "<string>", exc.object, exc.start, exc.end,
...     ) from None
...
Traceback (most recent call last):
  File "<string>", line 1, column 4-5
    café
       ^
jsonyx.TruncatedSyntaxError: (unicode error) 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)

.. _better_decoding_error:

Better error messages for decoding bytes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> try:
...     b"caf\xe9".decode("ascii")
... except UnicodeDecodeError as exc:
...     doc = exc.object.decode("ascii", "replace")
...     start = exc.object[:exc.start].decode("ascii", "replace")
...     end = exc.object[:exc.end].decode("ascii", "replace")
...     raise json.TruncatedSyntaxError(
...         f"(unicode error) {exc}", "<string>", doc, len(start), len(end),
...     ) from None
...
Traceback (most recent call last):
  File "<string>", line 1, column 4-5
    caf�
       ^
jsonyx.TruncatedSyntaxError: (unicode error) 'ascii' codec can't decode byte 0xe9 in position 3: ordinal not in range(128)

.. seealso:: :func:`jsonyx.format_syntax_error` for formatting the exception.

Encoding objects
----------------

.. _protocol_types:

Encoding protocol-based objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

============== ========================================================================
Type           Required methods
============== ========================================================================
``"bool"``     :meth:`~object.__bool__`, :meth:`~object.__len__` or absent for ``true``
``"float"``    :meth:`~object.__float__` or :meth:`~object.__index__`
``"int"``      :meth:`~object.__int__` or :meth:`~object.__index__`
``"mapping"``  :meth:`~object.__len__`, :meth:`!values` and :meth:`!items`
``"sequence"`` :meth:`~object.__len__`, and :meth:`~object.__iter__`
``"str"``      :meth:`~object.__str__` or :meth:`~object.__repr__`
============== ========================================================================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> import numpy as np
>>> obj = np.array([
...     np.bool_(), np.int8(), np.uint8(), np.int16(), np.uint16(), np.int32(),
...     np.uint32(), np.intp(), np.uintp(), np.int64(), np.uint64(), np.float16(),
...     np.float32(), np.float64(), np.float128()
... ], dtype="O")
>>> types = {
...     "bool": np.bool_,
...     "float": np.floating,
...     "int": np.integer,
...     "sequence": np.ndarray
... }
>>> json.dump(obj, types=types)
[false, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]

.. note:: Custom types must be registered manually, :mod:`jsonyx` does not
    infer serializability based on method presence.
.. warning:: Avoid specifying ABCs for ``types``, that is very slow.

Encoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

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
.. seealso:: The :mod:`pickle` and :mod:`shelve` modules which are better
    suited for this.

Decoding objects
----------------

.. _using_hooks:

Decoding objects using hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

============== =========================
Hook           Called with
============== =========================
``"bool"``     :class:`bool`
``"float"``    :class:`float`
``"int"``      :class:`int`
``"mapping"``  ``list[tuple[Any, Any]]``
``"sequence"`` :class:`list`
``"str"``      :class:`str`
============== =========================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> from functools import partial
>>> import numpy as np
>>> hooks = {
...     "bool": np.bool_,
...     "float": np.float64,
...     "int": np.int64,
...     "sequence": partial(np.array, dtype="O")
... }
>>> json.loads("[false, 0.0, 0]", hooks=hooks)
array([np.False_, np.float64(0.0), np.int64(0)], dtype=object)

Decoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. note:: The ``"mapping"`` hook is not intended for this purpose.
.. seealso:: The :mod:`pickle` and :mod:`shelve` modules which are better
    suited for this.

Encoding and decoding big integers
----------------------------------

>>> import jsonyx as json
>>> from sys import set_int_max_str_digits
>>> set_int_max_str_digits(0)
>>> json.loads("9" * 5_000) == 10 ** 5_000 - 1
True
>>> len(json.dumps(10 ** 5_000))
5002

See :ref:`int_max_str_digits` for more information.
