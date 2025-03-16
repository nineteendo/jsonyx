jsonyx Specification
====================

jsonyx
------

.. image:: /_images/jsonyx.png
.. productionlist:: jsonyx-grammar
    jsonyx: `value`

value
-----

.. image:: /_images/value.png
.. productionlist:: jsonyx-grammar
    value: `comments`? ( `object` | `array` | `string` | `number` | 'true' | 'false' | 'null' ) `comments`?

object
------

.. image:: /_images/object.png
.. productionlist:: jsonyx-grammar
    object: '{' ( `comments`? | ( ( `key` ':' `value` ) ++ ( ',' | `comments` ) ) ( ',' `comments`? )? ) '}'

array
-----

.. image:: /_images/array.png
.. productionlist:: jsonyx-grammar
    array: '[' ( `comments`? | ( `value` ++ ( ',' | `comments` ) ) ( ',' `comments`? )? ) ']'

string
------

.. image:: /_images/string.png
.. productionlist:: jsonyx-grammar
    string: '"' ( [^"\#x0-#x1F] | '\' ( ["\/bfnrt] | 'u' [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] ) )* '"'

number
------

.. image:: /_images/number.png
.. productionlist:: jsonyx-grammar
    number: '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' ) | 'NaN'

key
---

.. image:: /_images/key.png
.. productionlist:: jsonyx-grammar
    key: `comments`? ( `string` | `~python-grammar:identifier` ) `comments`?

comments
--------

.. image:: /_images/comments.png
.. productionlist:: jsonyx-grammar
    comments: ( '//' [^#xA#xD]* | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/' | [#x9#xA#xD#x20] )+