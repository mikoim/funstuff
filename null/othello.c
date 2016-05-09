#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#pragma message ("LoLoLoLo v0.2.2")
#pragma message ("")
#pragma message ("---============= Options =============---")
#pragma message (" _OSX         Use POSIX API")
#pragma message (" _DEBUG       Enable debug mode")
#pragma message (" _BENCHMARK   Enable performance counter")
#pragma message ("---============= Options =============---")
#pragma message ("")
#ifdef _OSX
#pragma message ("_OSX       O : Use POSIX API")
#else
#pragma message ("_OSX       X : Use Windows API")
#endif
#ifdef _DEBUG
#pragma message ("_DEBUG     O : Enable debug mode")
#else
#pragma message ("_DEBUG     X : Disable debug mode")
#endif
#ifdef _BENCHMARK
#pragma message ("_BENCHMARK O : Enable performance counter")
#else
#pragma message ("_BENCHMARK X : Disable performance counter")
#endif
#pragma message ("")
#pragma message ("[Tips] Compile with optimize option")
#pragma message ("cl /O2 *.c    : M$ C/C++ Compiler")
#pragma message ("clang -O4 *.c : LLVM + Clang")
#pragma message ("gcc -O3 *.c   : GCC")
#pragma message ("")
#ifdef _OSX
#include <pthread.h>
#include <sys/time.h>
#include <unistd.h>
#else
#include <Windows.h>
#endif

/* cui.h */
typedef struct {
    int isBlackPlayer;
    int isWhitePlayer;
    int AI;
} Menu;

void cuiTop(Menu* m);
void cuiPlaying(int* x, int* y);
/* cui.h */

/* reversi.h */
typedef enum {
    None,
    Black,
    White
} Disk;

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    char board_[8][8];
    Point canSet_[30];
    Disk current_;

    int countTurn;
    int countCanSet;
    int countBlack;
    int countWhite;
} Reversi;

Point p_add(Point a, Point b);
Point p_sub(Point a, Point b);
Point p_set(int x, int y);
int p_cmp(const Point* a, const Point* b);

void r_init(Reversi* r);
void r_dump(const Reversi* r);
int r_scan(Reversi* r);
void r_flip(Reversi* r, int x, int y);
int r_set(Reversi* r, Disk d, int x, int y);
/* reversi.h */

typedef void (*pAi)(const Reversi* r, int* x, int* y);

/* ai_stub.h */
void AI_Stub(const Reversi* r, int* x, int* y);
/* ai_stub.h */

/* ai_mc.h */
typedef struct {
    Point pos;
    double rateBlack;
    double rateWhite;
} AI_MC_Data;

typedef struct {
    int countTry, countWinBlack, countWinWhite;
    AI_MC_Data* data;
    const Reversi* orig;
} AI_MC_Thread_Data;

void AI_MC(const Reversi* r, int* x, int* y);

#define MAX_THREADS 32

int g_tryCount = 30000;
/* ai_mc.h */

int main()
{
    Reversi r;
    pAi AI;
    Menu m;
    int x, y;

    srand((unsigned int)time(NULL));

    cuiTop(&m);

    switch (m.AI) {
        case 0:
            AI = &AI_MC;
            break;

        default:
            AI = &AI_Stub;
            break;
    }

    r_init(&r);

    while (r.current_ != None) {
        r_dump(&r);

        switch (r.current_) {
            case Black:
                if (m.isBlackPlayer) {
                    do {
                        cuiPlaying(&x, &y);
                    } while (r_set(&r, Black, x, y) == -1);
                } else {
                    (AI)(&r, &x, &y);
                    printf("[x,y] > %d,%d\n", x, y);
                    if (r_set(&r, Black, x, y) == -1) {
                        printf("AI Error.\n");
                        exit(EXIT_FAILURE);
                    }
                }
                break;

            case White:
                if (m.isWhitePlayer) {
                    do {
                        cuiPlaying(&x, &y);
                    } while (r_set(&r, White, x, y) == -1);
                } else {
                    (AI)(&r, &x, &y);
                    printf("[x,y] > %d,%d\n", x, y);
                    if (r_set(&r, White, x, y) == -1) {
                        printf("AI Error.\n");
                        exit(EXIT_FAILURE);
                    }
                }
                break;

            case None:
                break;
        }
    }

    r_dump(&r);

    if (r.countBlack == r.countWhite) {
        printf("It's a draw.\n");
    } else if (r.countBlack > r.countWhite) {
        printf("Black won by %d.\n", r.countBlack - r.countWhite);
    } else {
        printf("White won by %d.\n", r.countWhite - r.countBlack);
    }

    return 0;
}

