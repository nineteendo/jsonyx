jsonyx Patch Specification
==========================

Operations
----------

.. todo:: Specify other operations

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
      :ref:`absolute path <absolute_path>` to the value.
    - **expr** (any) - :ref:`an expression <expression>`.
    - **msg** (string, default: ``"Path <path>: <expr>"``): an error message

Example:
    Input:

    .. code-block:: json

        false

    Patch:

    .. code-block:: json

        {"op": "assert", "expr": "@ == true"}

    Output:

    .. code-block:: none

        AssertionError: Path $: @ == true

clear
^^^^^

Remove all items from an array or object.

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

copy
^^^^

Copy a value.

Fields:
    - **op** (string) - the operation to perform. Must be ``"copy"``.
    - **mode** (string) - the paste mode. Must be:

        - ``"append"`` - append the source value to the end of a target array.
        - ``"extend"`` - extend a target array with the contents of the source
          array.
        - ``"insert"`` - insert the source value at the specified index in the
          target array. In this mode, the **to** field is required.
        - ``"set"`` - replace the target value by the source value.
        - ``"update"`` - update the target object with key/value pairs from the
          source object, overwriting existing keys.

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

Grammar
-------

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx_expression
^^^^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        jsonyx_expression: `absolute_query` | `relative_query` | `filter`

.. image:: /_images/light/jsonyx-patch/jsonyx_expression.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/jsonyx_expression.svg
        :class: only-dark

.. _absolute_path:

absolute_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        absolute_query: '$' ( '?'? (
                      :     '.' `~python-grammar:identifier`
                      :     | '{' `filter` '}'
                      :     | '[' ( `slice` | `integer` | `string` | `filter` ) ']' )
                      : )* '?'?

.. image:: /_images/light/jsonyx-patch/absolute_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/absolute_query.svg
        :class: only-dark

.. _relative_path:

relative_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/jsonyx-patch/relative_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/relative_query.svg
        :class: only-dark

.. _expression:

filter
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        filter: (
              :     '!' `relative_query`
              :     | `relative_query` `whitespace` `operator` `whitespace` `value`
              : ) ++ ( `whitespace` '&&' `whitespace` )

.. image:: /_images/light/jsonyx-patch/filter.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/filter.svg
        :class: only-dark

value
^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/jsonyx-patch/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/value.svg
        :class: only-dark

slice
^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/jsonyx-patch/slice.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/slice.svg
        :class: only-dark

string
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/jsonyx-patch/string.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/string.svg
        :class: only-dark

integer
^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/jsonyx-patch/integer.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/integer.svg
        :class: only-dark

number
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        number: '-'? (
              :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
              :     | 'Infinity'
              : )

.. image:: /_images/light/jsonyx-patch/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/number.svg
        :class: only-dark

operator
^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

.. image:: /_images/light/jsonyx-patch/operator.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/operator.svg
        :class: only-dark


whitespace
^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        whitespace: '#x20'*

.. image:: /_images/light/jsonyx-patch/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/whitespace.svg
        :class: only-dark
