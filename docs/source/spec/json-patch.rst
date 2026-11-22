JSON Patch
==========

A format for describing changes to a JSON document.

.. versionadded:: 2.0

The patch documents are themselves JSON documents, consisting of a
single operation or an array of operations.

Example
-------

Input:

.. code-block:: json

    {"baz": "qux", "foo": "bar"}

Patch:

.. code-block:: json

    [
        {"op": "set", "path": "$.baz", "value": "boo"},
        {"op": "set", "path": "$.hello", "value": ["world"]},
        {"op": "del", "path": "$.foo"}
    ]

Output:

.. code-block:: json

    {"baz": "boo", "hello": ["world"]}

Schema
------

https://github.com/nineteendo/jsonyx/blob/2.5.x/json-patch.schema.json

Operations
----------

append
^^^^^^

Append a value to the end of an array.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"append"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **value** (:ref:`any <any>`) - a value.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "append", "value": 4}

    Output:

    .. code-block:: json

        [1, 2, 3, 4]

assert
^^^^^^

Test if a condition is true.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"assert"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` where the expression is evaluated.
    - **expr** (:ref:`string`) - an :ref:`expression <expression>`.
    - **msg** (:ref:`string`, default: :json:`"Path <path>: <expr>"`): an error
      message

Example:
    Input:

    .. code-block:: json

        false

    Good patch:

    .. code-block:: json

        {"op": "assert", "expr": "@ == false"}

    Bad patch:

    .. code-block:: json

        {"op": "assert", "expr": "@ == true"}

clear
^^^^^

Remove all items from an array or all properties from an object.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"clear"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the array or object.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "clear"}

    Output:

    .. code-block:: json

        []

.. _copy:

copy
^^^^

Copy a value.

.. versionchanged:: 2.5 Made :json:`"set"` the default paste mode.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"copy"`.
    - **mode** (:ref:`string`, default: :json:`"set"`) - the paste mode. Must
      be:

      - :json:`"append"` - append the source value to the end of a target
        array.
      - :json:`"extend"` - extend the target array with the values of the
        source array.
      - :json:`"insert"` - insert the source value at the specified index in
        the target array. In this mode, the **to** field is required.
      - :json:`"set"` - replace the target value with the source value.
      - :json:`"update"` - update the target object with the properties of the
        source object, overwriting existing properties.

    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` where the operation is applied.
    - **from** (:ref:`string`) - the
      :ref:`relative path <relative_path>` to the source value.
    - **to** (:ref:`string`, default: :json:`"@"`) - the
      :ref:`relative path <relative_path>` to the target value.

Example:
    Input:

    .. code-block:: json

        {"a": 0}

    Patch:

    .. code-block:: json

        {"op": "copy", "from": "@.a", "to": "@.b"}

    Output:

    .. code-block:: json

        {"a": 0, "b": 0}

.. note:: You can't use a :ref:`filter` in the **from** and **to** fields.

del
^^^

Delete an item from an array or a property from an object.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be :json:`"del"`.
    - **path** (:ref:`string`) - the :ref:`absolute path <absolute_path>` to
      the item.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "del", "path": "$[1]"}

    Output:

    .. code-block:: json

        [1, 3]

.. tip:: A :ref:`filter` is more robust than an index.

extend
^^^^^^

Extend an array with the values of another array.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"extend"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **values** (:ref:`array`) - another array.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "extend", "values": [4, 5, 6]}

    Output:

    .. code-block:: json

        [1, 2, 3, 4, 5, 6]

insert
^^^^^^

Insert a value at the specified index in an array.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"insert"`.
    - **path** (:ref:`string`) - the :ref:`absolute path <absolute_path>` with
      the index in the array.
    - **value** (:ref:`any <any>`) - a value.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "insert", "path": "$[0]", "value": 0}

    Output:

    .. code-block:: json

        [0, 1, 2, 3]

.. tip:: A :ref:`filter` is more robust than an index.

.. _move:

move
^^^^

Move a value.

.. versionchanged:: 2.5 Made :json:`"set"` the default paste mode.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"move"`.
    - **mode** (:ref:`string`, default: :json:`"set"`) - the paste mode. Must
      be:

      - :json:`"append"` - append the source value to the end of a target
        array.
      - :json:`"extend"` - extend the target array with the values of the
        source array.
      - :json:`"insert"` - insert the source value at the specified index in
        the target array. In this mode, the **to** field is required.
      - :json:`"set"` - replace the target value with the source value.
      - :json:`"update"` - update the target object with the items of the
        source object, overwriting existing properties.

    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` where the operation is applied.
    - **from** (:ref:`string`) - the
      :ref:`relative path <relative_path>` to the source value.
    - **to** (:ref:`string`, default: :json:`"@"`) - the
      :ref:`relative path <relative_path>` to the target value.

Example:
    Input:

    .. code-block:: json

        {"a": 0}

    Patch:

    .. code-block:: json

        {"op": "move", "from": "@.a", "to": "@.b"}

    Output:

    .. code-block:: json

        {"b": 0}

.. note:: You can't use a :ref:`filter` in the **from** and **to** fields.

reverse
^^^^^^^

Reverse the items from an array.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"reverse"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the array.

Example:
    Input:

    .. code-block:: json

        [1, 2, 3]

    Patch:

    .. code-block:: json

        {"op": "reverse"}

    Output:

    .. code-block:: json

        [3, 2, 1]

set
^^^

Replace an item of an array, a property of an object or the root.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be :json:`"set"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the value.
    - **value** (:ref:`any <any>`) - a value.

Example:
    Input:

    .. code-block:: json

        false

    Patch:

    .. code-block:: json

        {"op": "set", "value": true}

    Output:

    .. code-block:: json

        true

sort
^^^^

Sort an array.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"sort"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **reverse** (:ref:`boolean <boolean>`, default: :json:`false`) - sort in
      descending order.

Example:
    Input:

    .. code-block:: json

        [3, 1, 2]

    Patch:

    .. code-block:: json

        {"op": "sort"}

    Output:

    .. code-block:: json

        [1, 2, 3]

update
^^^^^^

Update an object with the properties of another object, overwriting existing
properties.

Fields:
    - **op** (:ref:`string`) - the operation to perform. Must be
      :json:`"update"`.
    - **path** (:ref:`string`, default: :json:`"$"`) - the
      :ref:`absolute path <absolute_path>` to the object.
    - **properties** (:ref:`object`) - another object.

Example:
    Input:

    .. code-block:: json

        {"a": 1, "b": 2, "c": 3}

    Patch:

    .. code-block:: json

        {"op": "update", "properties": {"a": 4, "b": 5, "c": 6}}

    Output:

    .. code-block:: json

        {"a": 4, "b": 5, "c": 6}
