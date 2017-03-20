#include <stdio.h>
#include "parser.h"
#define ST_SIZE 100
static char *SymTab[ST_SIZE];
static int Last = 0;

extern void yyerror(const char *s);

void SymDecl(char *sptr) {
  int i;

  SymTab[Last + 1] = sptr;
  for (i = 1; SymTab[i] != sptr; i++) {
    if (i > Last) {
      Last++;
    } else {
      yyerror("Duplicated declaration");
    }
  }
}

int SymRef(char *sptr) {
  int i;

  SymTab[Last + 1] = sptr;
  for (i = 1; SymTab[i] != sptr; i++)
    ;
  if (i > Last) {
    yyerror("Undeclared identifier used");
  }

  return i;
}
