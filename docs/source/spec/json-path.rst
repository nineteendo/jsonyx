JSON Path
=========

A query language for selecting values from a JSON document.

.. versionadded:: 2.0

Selectors
---------

.. tabularcolumns:: \X{1}{2}\X{1}{2}
.. table::
    :class: longtable

    =================================== =============================
    Selector                            Description
    =================================== =============================
    ``$``                               The root value
    ``@``                               The current value
    ``.<identifier>``                   A single object property
    ``[<string>, ...]``                 Multiple object properties
    ``[<integer>, ...]``                Multiple array indices
    ``[<integer>:<integer>]``           An array slice
    ``[<integer>:<integer>:<integer>]`` An extended array slice
    ``[<filter>]``                      A filter on the child values
    ``{<filter>}``                      A filter on the current value
    ``?``                               A shorthand for ``{@}``
    =================================== =============================

Examples
--------

.. versionchanged:: 2.6

    - Added support for comparing 2 paths.
    - Allowed selecting multiple indices.
    - Made ``?`` expand slices like ``{@}``.
    - Switched from tilde escapes to doubling.

.. code-block:: json

    {
        "books": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "available": 1,
                "total": 1
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "available": 3,
                "total": 3
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "available": 0,
                "total": 2
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "available": 1,
                "total": 4
            }
        ],
        "foo'bar": "value"
    }

.. tabularcolumns:: \X{1}{2}\X{1}{2}
.. table::
    :class: longtable

    ======================================================= ===========================================
    JSON Path                                               Result
    ======================================================= ===========================================
    ``$.books``                                             The array of all books
    ``$.books[@]``                                          All books
    ``$.books[:].author``                                   The authors of all books
    ``$.books[2]``                                          The third book
    ``$.books[-1]``                                         The last book
    ``$.books[0, 1]``                                       The first two books
    ``$.books[::2]``                                        An array of the even books
    ``$.books[::2]?``                                       The even books
    ``$.books[@.isbn]``                                     All books with an ISBN
    ``$.books[:].isbn?``                                    The ISBNs of all books with an ISBN
    ``$.books[@.available > 0]``                            All available books
    ``$.books[:].available{@ > 0}``                         The number of copies of all available books
    ``$.books[@.category == 'fiction' && @.available > 0]`` All available fiction books
    ``$.books[@.available < @.total]``                      All borrowed books
    ``$['foo''bar']``                                       The value of the key :json:`"foo'bar"`
    ======================================================= ===========================================

Grammar
-------

Generated with
`RR - Railroad Diagram Generator <https://www.bottlecaps.de/rr/ui>`_ by
`Gunther Rademacher <https://github.com/GuntherRademacher>`_.

.. _select_query:

query
^^^^^

A query can be absolute or relative.

.. tab:: Diagram

    .. image:: /_images/light/json-path/query.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/query.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            query: `absolute_query` | `relative_query`

.. _absolute_path:
.. _absolute_query:

absolute query
^^^^^^^^^^^^^^

An absolute query starts with a dollar sign followed by zero or more selectors.

.. versionchanged:: 2.6 Allowed selecting multiple indices or properties.

.. tab:: Diagram

    .. image:: /_images/light/json-path/absolute_query.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/absolute_query.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            absolute_query: '$' ( '?'? (
                          :     '.' `~python-grammar:identifier`
                          :     | '{' `filter` '}'
                          :     | '[' ( `slice` | `index_array` | `property_array` | `filter` ) ']'
                          : ) )* '?'?

.. _relative_path:

relative query
^^^^^^^^^^^^^^

A relative query starts with an at sign followed by zero or more child
selectors.

.. tab:: Diagram

    .. image:: /_images/light/json-path/relative_query.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/relative_query.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            relative_query: '@' ( '.' `~python-grammar:identifier` | '[' ( `slice` | `string` | `integer` ) ']' )*

.. _expression:
.. _filter:
.. _filter_query:

filter
^^^^^^

A filter consists of one or more (non-)existence checks / comparisons,
separated by double ampersands.

.. versionchanged:: 2.6 Added support for comparing 2 paths.

.. tab:: Diagram

    .. image:: /_images/light/json-path/filter.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/filter.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            filter: (
                  :     '!'? `relative_query`
                  :     | `relative_query` `whitespace` `operator` `whitespace` ( `value` | `relative_query` )
                  : ) ++ ( `whitespace` '&&' `whitespace` )

index array
^^^^^^^^^^^

An index array is an ordered collection of one or more integers, separated by
commas or whitespace with an optional trailing comma.

.. versionadded:: 2.6

.. tab:: Diagram

    .. image:: /_images/light/json-path/index_array.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/index_array.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            index_array: ( `integer` ++ ( ',' | `whitespace` - '' ) ) ','?

property array
^^^^^^^^^^^^^^

A property array is an ordered collection of one or more strings, separated by
commas or whitespace with an optional trailing comma.

.. versionadded:: 2.6

.. tab:: Diagram

    .. image:: /_images/light/json-path/property_array.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/property_array.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            property_array: ( `string` ++ ( ',' | `whitespace` - '' ) ) ','?

.. _query_value:

value
^^^^^

A value can be a string, number, :json:`true`, :json:`false` or :json:`null`.

.. tab:: Diagram

    .. image:: /_images/light/json-path/value.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/value.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            value: `string` | `number` | 'true' | 'false' | 'null'

slice
^^^^^

A slice has a start and an end index (exclusive) with an optional step.

.. tab:: Diagram

    .. image:: /_images/light/json-path/slice.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/slice.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            slice: `integer`? ':' `integer`? ( ':' `integer`? )?

.. _query_string:

string
^^^^^^

A string is a sequence of characters, wrapped in single quotes, using quote
doubling.

.. versionchanged:: 2.6 Switched from tilde escapes to quote doubling.

.. tab:: Diagram

    .. image:: /_images/light/json-path/string.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/string.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            string: ( "'" [^']* "'" )+

integer
^^^^^^^

An integer is a signed whole number.

.. tab:: Diagram

    .. image:: /_images/light/json-path/integer.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/integer.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            integer: '-'? ( '0' | [1-9] [0-9]* )

number
^^^^^^

A number is a signed decimal number, optionally in scientific notation or one
of the special values :javascript:`Infinity` and :javascript:`-Infinity`.

.. tab:: Diagram

    .. image:: /_images/light/json-path/number.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/number.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            number: '-'? (
                  :     ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )?
                  :     | 'Infinity'
                  : )

.. note:: ``@ == NaN`` is not allowed because :javascript:`NaN !== NaN`, use
    ``@ != @`` instead.

operator
^^^^^^^^

An operator can be ``<=``, ``<``, ``==``, ``!=``, ``>=`` or ``>``.

.. tab:: Diagram

    .. image:: /_images/light/json-path/operator.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/operator.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            operator: '<=' | '<' | '==' | '!=' | '>=' | '>'

whitespace
^^^^^^^^^^

Whitespace can be inserted around operators and comma's.

.. tab:: Diagram

    .. image:: /_images/light/json-path/whitespace.*
        :class: only-light

    .. only:: not latex

        .. image:: /_images/dark/json-path/whitespace.svg
            :class: only-dark

.. tab:: EBNF

    .. container:: highlight

        .. productionlist:: json-path-grammar
            whitespace: '#x20'*
