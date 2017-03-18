%{
#include <stdio.h>
#include <math.h>
#define YYSTYPE double
%}

%token NUM UMINUS

%left '+' '-'
%left '*' '/'
%right '^'
%right UMINUS

%%
line :
     | line expr '\n' { printf("%f\n", $2); }
     | line error '\n' { yyerrok; };

expr : expr '+' expr { $$ = $1 + $3; }
     | expr '-' expr { $$ = $1 - $3; }
     | expr '*' expr { $$ = $1 * $3; }
     | expr '/' expr { $$ = $1 / $3; }
     | expr '^' expr { $$ = pow($1, $3); }
     | '-' expr %prec UMINUS { $$ = - $2; }
     | '(' expr ')' { $$ = $2; }
     | NUM;
%%

yylex()
{
  int c;
  while((c = getchar()) == ' ');
  if (((c >= '0') && (c <= '9')) || c == '.') {
    ungetc(c, stdin);
    scanf("%lf", &yylval);
    return NUM;
  } else {
    return c;
  }
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
