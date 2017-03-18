%{
  #include <stdio.h>
  int yylex (void);
  void yyerror (char const *);
  extern int yydebug;
%}

%start line

%%
line :
     | line expr '\n' { printf("%d\n", $2); }
     | line error '\n' { yyerrok; }
     ;

expr : expr '+' term { $$ = $1 + $3; }
     | expr '-' term { $$ = $1 - $3; }
     | term
     ;

term : term '*' factor { $$ = $1 * $3; }
     | term '/' factor { $$ = $1 / $3; }
     | factor
     ;

factor : '(' expr ')' { $$ = $2; }
       | NUM { $$ = $1; }
       ;

NUM : DIGIT
    | NUM DIGIT { $$ = $1 * 10 + $2; }
    ;

DIGIT : '0' { $$ = 0; }
      | '1' { $$ = 1; }
      | '2' { $$ = 2; }
      | '3' { $$ = 3; }
      | '4' { $$ = 4; }
      | '5' { $$ = 5; }
      | '6' { $$ = 6; }
      | '7' { $$ = 7; }
      | '8' { $$ = 8; }
      | '9' { $$ = 9; }
      ;
%%

yylex()
{
  int c;
  while((c = getchar()) == ' ');
  return c;
}

void yyerror(char const *s)
{
  fprintf(stderr, "%s\n", s);
}

int main(int argc, char const* argv[])
{
  yydebug = 0;
  return yyparse();
}
