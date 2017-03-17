/* Program 3.1 Extended */

%start line

%%
line : expr '\n' { printf("%d\n", $1); }
	;

expr : expr '+' term { $$ = $1 + $3; }
	| expr '-' term { $$ = $1 - $3; }
	| term { $$ = $1; }
	;

term : term '*' factor { $$ = $1 * $3; }
	| term '/' factor { $$ = $1 / $3; }
	| factor { $$ = $1; }
	;

factor : num
	| '(' expr ')' { $$ = $2; }
	;

num : digit
	| num digit { $$ = $1*10 + $2; }
	;

digit : '0' { $$ = 0; }
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

yylex() {
	int c;

	while ((c = getchar()) == ' ');
	return c;
}