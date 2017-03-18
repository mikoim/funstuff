CC = clang
OBJFILES = lex.yy.o y.tab.o VSM.o

CalcC  : ${OBJFILES}
	${CC} ${OBJFILES} -ly -ll -o CalcL

VSM.o    : VSM.c VSM.h

lex.yy.o : lex.yy.c y.tab.h VSM.h

lex.yy.c : CalcL.l
	flex -l CalcL.l

y.tab.o : y.tab.c VSM.h

y.tab.c y.tab.h : CalcL.y
	bison -dv -y CalcL.y
