#include <stdio.h>
#include <stdlib.h>
#include "SymTable.h"
#include "VSM.h"
#include "parser.h" // Don't change order this line

static int Level = 0, Mallocp = 0, MaxFSZ;
static char msg[50];

#define SYMT_SIZE 200
static STentry SymTab[SYMT_SIZE];
static STP SymTptr = &SymTab[1];

#define BT_SIZE 20
static struct {
    int allocp;
    STP first;
} BLKtbl[BT_SIZE] = {{0, &SymTab[1]}};

extern int SymPrintSW;
extern void yyerror(const char *s);

void OpenBlock(void) {
    BLKtbl[++Level].first = SymTptr;
    BLKtbl[Level].allocp = Mallocp;
}

void CloseBlock(void) {
    if (Mallocp > MaxFSZ) {
        MaxFSZ = Mallocp;
    }

    SymTptr = BLKtbl[Level].first;
    Mallocp = BLKtbl[Level--].allocp;
}

static STP MakeEntry(char *Name, Dtype T, Class C) {
    STP p;

    if ((p=SymTptr++) >= &SymTab[SYMT_SIZE]) {
        fprintf(stderr, "Too many symbols declared");
        exit(-2);
    }
    p->type = T;
    p->class = C;
    p->deflvl = Level;
    p->name = Name;

    return p;
}

static STP LookUp(char *Name) {
    STP p;

    for (p = SymTptr - 1, SymTab[0].name = Name; p->name != Name; p--);
    return p > SymTab ? p : NULL;
}

STP MakeFuncEntry(char *Fname) {
    STP p;

    if ((p = LookUp(Fname)) == NULL) {
        p = MakeEntry(Fname, VOID, NEWSYM);
    } else if (p->class != F_PROT) {
        yyerror("The Function name already declared");
    }

    if (SymPrintSW) {
        printf("\n"); PrintSymEntry(p);
    }

    Mallocp = MaxFSZ = 1;
    OpenBlock();
    return p;
}

void Prototype(STP Funcp, Dtype T) {
    Funcp->class = F_PROT;
    Funcp->type = T;
    Funcp->loc = -1;
    Funcp->Nparam = SymTptr - BLKtbl[Level].first;
    if (Level > 1) {
        yyerror("The prototype declaration ignored");
    }
    CloseBlock();
}

void FuncDef(STP Funcp, Dtype T) {
    int n = SymTptr - BLKtbl[Level].first;

    if (Funcp->class == NEWSYM) {
        Funcp->type = T;
        Funcp->Nparam = n;
    } else if (Funcp->class == F_PROT) {
        if (Funcp->type != T) {
            yyerror("Function type unmatched to the prototype");
        }

        if (Funcp->Nparam != n) {
            yyerror("No. of parameters mismatched");
        }

        Bpatch(Funcp->loc, PC() + 3);
    } else {
        yyerror("The function already declared");
        return;
    }

    Funcp->class = FUNC;
    Funcp->loc = PC() + 3;
}

void EndFdecl(STP Funcp) {
    CloseBlock();
    if (Funcp->class == FUNC) {
        Bpatch(Funcp->loc, MaxFSZ);
    }
    if (SymPrintSW) {
        PrintSymEntry(Funcp);
    }
}

void VarDecl(char *Name, Dtype T, Class C) {
    STP p;

    SymTptr->name = Name;
    for (p = BLKtbl[Level].first; p->name != Name; p++);
    if (p >= SymTptr) {
        if (T == VOID) {
            yyerror("Void is used as a type name");
            T = INT;
        }
        p = MakeEntry(Name, T, C);
        p->loc = Mallocp++;
        if (SymPrintSW) {
            PrintSymEntry(p);
        }
    } else {
        yyerror("Duplicated declaration");
    }
}

STP SymRef(char *Name) {
    STP p;

    if ((p = LookUp(Name)) == NULL) {
        sprintf(msg, "Ref. to undeclared identifier %s", Name);
        yyerror(msg);
        p = MakeEntry(Name, INT, VAR);
    }

    return p;
}

void UndefCheck(void) {
    STP p;

    if (Level > 0) {
        yyerror("Block is not properly nested");
    }

    for (p = &SymTab[1]; p < SymTptr; p++) {
        if (p->type == F_PROT && p->loc > 0) {
            sprintf(msg, "Undefined function %s is called", p->name);
            yyerror(msg);
        }
    }
}

void PrintSymEntry(STP Symp) {
    static char *SymC[] = {"NewSym", "Func", "Param", "Var", "P_Type"},
    *SymD[] = {"void", "int"};

    printf("%*c%-10s ", (Symp->deflvl)*2+2, ' ', Symp->name);
    printf("%-6s %-4s  ", SymC[Symp->class], SymD[Symp->type]);
    printf(Symp->deflvl ? "%+5d\n" : "%5d\n", Symp->loc);
}
