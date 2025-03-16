jsonyx Patch Specification
==========================

.. todo:: Specify operations

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx_expression
-----------------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        jsonyx_expression: `absolute_query` | `relative_query` | `filter`

.. image:: /_images/light/jsonyx-patch/jsonyx_expression.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/jsonyx_expression.svg
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

.. image:: /_images/light/jsonyx-patch/absolute_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/absolute_query.svg
        :class: only-dark

relative_query
--------------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/jsonyx-patch/relative_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/relative_query.svg
        :class: only-dark

filter
------

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
-----

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/jsonyx-patch/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/value.svg
        :class: only-dark

slice
-----

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/jsonyx-patch/slice.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/slice.svg
        :class: only-dark

string
------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/jsonyx-patch/string.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/string.svg
        :class: only-dark

integer
-------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/jsonyx-patch/integer.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/integer.svg
        :class: only-dark

number
------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        number: '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' )

.. image:: /_images/light/jsonyx-patch/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/number.svg
        :class: only-dark

operator
--------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

.. image:: /_images/light/jsonyx-patch/operator.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/operator.svg
        :class: only-dark


whitespace
----------

.. container:: highlight

    .. productionlist:: jsonyx-patch-grammar
        whitespace: '#x20'*

.. image:: /_images/light/jsonyx-patch/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-patch/whitespace.svg
        :class: only-dark
