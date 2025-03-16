jsonyx Patch Specification
==========================

jsonyx_expression
-----------------

.. productionlist:: jsonyx-patch-grammar
    jsonyx_expression: `absolute_query` | `relative_query` | `filter`

.. image:: /_images/light/jsonyx/jsonyx_expression.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/jsonyx_expression.png
        :class: only-dark

absolute_query
--------------

.. productionlist:: jsonyx-patch-grammar
    absolute_query: '$' ( '?'? ( '.' `~python-grammar:identifier` | '{' `filter` '}' | '[' ( `slice` | `integer` | `string` | `filter` ) ']' ) )* '?'?

.. image:: /_images/light/jsonyx/absolute_query.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/absolute_query.png
        :class: only-dark

relative_query
--------------

.. productionlist:: jsonyx-patch-grammar
    relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/jsonyx/relative_query.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/relative_query.png
        :class: only-dark

filter
------

.. productionlist:: jsonyx-patch-grammar
    filter: ( '!' `relative_query` | `relative_query` `whitespace` ( '<=' | '<' | '==' | '!=' | '>=' | '>' ) `whitespace` `value` ) ++ ( `whitespace` '&&' `whitespace` )

.. image:: /_images/light/jsonyx/filter.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/filter/jsonyx.png
        :class: only-dark

value
-----

.. productionlist:: jsonyx-patch-grammar
    value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/jsonyx/value.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/valuex/jsonyx.png
        :class: only-dark

slice
-----

.. productionlist:: jsonyx-patch-grammar
    slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/jsonyx/slice.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/slicex/jsonyx.png
        :class: only-dark

string
------

.. productionlist:: jsonyx-patch-grammar
    string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/jsonyx/string.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/string/jsonyx.png
        :class: only-dark

integer
-------

.. productionlist:: jsonyx-patch-grammar
    integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/jsonyx/integer.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyxintegerjsonyx.png
        :class: only-dark

number
------

.. productionlist:: jsonyx-patch-grammar
    number: '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' )

.. image:: /_images/light/jsonyx/number.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/number/jsonyx.png
        :class: only-dark

whitespace
----------

.. productionlist:: jsonyx-patch-grammar
    whitespace: '#x20'*

.. image:: /_images/light/jsonyx/whitespace.png
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx/whitespacenyx.png
        :class: only-dark