/* cui.c */
void benchmark() {
    const long baseline = 2428538; // Mac mini Late 2012 (clang -O4) [microsecond]

    int blackhole;
    unsigned long result;
    Reversi board;
#ifdef _OSX
    struct timeval start, end;
#else
    unsigned long start, end;
#endif

    double rate;

    printf("benchmark() : Wait a moment...\n");

    srand(353535);

    r_init(&board);

#ifdef _OSX
    gettimeofday(&start, NULL);
#else
    start = GetTickCount();
#endif


    AI_MC(&board, &blackhole, &blackhole);
#ifdef _OSX
    gettimeofday(&end, NULL);
#else
    end = GetTickCount();
#endif

#ifdef _OSX
    result = (end.tv_sec - start.tv_sec) * 1000000 + end.tv_usec - start.tv_usec;
#else
    result = (end - start) * 1000;
#endif

    rate = (double)baseline / result;

    g_tryCount = (int)(g_tryCount * rate);

    printf("benchmark() : Baseline %ld / Your system %ld => %f\n", baseline, result, rate);

    if (rate < 0.8) {
        printf("\n[WARNING] Your system is too slow! [WARNING]\n");
    }

    printf("benchmark() : Let's start!\n\n");
}

void cuiTop(Menu* m)
{
    char buf[1000];
    int tmp;

    m->isBlackPlayer = -1;
    m->isWhitePlayer = -1;

    printf("LoLoLoLo v0.2.2\n\n");

#ifdef _DEBUG
    printf("!!! Debug Mode !!!\n");
#endif

    benchmark();

    do {
        printf("Black [AI : 0 / Player : 1] > ");
        fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
        sscanf(buf, "%d", &m->isBlackPlayer);
    } while (m->isBlackPlayer != 0 && m->isBlackPlayer != 1);

    do {
        printf("White [AI : 0 / Player : 1] > ");
        fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
        sscanf(buf, "%d", &m->isWhitePlayer);
    } while (m->isWhitePlayer != 0 && m->isWhitePlayer != 1);

    if (m->isBlackPlayer != 1 || m->isWhitePlayer != 1) {
        do {
            printf("AI [Monte Carlo : 0 / Stub : 1] > ");
            fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
            sscanf(buf, "%d", &m->AI);
        } while (m->AI != 0 && m->AI != 1);

        if (m->AI == 0) {
            do {
                printf("Difficulty [Normal : 0 / Custom : 1] > ");
                fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
                sscanf(buf, "%d", &tmp);
            } while (tmp != 0 && tmp != 1);

            if (tmp == 1) {
                do {
                    printf("Difficulty [1000 - %d] > ", g_tryCount * 4);
                    fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
                    sscanf(buf, "%d", &tmp);
                } while (tmp < 1000 || tmp > g_tryCount * 4);

                g_tryCount = tmp;
            }
        }
    }

    printf("\n");
}

void cuiPlaying(int* x, int* y)
{
    char buf[1000];

    *x = (*y = -1);

    do {
        printf("[x,y] > ");
        fgets(buf , sizeof(buf) / sizeof(buf[0]) , stdin);
        sscanf(buf, "%d,%d", x, y);
    } while (*x < 0 || *x >= 8 || *y < 0 || *y >= 8);
}
/* cui.c */

/* reversi.c */
Point p_add(Point a, Point b)
{
    Point res;

    res = a;
    res.x += b.x;
    res.y += b.y;

    return res;
}

Point p_sub(Point a, Point b)
{
    Point res;

    res = a;
    res.x -= b.x;
    res.y -= b.y;

    return res;
}

Point p_set(int x, int y)
{
    Point res;

    res.x = x;
    res.y = y;

    return res;
}

int p_cmp(const Point* a, const Point* b) {
    if (memcmp(a, b, sizeof(Point)) == 0) return 1;
    return 0;
}

void r_init(Reversi* r)
{
    memset(r->board_, 0, sizeof(r->board_[0][0]) * 64);
    memset(r->canSet_, 0, sizeof(r->canSet_));

    r->current_ = Black;
    r->countTurn = 1;

    r->board_[3][3] = White;
    r->board_[4][3] = Black;
    r->board_[3][4] = Black;
    r->board_[4][4] = White;

    r->countBlack = 2;
    r->countWhite = 2;

    r_scan(r);
}

void r_dump(const Reversi* r)
{
    int x, y, i;
    char overlay[8][8] = {0};

    for (i = 0; i < r->countCanSet; i++) {
        overlay[r->canSet_[i].x][r->canSet_[i].y] = 1;
    }

    printf("===== Turn %2d =====\n", r->countTurn);

    printf(" %c ", r->current_ == Black ? 'B' : 'W');

    for (i = 0; i < 8; i++) {
        printf("%d ", i);
    }

    printf("\n");

    for (y = 0; y < 8; y++) {
        printf(" %d ", y);

        for (x = 0; x < 8; x++) {
            switch (r->board_[x][y]) {
                case None:
                    if (overlay[x][y] == 1) {
                        printf("* ");
                    } else {
                        printf(". ");
                    }
                    break;
                case Black:
                    printf("B ");
                    break;
                case White:
                    printf("W ");
                    break;
            }
        }

        printf("\n");
    }

    printf("=== B %2d / W %2d ===\n", r->countBlack, r->countWhite);

    printf("\n");
}

