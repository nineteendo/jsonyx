jsonyx Patch Specification
==========================

.. todo:: Specify operations

jsonyx_expression
-----------------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        jsonyx_expression: `absolute_query` | `relative_query` | `filter`

.. image:: /_images/light/jsonyx-patch/jsonyx_expression.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/jsonyx_expression.png
        :class: only-dark

absolute_query
--------------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        absolute_query: '$' ( '?'? (
                      :     '.' `~python-grammar:identifier`
                      :     | '{' `filter` '}'
                      :     | '[' ( `slice` | `integer` | `string` | `filter` ) ']' )
                      : )* '?'?

.. image:: /_images/light/jsonyx-patch/absolute_query.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/absolute_query.png
        :class: only-dark

relative_query
--------------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/jsonyx-patch/relative_query.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/relative_query.png
        :class: only-dark

filter
------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        filter: (
              :     '!' `relative_query`
              :     | `relative_query` `whitespace` `operator` `whitespace` `value`
              : ) ++ ( `whitespace` '&&' `whitespace` )

.. image:: /_images/light/jsonyx-patch/filter.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/filter.png
        :class: only-dark

value
-----

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/jsonyx-patch/value.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/value.png
        :class: only-dark

slice
-----

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/jsonyx-patch/slice.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/slice.png
        :class: only-dark

string
------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/jsonyx-patch/string.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/string.png
        :class: only-dark

integer
-------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/jsonyx-patch/integer.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/integer.png
        :class: only-dark

number
------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        number: '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' )

.. image:: /_images/light/jsonyx-patch/number.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/number.png
        :class: only-dark

operator
--------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

.. image:: /_images/light/jsonyx-patch/operator.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/operator.png
        :class: only-dark


whitespace
----------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        whitespace: '#x20'*

.. image:: /_images/light/jsonyx-patch/whitespace.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/whitespace.png
        :class: only-dark
