How-to Guide
============

Encoding and decoding protocol-based objects
--------------------------------------------

.. versionadded:: 2.0

.. _additional_types:

Encoding protocol-based objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionchanged:: 2.4 Made :class:`frozendict` serializable by default.

By default, protocol types are encoded from instances of the corresponding
Python types shown below. Additional types can be registered with ``types``.

.. tabularcolumns:: \X{1}{4}\X{1}{4}\X{1}{2}
.. table::
    :class: longtable

    ============ ===================================== ===================================================================================
    Type         Default                               Required methods
    ============ ===================================== ===================================================================================
    ``"array"``  :class:`list` and :class:`tuple`      :meth:`~object.__iter__` or :meth:`~object.__len__` and :meth:`~object.__getitem__`
    ``"bool"``   ``True`` and ``False``                :meth:`~object.__bool__`, :meth:`~object.__len__` or neither (``true``)
    ``"float"``  :class:`float`                        :meth:`~object.__str__` or :meth:`~object.__repr__`
    ``"int"``    :class:`int`                          :meth:`~object.__str__` or :meth:`~object.__repr__`
    ``"null"``   ``None``                              none (not extensible)
    ``"object"`` :class:`dict` and :class:`frozendict` :meth:`!values` and :meth:`!items`
    ``"str"``    :class:`str`                          :meth:`~object.__str__` or :meth:`~object.__repr__`
    ============ ===================================== ===================================================================================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> import numpy as np
>>> obj = np.array([
...     np.bool_(), np.int8(), np.uint8(), np.int16(), np.uint16(), np.int32(),
...     np.uint32(), np.intp(), np.uintp(), np.int64(), np.uint64(), np.float16(),
...     np.float32(), np.float64(), np.str_()
... ], dtype="O")
>>> types = {
...     "array": np.ndarray,
...     "bool": np.bool_,
...     "float": np.floating,
...     "int": np.integer,
...     "str": np.str_
... }
>>> json.dump(obj, types=types)
[false, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, ""]

.. note:: Custom types must be registered manually, :mod:`jsonyx` does not
    infer serializability based on method presence.
.. warning:: Avoid specifying ABCs for ``types``, that is very slow.

.. _decoding_hooks:

Decoding protocol-based objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, decoded protocol types are converted to the corresponding Python
types shown below. The conversion can be customized with ``hooks``.

.. tabularcolumns:: \X{1}{4}\X{1}{4}\X{1}{2}
.. table::
    :class: longtable

    ============ ======================= ===============================
    Hook         Default                 Called with
    ============ ======================= ===============================
    ``"array"``  :class:`list`           :class:`list`
    ``"bool"``   :class:`bool`           ``True`` or ``False``
    ``"float"``  :class:`float`          :class:`str`
    ``"int"``    :class:`int`            :class:`str`
    ``"null"``   :class:`types.NoneType` nothing (not customizable)
    ``"object"`` :class:`dict`           ``list[tuple[Any, Any]]``
    ``"str"``    :class:`str`            :class:`str`
    ============ ======================= ===============================

Example with :mod:`numpy`:

>>> import jsonyx as json
>>> from functools import partial
>>> import numpy as np
>>> hooks = {
...     "array": partial(np.array, dtype="O"),
...     "bool": np.bool_,
...     "float": np.float64,
...     "int": np.int64,
...     "str": np.str_
... }
>>> json.loads('[false, 0.0, 0, ""]', hooks=hooks)
array([np.False_, np.float64(0.0), np.int64(0), np.str_('')], dtype=object)

Using :class:`decimal.Decimal` instead of :class:`float`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> from decimal import Decimal
>>> json.loads("1.1", hooks={"float": Decimal})
Decimal('1.1')
>>> json.dump(Decimal('1.1'), types={"float": Decimal})
1.1

Using :class:`multidict.MultiDict` instead of :class:`dict`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> from multidict import MultiDict
>>> json.loads('{"a": 1, "a": 2, "a": 3}', hooks={"object": MultiDict})
<MultiDict('a': 1, 'a': 2, 'a': 3)>
>>> obj = MultiDict([('a', 1), ('a', 2), ('a', 3)])
>>> json.dump(obj, types={"object": MultiDict})
{"a": 1, "a": 2, "a": 3}