int r_scan(Reversi* r)
{
    const Point dir[8] = {{0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1}, { -1, -1}, { -1, 0}, { -1, 1}};
    int count = 0, x, y, i, flag, bench = 0;
    Point cur;

    r->countBlack = (r->countWhite = 0);

    for (y = 0; y < 8; y++) {
        for (x = 0; x < 8; x++)	{
            bench++;

            if (r->board_[x][y] == Black) {
                r->countBlack++;
                continue;
            } else if (r->board_[x][y] == White) {
                r->countWhite++;
                continue;
            }

            for (i = 0; i < 8; i++) {
                cur = p_set(x, y);
                flag = 0;

                for (;;) {
                    bench++;
                    cur = p_add(cur, dir[i]);

                    if (cur.x < 0 || cur.y < 0 || cur.x >= 8 || cur.y >= 8) {
                        break;    // Out of bounds.
                    }
                    if (r->board_[cur.x][cur.y] == None) {
                        break;    // Free
                    }
                    if (!flag && r->board_[cur.x][cur.y] == r->current_) {
                        break;    // LoL
                    }

                    if (flag && r->board_[cur.x][cur.y] == r->current_) {
                        r->canSet_[count] = p_set(x, y);
                        count++;

                        flag = -1;

                        break;
                    }

                    if (r->board_[cur.x][cur.y] == (r->current_ == Black ? White : Black)) {
                        flag++;
                    }
                }

                if (flag == -1) {
                    break;
                }
            }
        }
    }

    r->countCanSet = count;

#ifdef _BENCHMARK
    printf("\t\t\t\t\t\t\tr_scan() count = %d / bench = %d\n", count, bench);
#endif

    return count;
}

void r_flip(Reversi* r, int x, int y)
{
    const Point dir[8] = {{0, 1}, {1, 1}, {1, 0}, {1, -1}, {0, -1}, { -1, -1}, { -1, 0}, { -1, 1}};
    int i, flag, bench = 0;
    Point cur;

    for (i = 0; i < 8; i++) {
        cur = p_set(x, y);
        flag = 0;

        for (;;) {
            bench++;
            cur = p_add(cur, dir[i]);

            if (cur.x < 0 || cur.y < 0 || cur.x >= 8 || cur.y >= 8) {
                break;    // Out of bounds.
            }
            if (r->board_[cur.x][cur.y] == None) {
                break;    // Free
            }
            if (!flag && r->board_[cur.x][cur.y] == r->current_) {
                break;    // LoL
            }

            if (flag && r->board_[cur.x][cur.y] == r->current_) {
                cur = p_sub(cur, dir[i]);

                do {
                    r->board_[cur.x][cur.y] = r->current_;
                    cur = p_sub(cur, dir[i]);
                    bench++;
                } while (r->board_[cur.x][cur.y] != r->current_);
                break;
            }

            if (r->board_[cur.x][cur.y] == (r->current_ == Black ? White : Black)) {
                flag++;
            }
        }
    }

#ifdef _BENCHMARK
    printf("\t\t\t\t\t\t\tr_flip() bench = %d\n", bench);
#endif

}

int r_set(Reversi* r, Disk d, int x, int y)
{
    int i = 0;

    if (r->current_ != d) {
#ifdef _DEBUG
        printf("r_set : It's not your turn.\n");
        exit(EXIT_FAILURE);
#endif
        return -1;
    }

    if (r->board_[x][y] != None) {
#ifdef _DEBUG
        printf("r_set : It seems like that (%d,%d) is already using.\n", x, y);
        exit(EXIT_FAILURE);
#endif
        return -1;
    }

    for (i = 0; i < r->countCanSet; i++) {
        if (r->canSet_[i].x == x && r->canSet_[i].y == y) {

            r->board_[x][y] = r->current_;

            r_flip(r, x, y);

            r->current_ = (r->current_ == Black ? White : Black);

            if (r_scan(r) == 0) { // Skip?
                r->current_ = (r->current_ == Black ? White : Black);

                if (r_scan(r) == 0) { // Game Over
                    r->current_ = None;

                    return 1;
                }
            }

            r->countTurn++;

            return 1;
        }
    }

#ifdef _DEBUG
    printf("r_set : (%d,%d) can't be set.\n", x, y);
    exit(EXIT_FAILURE);
#endif

    return -1;
}
/* reversi.c */

