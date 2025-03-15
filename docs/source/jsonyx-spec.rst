jsonyx Specification
====================

.. code-block:: ebnf
 
    jsonyx ::= value
    value ::= comments? ( object | array | string | number | 'true' | 'false' | 'null' ) comments?
    object ::= '{' ( comments? | ( ( key ':' value ) ++ ( ',' | comments ) ) ( ',' comments? )? ) '}'
    array ::= '[' ( comments? | ( value ++ ( ',' | comments ) ) ( ',' comments? )? ) ']'
    string ::= '"' ( [^"\#x0-#x1F] | '\' ( ["\/bfnrt] | 'u' [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] ) )* '"'
    number ::= '-'? ( ( '0' | [1-9] [0-9]* ) ( '.' [0-9]+ )? ( [eE] [+-]? [0-9]+ )? | 'Infinity' ) | 'NaN'
    key ::= comments? ( string | identifier ) comments?
    identifier ::= [https://docs.python.org/3/reference/lexical_analysis.html#identifiers]
    comments ::= ( '//' [^#xA#xD]* | '/*' ( ( [^*]* '*'+ ) ++ [^*/] ) '/' | [#x9#xA#xD#x20] )+