JSON Path Specification
=======================

JSON Path is a query language for JSON documents.

Operators
---------

==================== ====================
Operator             Description
==================== ====================
``$``                The root object
``@``                The current object
``.<name>``          Dot-notated child
``[<string>]``       Bracket-notated child
``[<number>]``       Array index
``[start:end]``      Array slice
``[start:end:step]`` Extended array slice
``[<expression>]``   Filter expression
``{<expression>}``   Condition
``?``                Optional marker 
==================== ====================

Examples
--------

Input:

.. code-block:: json

    {
        "books": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ]
    }

==================================================== =======================================
JSON Path                                            Result
==================================================== =======================================
``$.books[@]``                                       All books
``$.books[:].author``                                The authors of all books
``$.books[2]``                                       The third book
``$.books[-1]``                                      The last book
``$.books[:2]``                                      The first two books
``$.books[@.isbn]``                                  All books with an ISBN
``$.books[:].isbn?``                                 The ISBNs of all books with an ISBN
``$.books[@.price < 10]``                            All books cheaper than 10
``$.books[:].price{@ < 10}``                         The prices of all books cheaper than 10
``$.books[@.category == 'fiction' && @.price < 20]`` All fiction books cheaper than 20
==================================================== =======================================

Grammar
-------

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

.. _query:

query
^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        query: `absolute_query` | `relative_query`

.. image:: /_images/light/json-path/query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/query.svg
        :class: only-dark

.. _absolute_path:

absolute_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        absolute_query: '$' ( '?'? (
                      :     '.' `~python-grammar:identifier`
                      :     | '{' `filter` '}'
                      :     | '[' ( `slice` | `integer` | `string` | `filter` ) ']' )
                      : )* '?'?

.. image:: /_images/light/json-path/absolute_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/absolute_query.svg
        :class: only-dark

.. _relative_path:

relative_query
^^^^^^^^^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. image:: /_images/light/json-path/relative_query.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/relative_query.svg
        :class: only-dark

.. _expression:
.. _filter:

filter
^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        filter: (
              :     '!' `relative_query`
              :     | `relative_query` `whitespace` `operator` `whitespace` `value`
              : ) ++ ( `whitespace` '&&' `whitespace` )

.. image:: /_images/light/json-path/filter.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/filter.svg
        :class: only-dark

.. _query_value:

value
^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        value: `string` | `number` | 'true' | 'false' | 'null'

.. image:: /_images/light/json-path/value.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/value.svg
        :class: only-dark

slice
^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. image:: /_images/light/json-path/slice.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/slice.svg
        :class: only-dark

string
^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        string: "'" ( [^'~] | '~' ['~] )* "'"

.. image:: /_images/light/json-path/string.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/string.svg
        :class: only-dark

integer
^^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        integer: '-'? ( '0' | [1-9] [0-9]* )

.. image:: /_images/light/json-path/integer.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/integer.svg
        :class: only-dark

number
^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        number: '-'? (
              :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
              :     | 'Infinity'
              : )

.. image:: /_images/light/json-path/number.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/number.svg
        :class: only-dark

operator
^^^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

.. image:: /_images/light/json-path/operator.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/operator.svg
        :class: only-dark


whitespace
^^^^^^^^^^

.. container:: highlight

    .. productionlist:: json-path-grammar
        whitespace: '#x20'*

.. image:: /_images/light/json-path/whitespace.svg
    :class: only-light

.. only:: not latex

    .. image:: /_images/dark/json-path/whitespace.svg
        :class: only-dark