/* ai_stub.c */
void AI_Stub(const Reversi* r, int* x, int* y)
{
    int i = rand() % r->countCanSet;

    if (r->countCanSet == 0) {
        printf("AI_Stub() Error.\n");
        exit(EXIT_FAILURE);
    }

    *x = r->canSet_[i].x;
    *y = r->canSet_[i].y;
}
/* ai_stub.c */

/* ai_mc.c */
int getCpuCount() {
    int count;
#ifdef _OSX
    count = (int)sysconf(_SC_NPROCESSORS_ONLN);
#else
    SYSTEM_INFO info;
    GetSystemInfo(&info);
    count = (int)info.dwNumberOfProcessors;
#endif
    return count;
}
#ifdef _OSX
void* AI_MC_Thread(void* args)
#else
DWORD WINAPI AI_MC_Thread(void* args)
#endif
{
    int j, x_, y_;
    Reversi tmp;
    AI_MC_Thread_Data* output = (AI_MC_Thread_Data*)args;

    for (j = 0; j < output->countTry; j++) {

        tmp = *output->orig;

        r_set(&tmp, tmp.current_, output->data->pos.x, output->data->pos.y);

        while (tmp.current_ != None) {
            AI_Stub(&tmp, &x_, &y_);
            r_set(&tmp, tmp.current_, x_, y_);
        }

        if (tmp.countBlack > tmp.countWhite) {
            output->countWinBlack++;
        } else if (tmp.countWhite > tmp.countBlack) {
            output->countWinWhite++;
        }
    }

    #ifdef _OSX
return NULL;
#else
return 0;
#endif
}

int qsort_black(const void *a, const void *b)
{
    AI_MC_Data *cc, *dd;
    cc = (AI_MC_Data*)a;
    dd = (AI_MC_Data*)b;

    if (cc->rateBlack > dd->rateBlack) {
        return -1;
    } else if(cc->rateBlack < dd->rateBlack) {
        return 1;
    } else {
        return 0;
    }
}

int qsort_white(const void *a, const void *b)
{
    AI_MC_Data *cc, *dd;
    cc = (AI_MC_Data*)a;
    dd = (AI_MC_Data*)b;

    if (cc->rateWhite > dd->rateWhite) {
        return -1;
    } else if(cc->rateWhite < dd->rateWhite) {
        return 1;
    } else {
        return 0;
    }
}

void AI_MC(const Reversi* r, int* x, int* y)
{
    AI_MC_Data data[30] = {0}, best;
    int countWinBlack, countWinWhite, i, t, cpu;
    AI_MC_Thread_Data threadData[MAX_THREADS];
#ifdef _OSX
    pthread_t thread[MAX_THREADS];
#else
	HANDLE thread[MAX_THREADS];
#endif
    cpu = getCpuCount();
    if (cpu > MAX_THREADS) cpu = MAX_THREADS;

    for (i = 0; i < r->countCanSet; i++) {
        countWinBlack = 0;
        countWinWhite = 0;

        data[i].pos = r->canSet_[i];

        memset(threadData, 0, sizeof(threadData));

        for (t = 0; t < cpu; t++) {
            threadData[t].countTry = g_tryCount / cpu;
            if (g_tryCount % cpu != 0 && i == cpu - 1) threadData[t].countTry += g_tryCount % cpu;

            threadData[t].data = &data[i];
            threadData[t].orig = r;
            #ifdef _OSX
            pthread_create(&thread[t], NULL, AI_MC_Thread, &threadData[t]);
			#else
			thread[t] = CreateThread(NULL, 0, AI_MC_Thread, &threadData[t], 0, NULL);
			#endif
        }

        for (t = 0; t < cpu; t++) {
			#ifdef _OSX
            pthread_join(thread[t], NULL);
			#else
			WaitForSingleObject(thread[t], INFINITE);
			#endif
            countWinBlack += threadData[t].countWinBlack;
            countWinWhite += threadData[t].countWinWhite;
        }

        data[i].rateBlack = (double)countWinBlack / g_tryCount;
        data[i].rateWhite = (double)countWinWhite / g_tryCount;

        printf("AI_MC(%d) (%d,%d) B %f / W %f\n", g_tryCount, data[i].pos.x, data[i].pos.y, data[i].rateBlack, data[i].rateWhite);
    }

    switch (r->current_) {
        case Black:
            qsort(data, r->countCanSet, sizeof(AI_MC_Data), qsort_black);
            break;

        case White:
            qsort(data, r->countCanSet, sizeof(AI_MC_Data), qsort_white);
            break;

        case None:
            break;
    }

    best = data[0];

    *x = best.pos.x;
    *y = best.pos.y;

    printf("AI_MC(%d) (%d,%d) B %f / W %f [Best!]\n", g_tryCount, best.pos.x, best.pos.y, best.rateBlack, best.rateWhite);
}
/* ai_mc.c */
