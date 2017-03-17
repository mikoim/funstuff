%{
#include <math.h>
#define YYSTYPE double
%}

%token NUM UMINUS

%left '+' '-'
%left '*' '/'
%right '^'
%right UMINUS

%%
line : /* Empty rule */
	| line expr '\n' { printf("%f\n", $2); }
	| line error '\n' { yyerrok; }
	;

expr : expr '+' expr { $$ = $1 + $3; }
	| expr '-' expr { $$ = $1 - $3; }
	| expr '*' expr { $$ = $1 * $3; }
	| expr '/' expr { $$ = $1 / $3; }
	| expr '^' expr { $$ = pow($1, $3); }
	| '-' expr %prec UMINUS { $$ = -$2; }
	| '(' expr ')' { $$ = $2; }
	| NUM
	;
%%

#include <stdio.h>
yylex()
{
	int c;

	while ((c = getchar()) == ' '); /* Skip white space */
	if (((c >= '0') && (c <= '9')) || c == '.') {
		ungetc(c, stdin);
		scanf("%lf", &yylval);
		return NUM;
	}
	else
		return c;
}