# simpleProgLang






    BNF Grammar


<statement_list> ::=  <statement_list> <statement> ;
                | <statement> 

<statement>  ::= MAKECLASS CLASSNAME <statement_list> ;
              | SUBCLASS CLASSNAME CLASSNAME statement_list ;
              | VARNAME '=' <expr> ;
              | <expr> ;

 <expr> ::= CLASSNAME
          | <expr> CONCAT <expr>
          | <expr> COMP <expr>
          | STR
          | VARNAME


