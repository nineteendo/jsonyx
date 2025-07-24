JSON Patch Specification
========================

JSON Patch is a format for describing changes to a `JSON <https://json.org>`_
document.

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

https://github.com/nineteendo/jsonyx/blob/2.3.x/json-patch.schema.json

Operations
----------

append
^^^^^^

Append a value to the end of an array.

Fields:
    - **op** (string) - the operation to perform. Must be ``"append"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **value** (any) - a value.

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
    - **op** (string) - the operation to perform. Must be ``"assert"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` where the expression is evaluated.
    - **expr** (string) - :ref:`an expression <expression>`.
    - **msg** (string, default: ``"Path <path>: <expr>"``): an error message

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
    - **op** (string) - the operation to perform. Must be ``"clear"``.
    - **path** (string, default: ``"$"``) - the
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

Fields:
    - **op** (string) - the operation to perform. Must be ``"copy"``.
    - **mode** (string) - the paste mode. Must be:

      - ``"append"`` - append the source value to the end of a target array.
      - ``"extend"`` - extend the target array with the values of the source
        array.
      - ``"insert"`` - insert the source value at the specified index in the
        target array. In this mode, the **to** field is required.
      - ``"set"`` - replace the target value with the source value.
      - ``"update"`` - update the target object with the properties of the
        source object, overwriting existing properties.

    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` where the operation is applied.
    - **from** (string) - the
      :ref:`relative path <relative_path>` to the source value.
    - **to** (string, default: ``"@"``) - the
      :ref:`relative path <relative_path>` to the target value.

Example:
    Input:

    .. code-block:: json

        {"a": 0}

    Patch:

    .. code-block:: json

        {"op": "copy", "mode": "set", "from": "@.a", "to": "@.b"}

    Output:

    .. code-block:: json

        {"a": 0, "b": 0}

.. note:: You can't use a :ref:`filter` in the **from** and **to** fields.

del
^^^

Delete an item from an array or a property from an object.

Fields:
    - **op** (string) - the operation to perform. Must be ``"del"``.
    - **path** (string) - the :ref:`absolute path <absolute_path>` to the item.

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
    - **op** (string) - the operation to perform. Must be ``"extend"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **values** (array) - another array.

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
    - **op** (string) - the operation to perform. Must be ``"insert"``.
    - **path** (string) - the :ref:`absolute path <absolute_path>` with the
      index in the array.
    - **value** (any) - a value.

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

Fields:
    - **op** (string) - the operation to perform. Must be ``"move"``.
    - **mode** (string) - the paste mode. Must be:

      - ``"append"`` - append the source value to the end of a target array.
      - ``"extend"`` - extend the target array with the values of the source
        array.
      - ``"insert"`` - insert the source value at the specified index in the
        target array. In this mode, the **to** field is required.
      - ``"set"`` - replace the target value with the source value.
      - ``"update"`` - update the target object with the items of the source
        object, overwriting existing properties.

    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` where the operation is applied.
    - **from** (string) - the
      :ref:`relative path <relative_path>` to the source value.
    - **to** (string, default: ``"@"``) - the
      :ref:`relative path <relative_path>` to the target value.

Example:
    Input:

    .. code-block:: json

        {"a": 0}

    Patch:

    .. code-block:: json

        {"op": "move", "mode": "set", "from": "@.a", "to": "@.b"}

    Output:

    .. code-block:: json

        {"b": 0}

.. note:: You can't use a :ref:`filter` in the **from** and **to** fields.

reverse
^^^^^^^

Reverse the items from an array.

Fields:
    - **op** (string) - the operation to perform. Must be ``"reverse"``.
    - **path** (string, default: ``"$"``) - the
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
    - **op** (string) - the operation to perform. Must be ``"set"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` to the value.
    - **value** (any) - a value.

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
    - **op** (string) - the operation to perform. Must be ``"sort"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` to the array.
    - **reverse** (boolean, default: ``false``) - sort in descending order.

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
    - **op** (string) - the operation to perform. Must be ``"update"``.
    - **path** (string, default: ``"$"``) - the
      :ref:`absolute path <absolute_path>` to the object.
    - **properties** (object) - another object.

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
