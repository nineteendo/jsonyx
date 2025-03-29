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

.. tabularcolumns:: \X{1}{2}\X{1}{2}

============ ========================================================================
Type         Required methods
============ ========================================================================
``"array"``  :meth:`~object.__len__`, and :meth:`~object.__iter__`
``"bool"``   :meth:`~object.__bool__`, :meth:`~object.__len__` or absent for ``true``
``"float"``  :meth:`~object.__str__` or :meth:`~object.__repr__`
``"int"``    :meth:`~object.__str__` or :meth:`~object.__repr__`
``"object"`` :meth:`~object.__len__`, :meth:`!values` and :meth:`!items`
``"str"``    :meth:`~object.__str__` or :meth:`~object.__repr__`
============ ========================================================================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> import numpy as np
>>> obj = np.array([
...     np.bool_(), np.int8(), np.uint8(), np.int16(), np.uint16(), np.int32(),
...     np.uint32(), np.intp(), np.uintp(), np.int64(), np.uint64(), np.float16(),
...     np.float32(), np.float64()
... ], dtype="O")
>>> types = {
...     "array": np.ndarray,
...     "bool": np.bool_,
...     "float": np.floating,
...     "int": np.integer
... }
>>> json.dump(obj, types=types)
[false, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0]

.. note:: Custom types must be registered manually, :mod:`jsonyx` does not
    infer serializability based on method presence.
.. warning:: Avoid specifying ABCs for ``types``, that is very slow.

.. _encoding_hook:

Encoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.1

>>> import jsonyx as json
>>> def complex_hook(obj):
...     if isinstance(obj, complex):
...         return {"__complex__": True, "real": obj.real, "imag": obj.imag}
...     return obj
... 
>>> json.dump(1 + 2j, hook=complex_hook)
{"__complex__": true, "real": 1.0, "imag": 2.0}

.. tip:: You can use :func:`functools.singledispatch` to make this extensible.
.. warning:: This function is called for **every object** during encoding, even
  if the object is normally serializable.
.. seealso:: The :mod:`pickle` and :mod:`shelve` modules which are better
    suited for this.

Decoding objects
----------------

.. _decoding_hooks:

Decoding objects using hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 2.0

.. tabularcolumns:: \X{1}{2}\X{1}{2}

============ =========================
Hook         Called with
============ =========================
``"array"``  :class:`list`
``"bool"``   :class:`bool`
``"float"``  :class:`str`
``"int"``    :class:`str`
``"object"`` ``list[tuple[Any, Any]]``
``"str"``    :class:`str`
============ =========================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> from functools import partial
>>> import numpy as np
>>> hooks = {
...     "array": partial(np.array, dtype="O"),
...     "bool": np.bool_,
...     "float": np.float64,
...     "int": np.int64
... }
>>> json.loads("[false, 0.0, 0]", hooks=hooks)
array([np.False_, np.float64(0.0), np.int64(0)], dtype=object)

Decoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> def object_hook(obj):
...     obj = dict(obj)
...     if "__complex__" in obj:
...         return complex(obj["real"], obj["imag"])
...     return obj
... 
>>> s = '{"__complex__": true, "real": 1.0, "imag": 2.0}'
>>> json.loads(s, hooks={"object": object_hook})
(1+2j)

.. warning:: The ``"object"`` hook is called with a list of tuples, not a dict.
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
