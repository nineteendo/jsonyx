jsonyx
======

A superset of JSON with less restrictive syntax.

Example
-------

.. versionchanged:: 2.0 Added support for unquoted keys.

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

jsonyx document
^^^^^^^^^^^^^^^

A jsonyx document consists of a single value.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/jsonyx_document.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/jsonyx_document.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            jsonyx_document: `value`

.. _any:
.. _boolean:
.. _null:

value
^^^^^

A value can be an object, array, string, number, :json:`true`, :json:`false` or
:json:`null`.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/value.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/value.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            value:  `whitespace`
                 :  ( `object` | `array` | `string` | `number` | 'true' | 'false' | 'null' )
                 :  `whitespace`

.. _object:

object
^^^^^^

An object is an unordered collection of key/value pairs enclosed in curly
braces.

Keys and values are separated by colons. Key/value pairs are separated by
commas or whitespace with an optional trailing comma.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/object.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/object.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            object: '{' (
                  :     `whitespace`
                  :     | ( ( `key` ':' `value` ) ++ ( ',' | `whitespace` - '' ) ) ( ',' `whitespace` )?
                  : ) '}'

.. _array:

array
^^^^^

An array is an ordered collection of values enclosed in square brackets.

Values are separated by commas or whitespace with an optional trailing comma.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/array.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/array.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            array:  '[' (
                 :      `whitespace`
                 :      | ( `value` ++ ( ',' | `whitespace` - '' ) ) ( ',' `whitespace` )?
                 :  ) ']'

.. _string:

string
^^^^^^

A string is a sequence of characters, wrapped in double quotes, using backslash
escapes.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/string.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/string.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            string: '"' (
                  :     [^"\#x0-#x1F]
                  :     | '\' ( ["\/bfnrt] | 'u' [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] )
                  : )* '"'

.. _number:

number
^^^^^^

A number is a signed decimal number, optionally in scientific notation or one
of the special values :javascript:`NaN`, :javascript:`Infinity` and
:javascript:`-Infinity`.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/number.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/number.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            number: '-'? (
                  :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
                  :     | 'Infinity'
                  : ) | 'NaN'

key
^^^

A key can be a string or an identifier.

.. versionchanged:: 2.0 Added support for identifiers.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/key.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/key.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            key: `whitespace` ( `string` | `~python-grammar:identifier` ) `whitespace`

whitespace
^^^^^^^^^^

Whitespace, including comments can be inserted between any pair of tokens.

.. tab:: Diagram

    .. image:: /_images/light/jsonyx/whitespace.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/jsonyx/whitespace.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: jsonyx-grammar
            whitespace: (
                      :     '//' [^#xA#xD]* ( [#xA#xD] | `!EOF` )
                      :     | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/'
                      :     | [#x9#xA#xD#x20]
                      : )*
