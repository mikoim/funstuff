/*
* VSM simulator (program 6.4)
 */

#include <stdio.h>
#include "VSM.h"

int DebugSW=0;                                   /* Debug mode is off */

static int Pctr=0, SP=0, Freg=0;
static int InsCount=0, MaxSD=0, MinFR=DSEG_SIZE, MaxPC=0, CallC=0;

static INSTR Iseg[ISEG_SIZE];                    /* Instruction segment */
static int   Dseg[DSEG_SIZE];                    /* Data segment */

#define STACK_SIZE 100
static int Stack[STACK_SIZE];                    /* Operand stack */

char *Scode[] = {                                /* operation code for displaying */
                 "Nop",    "  =",   "  +",    "  -",    "  *",  "  /",
                 "  %",    "  -'",  "and",    "or",     "not",  "comp",
                 "copy",   "push",  "push-i", "remove", "pop",  " ++",
                 " --",    "setFR", "++FR",   "--FR",   "jump", "<0 ?",
                 "<=0 ?",  "==0 ?", "!=0 ?",  ">=0 ?",  ">0 ?", "call",
                 "return", "halt",  "input",  "output" };

static void PrintIns(int loc)                    /* Edit and print of instruction */
{
  int   op;

  op = Iseg[loc].Op;
  printf("%5d  %-8s ", loc, Scode[op]);
  switch (op) {
    case PUSH:  case PUSHI: case POP: case SETFR: case INCFR:
    case DECFR: case JUMP:  case BLT: case BLE:   case BEQ:
    case BNE:   case BGE:   case BGT: case CALL:
      printf("%6d%4s", Iseg[loc].Addr, Iseg[loc].Reg ? "[fp]" : " ");
      break;
    default:
      printf("%10c", ' '); }
}

void SetPC(int Addr)                             /* Set program counter */
{
  Pctr = Addr;
}

int PC(void)                                     /* read the content of PC*/
{
  return Pctr;
}

void SetI(OP OpCode, int F, int Addr)            /* write instruction*/
{
    Iseg[Pctr].Op = OpCode;                      /* opcode */
    Iseg[Pctr].Reg = F;                          /* register flag */
    Iseg[Pctr].Addr = Addr;                      /* address */
    if (DebugSW) {
      PrintIns(Pctr); printf("\n"); }
    if (++Pctr > MaxPC) MaxPC = Pctr;            /* Too long program... */
}

void Bpatch(int Loc, int Target)                 /* backpatching */
{
  while (Loc >= 0) { int p;
    if ((p=Iseg[Loc].Addr) == Loc) {
      printf("Trying to rewrite self address part at loc. %d\n", p);
      return; }
    Iseg[Loc].Addr = Target;
    Loc = p; }
}

#define BINOP(OP) {Stack[SP-1] = Stack[SP-1] OP Stack[SP]; SP--;}

int StartVSM(int StartAddr, int TraceSW)         /* Start VSM */
{
  int addr, op;

  Pctr = StartAddr;                              /* Set Pctr */
  SP = Freg = 0;                                 /* Set register flag */
  while (1) {
    if (SP >= STACK_SIZE || SP < 0) {            /* check the range of stack pointer */
      fprintf(stderr, "Illegal Stack pointer %d\n", SP);
      return -1; }
    op   = Iseg[Pctr].Op;                        /* fetch instruction */
    addr = Iseg[Pctr].Addr;                      /* calculate effective address */
    if (Iseg[Pctr++].Reg & FP)                   /* FP register modification */
      addr += Freg;                              /* add FP */
    InsCount++;                                  /* Increment the number of instructions */
    if (SP > MaxSD) MaxSD = SP;                  /* check the max SP value */
    if (TraceSW) {                               /* if trace flag is on, make trace */
      PrintIns(Pctr-1);
      printf("%15d %5d %12d\n", addr, SP, Stack[SP]); }
    switch (op) {                                /* execute each instruction */
      case NOP:                                              continue;
      case ASSGN:  addr = Stack[--SP];
                   Dseg[addr] = Stack[SP] = Stack[SP+1];     continue;
      case ADD:    BINOP(+);                                 continue;
      case SUB:    BINOP(-);                                 continue;
      case MUL:    BINOP(*);                                 continue;
      case DIV:    if (Stack[SP] == 0) {
                     yyerror("Zero divider detected"); return -2; }
                   BINOP(/);                                 continue;
      case MOD:    if (Stack[SP] == 0) {
                     yyerror("Zero divider detected"); return -2; }
                   BINOP(%);                                 continue;
      case CSIGN:  Stack[SP] = -Stack[SP];                   continue;
      case AND:    BINOP(&&);                                continue;
      case OR:     BINOP(||);                                continue;
      case NOT:    Stack[SP] = !Stack[SP];                   continue;
      case COMP:   Stack[SP-1] = Stack[SP-1] > Stack[SP] ? 1 :
                                 Stack[SP-1] < Stack[SP] ? -1 : 0;
                   SP--;                                     continue;
      case COPY:   ++SP; Stack[SP] = Stack[SP-1];            continue;
      case PUSH:   Stack[++SP] = Dseg[addr];                 continue;
      case PUSHI:  Stack[++SP] = addr;                       continue;
      case REMOVE: --SP;                                     continue;
      case POP:    Dseg[addr] = Stack[SP--];                 continue;
      case INC:    Stack[SP] = ++Stack[SP];                  continue;
      case DEC:    Stack[SP] = --Stack[SP];                  continue;
      case SETFR:  Freg = addr;                              continue;
      case INCFR : if ((Freg += addr) >= DSEG_SIZE) {
                     printf("Freg overflow at loc. %d\n", Pctr-1);
                     return -3; }                            continue;
      case DECFR : Freg -= addr;
                   if (Freg < MinFR) MinFR = Freg;           continue;
      case JUMP:   Pctr = addr;           continue;
      case BLT:    if (Stack[SP--] <  0) Pctr = addr;        continue;
      case BLE:    if (Stack[SP--] <= 0) Pctr = addr;        continue;
      case BEQ:    if (Stack[SP--] == 0) Pctr = addr;        continue;
      case BNE:    if (Stack[SP--] != 0) Pctr = addr;        continue;
      case BGE:    if (Stack[SP--] >= 0) Pctr = addr;        continue;
      case BGT:    if (Stack[SP--] >  0) Pctr = addr;        continue;
      case CALL:   Stack[++SP] = Pctr; Pctr = addr; CallC++; continue;
      case RET:    Pctr = Stack[SP--];                       continue;
      case HALT:                                             return 0;
      case INPUT:  scanf("%d", &Dseg[Stack[SP--]]);          continue;
      case OUTPUT: printf("%15d\n", Stack[SP--]);            continue;
      default:
        printf("Illegal Op. code at location %d\n", Pctr);   return -4;
      }
  }
}

void DumpIseg(int first, int last)               /* Display Iseg */
{
  printf("\nContents of Instruction Segment\n");
  for (; first<=last; first++)
    PrintIns(first),  printf("\n");
  printf("\n");
}

void ExecReport(void)                            /* Display code information */
{
  printf("\nObject Code Size:%10d ins.\n", MaxPC);
  printf("Max Stack Depth: %10d\n", MaxSD);
  printf("Max Frame Size:  %10d bytes\n", DSEG_SIZE - MinFR);
  printf("Function calls:  %10d times\n", CallC);
  printf("Execution Count: %10d ins. \n\n", InsCount);
}
