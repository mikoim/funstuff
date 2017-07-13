typedef enum {NEWSYM, FUNC, PARAM, VAR, F_PROT} Class;
typedef enum {VOID, INT} Dtype;

typedef struct STentry{
    unsigned char type, class;
    unsigned char deflvl, Nparam;
    char *name;
    int loc;
} STentry, *STP;

void OpenBlock(void);
void CloseBlock(void);

STP MakeFuncEntry(char *Name);
void FuncDef(STP Funcp, Dtype T);
void Prototype(STP Funcp, Dtype T);
void EndFdecl(STP Funcp);
void VarDecl(char *Name, Dtype T, Class C);
STP SymRef(char *Name);
void UndefCheck(void);

void PrintSymEntry(STP Symp);
