jsonyx Path Specification
=========================

.. todo:: Explain syntax elements

Grammar
-------

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

jsonyx_expression
^^^^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        jsonyx_expression: `absolute_query` | `relative_query` | `filter`

.. image:: /_images/light/jsonyx-path/jsonyx_expression.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/jsonyx_expression.svg
        :class: only-dark

.. _absolute_path:

absolute_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        absolute_query: '$' ( '?'? (
                      :     '.' `~python-grammar:identifier`
                      :     | '{' `filter` '}'
                      :     | '[' ( `slice` | `integer` | `string` | `filter` ) ']' )
                      : )* '?'?

.. image:: /_images/light/jsonyx-path/absolute_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/absolute_query.svg
        :class: only-dark

.. _relative_path:

relative_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/jsonyx-path/relative_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/relative_query.svg
        :class: only-dark

.. _expression:
.. _filter:

filter
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        filter: (
              :     '!' `relative_query`
              :     | `relative_query` `whitespace` `operator` `whitespace` `value`
              : ) ++ ( `whitespace` '&&' `whitespace` )

.. image:: /_images/light/jsonyx-path/filter.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/filter.svg
        :class: only-dark

value
^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/jsonyx-path/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/value.svg
        :class: only-dark

slice
^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/jsonyx-path/slice.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/slice.svg
        :class: only-dark

string
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/jsonyx-path/string.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/string.svg
        :class: only-dark

integer
^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/jsonyx-path/integer.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/integer.svg
        :class: only-dark

number
^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        number: '-'? (
              :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
              :     | 'Infinity'
              : )

.. image:: /_images/light/jsonyx-path/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/number.svg
        :class: only-dark

operator
^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

.. image:: /_images/light/jsonyx-path/operator.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/operator.svg
        :class: only-dark


whitespace
^^^^^^^^^^

.. container:: highlight

    .. productionlist:: jsonyx-path-grammar
        whitespace: '#x20'*

.. image:: /_images/light/jsonyx-path/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/jsonyx-path/whitespace.svg
        :class: only-dark
