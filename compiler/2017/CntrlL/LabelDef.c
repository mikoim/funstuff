#include "VSM.h"

#define CT_SIZE 100

typedef struct {
  int label;
  int addr;
} CSentry;

static CSentry Cstk[CT_SIZE], *CaseP = Cstk;

#define SWT_SIZE 10

struct {
  CSentry *CTptr;
  int DefltAddr;
} SWtbl[SWT_SIZE];

static int SWTptr = 0;

void BeginSW(void) {
  SWtbl[++SWTptr].CTptr = CaseP;
  SWtbl[SWTptr].DefltAddr = -1;
}

void CaseLbl(int Clabel) {
  CSentry *p;

  if (SWTptr > 0) {
    CaseP->label = Clabel;
    for (p = SWtbl[SWTptr].CTptr; p->label != Clabel; p++)
      ;
    if (p >= CaseP) {
      CaseP->addr = PC();
      CaseP++;
    } else {
      yyerror("Duplicated case constant");
    }
  }
}

void DfltLbl(void) {
  if (SWTptr > 0 && SWtbl[SWTptr].DefltAddr < 0) {
    SWtbl[SWTptr].DefltAddr = PC();
  } else {
    yyerror("Illegal default label");
  }
}

void EndSW(void) {
  CSentry *p;

  for (p = SWtbl[SWTptr].CTptr; p < CaseP; p++) {
    Pout(COPY);
    Cout(PUSHI, p->label);
    Pout(COMP);
    Cout(BNE, PC() + 3);
    Pout(REMOVE);
    Cout(JUMP, p->addr);
  }

  Pout(REMOVE);

  if (SWtbl[SWTptr].DefltAddr > 0) {
    Cout(JUMP, SWtbl[SWTptr].DefltAddr);
  }

  CaseP = SWtbl[SWTptr--].CTptr;
}
