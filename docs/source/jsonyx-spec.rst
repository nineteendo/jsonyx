jsonyx Specification
====================

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx
------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        jsonyx: `value`

.. image:: /_images/light/jsonyx/jsonyx.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/jsonyx.png
        :class: only-dark

value
-----

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        value: `comments`? ( `object` | `array` | `string` | `number` | 'true' | 'false' | 'null' ) `comments`?

.. image:: /_images/light/jsonyx/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/value.png
        :class: only-dark

object
------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        object: '{' ( `comments`? | ( ( `key` ':' `value` ) ++ ( ',' | `comments` ) ) ( ',' `comments`? )? ) '}'

.. image:: /_images/light/jsonyx/object.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/object.png
        :class: only-dark

array
-----

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        array: '[' ( `comments`? | ( `value` ++ ( ',' | `comments` ) ) ( ',' `comments`? )? ) ']'

.. image:: /_images/light/jsonyx/array.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/array.png
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

    .. image:: /_images/dark/jsonyx/string.png
        :class: only-dark

number
------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        number: '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' )
              : | 'NaN'

.. image:: /_images/light/jsonyx/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/number.png
        :class: only-dark

key
---

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        key: `comments`? ( `string` | `~python-grammar:identifier` ) `comments`?

.. image:: /_images/light/jsonyx/key.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/key.png
        :class: only-dark

comments
--------

.. container:: highlight

    .. productionlist:: jsonyx-grammar
        comments: ( '//' [^#xA#xD]* | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/' | [#x9#xA#xD#x20] )+

.. image:: /_images/light/jsonyx/comments.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/comments.png
        :class: only-dark
