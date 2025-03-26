jsonyx Specification
====================

jsonyx allows minimal and unambiguous JSON deviations for developer
convenience.

Example
-------

.. code-block:: javascript

    {
        /* Block */ // and line comments
        "Missing commas": [1 2 3],
        "NaN and infinity": [NaN, Infinity, -Infinity],
        "Surrogates": "\ud800",
        "Trailing comma": [0,],
        "Unquoted keys": {key: "value"}
    }

Grammar
-------

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx_document
^^^^^^^^^^^^^^^

A jsonyx document consists of a single value.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        jsonyx_document: `value`

.. image:: /_images/light/jsonyx/jsonyx_document.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/jsonyx_document.svg
        :class: only-dark

value
^^^^^

A value can be an object, array, string, number, ``true``, ``false`` or
``null``.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        value:  `whitespace`
             :  ( `object` | `array` | `string` | `number` | 'true' | 'false' | 'null' )
             :  `whitespace`

.. image:: /_images/light/jsonyx/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/value.svg
        :class: only-dark

object
^^^^^^

An object is an unordered set of key/value pairs enclosed in curly braces.
Each key is followed by a colon and pairs are separated by commas or
whitespace with an optional trailing comma.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        object: '{' (
              :     `whitespace`
              :     | ( ( `key` ':' `value` ) ++ ( ',' | `whitespace` - '' ) ) ( ',' `whitespace` )?
              : ) '}'

.. image:: /_images/light/jsonyx/object.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/object.svg
        :class: only-dark

array
^^^^^

An array is an ordered collection of values enclosed in square brackets. Values
are separated by commas or whitespace with an optional trailing comma.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        array:  '[' (
             :      `whitespace`
             :      | ( `value` ++ ( ',' | `whitespace` - '' ) ) ( ',' `whitespace` )?
             :  ) ']'

.. image:: /_images/light/jsonyx/array.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/array.svg
        :class: only-dark

string
^^^^^^

A string is a sequence of characters, wrapped in double quotes, using backslash
escapes.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        string: '"' (
              :     [^"\#x0-#x1F]
              :     | '\' ( ["\/bfnrt] | 'u' [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] )
              : )* '"'

.. image:: /_images/light/jsonyx/string.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/string.svg
        :class: only-dark

number
^^^^^^

A number is a signed decimal number, optionally in scientific notation or one
of the special values ``NaN``, ``Infinity`` and ``-Infinity``.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        number: '-'? (
              :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
              :     | 'Infinity'
              : ) | 'NaN'

.. image:: /_images/light/jsonyx/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/number.svg
        :class: only-dark

key
^^^

A key can be a string or an identifier.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        key: `whitespace` ( `string` | `~python-grammar:identifier` ) `whitespace`

.. image:: /_images/light/jsonyx/key.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/key.svg
        :class: only-dark

whitespace
^^^^^^^^^^

Whitespace, including comments can be inserted between any pair of tokens.

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        whitespace: ( '//' [^#xA#xD]* | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/' | [#x9#xA#xD#x20] )*

.. image:: /_images/light/jsonyx/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/whitespace.svg
        :class: only-dark