Encoding and decoding arbitrary objects
---------------------------------------

.. versionadded:: 2.1

.. _encoding_hook:

Encoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> from functools import singledispatch
>>> @singledispatch
... def type_to_obj_hook(obj):
...     return obj
... 
>>> @type_to_obj_hook.register(complex)
... def complex_to_obj_hook(obj):
...     return {"__type__": "complex", "real": obj.real, "imag": obj.imag}
... 
>>> json.dump(1 + 2j, hook=type_to_obj_hook)
{"__type__": "complex", "real": 1.0, "imag": 2.0}

.. warning:: This function is called for **every object** during encoding, even
  if the object is normally serializable.
.. seealso:: The :mod:`pickle` and :mod:`shelve` modules which are better
    suited for this.

Decoding arbitrary objects
^^^^^^^^^^^^^^^^^^^^^^^^^^

>>> import jsonyx as json
>>> obj_to_type_hooks = {}
>>> def obj_to_type_hook(items):
...     obj = dict(items)
...     if "__type__" in obj:
...         return obj_to_type_hooks[obj["__type__"]](obj)
...     return obj
... 
>>> def obj_to_complex_hook(obj):
...     return complex(obj["real"], obj["imag"])
... 
>>> obj_to_type_hooks["complex"] = obj_to_complex_hook
>>> s = '{"__type__": "complex", "real": 1.0, "imag": 2.0}'
>>> json.loads(s, hooks={"object": obj_to_type_hook})
(1+2j)

.. note:: ``hooks["object"]`` is called with a list of tuples, not a dict.
.. seealso:: The :mod:`pickle` and :mod:`shelve` modules which are better
    suited for this.

.. _compact_float_formatter:
.. _formatters:

Formatting numbers
------------------

.. versionadded:: 2.4

By default, numbers are formatted using :class:`str`. Custom formatters can
be registered with ``formatters``. Formatters must return a string containing
a valid JSON number.

.. tabularcolumns:: \X{1}{4}\X{1}{4}\X{1}{2}
.. table::
    :class: longtable

    ============ ============= ====================================
    Formatter    Default       Called with
    ============ ============= ====================================
    ``"float"``  :class:`str`  :class:`float` or ``types["float"]``
    ``"int"``    :class:`str`  :class:`int` or ``types["int"]``
    ============ ============= ====================================

Compact float example:

>>> import jsonyx as json
>>> def compact_float_formatter(x):
...     if "e" in (scientific := f"{x:.16e}"): # skip NaN and infinity
...         mantissa, exp = scientific.split("e")
...         mantissa = mantissa.rstrip("0").rstrip(".")
...         scientific = f"{mantissa}e{int(exp)}"
...     return min(repr(x), scientific, key=len)
... 
>>> json.dump([0.001, 10.0], formatters={"float": compact_float_formatter})
[1e-3, 1e1]

.. note:: Case variations of ``"nan"``, ``"inf"``, ``"infinity"``, ``"-inf"``
    and ``"-infinity"`` are normalized.

Encoding :class:`enum.ReprEnum`
-------------------------------

>>> import jsonyx as json
>>> from enum import ReprEnum
>>> class MyEnum(int, ReprEnum):
...     ZERO = 0
... 
>>> json.dump(MyEnum.ZERO)
0

.. warning:: Don't use :class:`enum.Enum`, because it overrides the string
    representation.

Encoding and decoding big integers
----------------------------------

Python has a global limit for converting between :class:`int` and :class:`str`.
If you need to process integers exceeding this limit, use
:func:`sys.set_int_max_str_digits` to increase it:

>>> import jsonyx as json
>>> from sys import set_int_max_str_digits
>>> set_int_max_str_digits(0)
>>> json.loads("9" * 5_000) == 10 ** 5_000 - 1
True
>>> len(json.dumps(10 ** 5_000))
5002

See :ref:`int_max_str_digits` for more information.

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

.. versionadded:: 2.0

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

.. versionadded:: 2.0

>>> import jsonyx as json
>>> try:
...     b"caf\xe9".decode("ascii")
... except UnicodeDecodeError as exc:
...     doc = exc.object.decode(exc.encoding, "replace")
...     start = exc.object[:exc.start].decode(exc.encoding, "replace")
...     end = exc.object[:exc.end].decode(exc.encoding, "replace")
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
