jsonyx Specification
====================

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx_document
---------------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        jsonyx_document: `value`

.. image:: /_images/light/jsonyx/jsonyx_document.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/jsonyx_document.svg
        :class: only-dark

value
-----

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
------

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
-----

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
------

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
------

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
---

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        key: `whitespace` ( `string` | `~python-grammar:identifier` ) `whitespace`

.. image:: /_images/light/jsonyx/key.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/key.svg
        :class: only-dark

whitespace
----------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        whitespace: ( '//' [^#xA#xD]* | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/' | [#x9#xA#xD#x20] )*

.. image:: /_images/light/jsonyx/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/whitespace.svg
        :class: only-dark
