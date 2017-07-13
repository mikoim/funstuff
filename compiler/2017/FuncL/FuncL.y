%{
  #include <stdio.h>
  #include "SymTable.h"
  #include "VSM.h"

  #define TCHK(X) { if((X)==VOID) { yyerror("Type error"); } }

  char *IDentry(char *Name, int len);
  Dtype VarRef(int OPcode, char *Vname);
  void GenFuncEntry(STP func);
  Dtype GenCall(char *Fname, int Nparam);

  STP FuncP;

  extern int StartP;

  int yylex();
  void yyerror(const char *s);
%}

%union {
  int Int;
  char *Name;
  STP SymP;
}

%token IF ELSE READ WRITE RETURN
%token <Int> TYPE RELOP ADDOP MULOP NUM
%token <Name> ID

%type <Int> decl expr LHS arg_list if_part
%type <SymP> f_head

%right '='
%left RELOP
%left ADDOP
%left MULOP
%right UM

%%

program : glbl_decl { UndefCheck(); StartP = PC(); Cout(SETFR, FRAME_BOTTOM); GenCall(IDentry("main", 4), 0); Pout(HALT); }
        ;

glbl_decl :
          | glbl_decl decl ';'
          | glbl_decl func_def
          | glbl_decl error ';' { yyerrok; }
          ;

decl : TYPE ID { VarDecl($2, $1, VAR); }
     | TYPE f_head { Prototype($2, $1); }
     | decl ',' ID { VarDecl($3, $1, VAR); }
     | decl ',' f_head { Prototype($3, $1); }
     ;

f_head : ID { $<SymP>$ = MakeFuncEntry($1); } '(' p_list ')' { $$ = $<SymP>2; }
       ;

p_list :
       | p_decl
       | p_list ',' p_decl
       ;

p_decl : TYPE ID { VarDecl($2, $1, PARAM); }
       ;

func_def : TYPE f_head '{' { FuncDef($2, $1); FuncP = $2; GenFuncEntry($2); }
           decl_list
           st_list '}' { if ($2->type == INT) { Cout(PUSHI, 0); } Cout(JUMP, ($2->loc)-3); EndFdecl($2); }
       ;

block : '{' { OpenBlock(); }
             decl_list st_list
         '}' { CloseBlock(); }
      ;

decl_list :
          | decl_list decl ';'
          ;

st_list : stmnt
        | st_list stmnt
        ;

stmnt : block
      | expr ';' { if ($1 != VOID) { Pout(REMOVE); } }
      | READ LHS ';' { Pout(INPUT); }
      | WRITE expr ';' { Pout(OUTPUT); TCHK($2); }
      | if_part { Bpatch($1, PC()); }
      | if_part ELSE { $<Int>$ = PC(); Cout(JUMP, -1); Bpatch($1, PC()); } stmnt { Bpatch($<Int>3, PC()); }
      | RETURN ';' { if(FuncP->type != VOID) { Cout(PUSHI, 0); } Cout(JUMP, (FuncP->loc)-3); }
      | RETURN expr ';' { if (FuncP->type != INT) { yyerror("Meaningless expression"); } Cout(JUMP, (FuncP->loc)-3); TCHK($2); }
      ;

if_part : IF '(' expr ')' { $<Int>$ = PC(); Cout(BEQ, -1); TCHK($3); } stmnt { $$ = $<Int>5; }
        ;

LHS : ID { $$ = VarRef(PUSHI, $1); }
    ;

expr : LHS '=' expr { Pout(ASSGN); TCHK($3); }
     | expr RELOP expr { TCHK($1); TCHK($3); Pout(COMP); Cout($2, PC() + 3); Cout(PUSHI, 0); Cout(JUMP, PC() + 2); Cout(PUSHI, 1); }
     | expr ADDOP expr { Pout($2); TCHK($1); TCHK($3); }
     | expr MULOP expr { Pout($2); TCHK($1); TCHK($3); }
     | ADDOP expr %prec UM { if ($1 == SUB) { Pout(CSIGN); } }
     | '(' expr ')' { $$ = $2; }
     | ID '(' arg_list ')' { $$ = GenCall($1, $3); }
     | ID { $$ = VarRef(PUSH, $1); }
     | NUM { Cout(PUSHI, $1); $$ = INT; }
     ;

arg_list : { $$ = 0; }
         | expr { $$ = 1; TCHK($1); }
         | arg_list ',' expr { $$ = $1 + 1; TCHK($3); }
         ;

%%

void GenFuncEntry(STP func) {
  int n;

  SetI(PUSH, FP, 0); Cout(INCFR, -1); Pout(RET);
  Cout(DECFR, PC() - 2); SetI(POP, FP, 0);
  for (n = func->Nparam; n > 0; n--) {
    SetI(POP, FP, n);
  }
}

Dtype VarRef(int OPcode, char *Vname) {
  STP p;

  if ((p = SymRef(Vname)) != NULL) {
    if (p->class != VAR && p->class != PARAM) {
      yyerror("Function name is used as a variable");
    }
  }

  SetI(OPcode, p->deflvl ? FP : 0, p->loc);
  return p->type;
}

Dtype GenCall(char *Fname, int Nparam) {
  STP p;

  if ((p=SymRef(Fname)) == NULL) {
    return VOID;
  }

  if (p->class == FUNC || p->class == F_PROT) {
    if (p->Nparam != Nparam) {
      yyerror("Number of arguments mismatched");
    }
    Cout(CALL, p->loc);
    if (p->class == F_PROT) {
      p->loc = PC() - 1;
    }
  } else {
    yyerror("Non-function call");
  }

  return p->type;
}
