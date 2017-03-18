%{
  #include "VSM.h"
%}

%token NUM

%left ADDOP
%left MULOP
%right UMINUS

%%

program : expr_list { Pout(HALT); }
        ;

expr_list :
          | expr_list expr ';' { Pout(OUTPUT); }
          | expr_list error ';'
          ;

expr : expr ADDOP expr { Pout($2); }
     | expr MULOP expr { Pout($2); }
     | '(' expr ')'
     | ADDOP expr %prec UMINUS { if ($1 == SUB) Pout(CSIGN); }
     | NUM { Cout(PUSHI, $1); }
     ;

%%

#define TraceSW 0

main()
{
  SetPC(0);
  yyparse();
  DumpIseg(0, PC() - 1);
  printf("Enter execution phase\n");
  if (StartVSM(0, TraceSW) != 0)
    printf("Execution aborted\n");
}

yyerror(char *msg)
{
  printf("%s\n", msg);
}
