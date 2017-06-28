#include "VSM.h"

#define CTRLT_SIZE 20

struct {
  int StType;
  int Bchain, Cchain;
} Ctable[CTRLT_SIZE];

static int CSptr = 0;

void NestIn(int St) {
  Ctable[++CSptr].StType = St;
  Ctable[CSptr].Bchain = Ctable[CSptr].Cchain = -1;
}

void GenBrk(int JC) {
  if (CSptr > 0) {
    Cout(JC, Ctable[CSptr].Bchain);
    Ctable[CSptr].Bchain = PC() - 1;
  } else {
    yyerror("Illegal use of break statement");
  }
}

void GenConti(void) {
  int i = 0;

  for (i = CSptr; i > 0 && Ctable[i].StType == 0; i--)
    ;
  if (i <= 0) {
    yyerror("Illegal use of the continue");
  } else {
    Cout(JUMP, Ctable[i].Cchain);
    Ctable[i].Cchain = PC() - 1;
  }
}

void NestOut(int ContP) {
  Bpatch(Ctable[CSptr].Cchain, ContP);
  Bpatch(Ctable[CSptr].Bchain, PC());
  CSptr--;
}
