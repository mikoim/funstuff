#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "GLFW/glfw3.h"

#ifndef M_PI
#define M_PI 3.14159265359
#endif

/* othello.h */
typedef struct {
    int x, y;
} Pos2D;

typedef enum {
    EMPTY,
    BLACK,
    WHITE
} Stone;

typedef struct {
    int sizeX, sizeY;
    Stone** board;
    Stone turn;
    Pos2D* settable;
} Othello;

void othello_init(Othello* othello, int sizeX, int sizeY);
void othello_free(Othello* othello);
void othello_clear(Othello* othello);
void othello_dump(const Othello* othello);
void othello_scan(Othello* othello);
int othello_set(Othello* othello, int x, int y);
/* othello.h */

/* othello.c */
void othello_init(Othello* othello, int sizeX, int sizeY) {
    int y;

    othello->sizeX = sizeX;
    othello->sizeY = sizeY;

    othello->board = (Stone**)calloc(othello->sizeX, sizeof(Stone*));

    for (y = 0; y < othello->sizeX; y++) {
        othello->board[y] = (Stone*)calloc(othello->sizeX, sizeof(Stone));
    }

    othello->settable = (Pos2D*)calloc(othello->sizeX * othello->sizeY - 4, sizeof(Pos2D));

    othello_clear(othello);
}

void othello_free(Othello* othello) {
    int y;

    for (y = 0; y < othello->sizeX; y++) {
        free(othello->board[y]);
    }

    free(othello->board);

    free(othello->settable);

    othello->sizeX = -1;
    othello->sizeY = -1;
}

void othello_clear(Othello* othello) {
    int x, y;

    othello->turn = BLACK;

    for (y = 0; y < othello->sizeY; y++) {
        for (x = 0; x < othello->sizeX; x++) {
            othello->board[x][y] = EMPTY;
        }
    }

    othello->board[othello->sizeX / 2 - 1][othello->sizeY / 2 - 1] = WHITE;
    othello->board[othello->sizeX / 2][othello->sizeY / 2 - 1] = BLACK;
    othello->board[othello->sizeX / 2 - 1][othello->sizeY / 2] = BLACK;
    othello->board[othello->sizeX / 2][othello->sizeY / 2] = WHITE;
}

void othello_dump(const Othello* othello) {
    int x, y;

    for (y = 0; y < othello->sizeY; y++) {
        for (x = 0; x < othello->sizeX; x++) {
            switch (othello->board[x][y]) {
                case EMPTY:
                    printf(". ");
                    break;
                case BLACK:
                    printf("B ");
                    break;
                case WHITE:
                    printf("W ");
                    break;
            }
        }

        printf("\n");
    }
}

void othello_scan(Othello* othello) {

}

int othello_set(Othello* othello, int x, int y) {
    if (othello->board[x][y] == EMPTY) {
        othello->board[x][y] = BLACK;
    }

    return 0;
}
/* othello.c */

/* ui.c */
Othello g_othello;
int g_windowSizeX = 800;
int g_windowSizeY = 800;
int g_cursor_x = 0;
int g_cursor_y = 0;

void ui_display_circle(GLdouble x0, GLdouble y0, GLdouble r) {
    int i, d = 32;
    GLdouble x, y;

    glBegin(GL_POLYGON);
    for (i = 0; i < d; i++) {
        x = x0 + r * cos(2 * i * M_PI / d);
        y = y0 + r * sin(2 * i * M_PI / d);

        glVertex2d(x, y);
    }
    glEnd();
}

void ui_display(GLFWwindow* window) {
    int x, y;

    glClear(GL_COLOR_BUFFER_BIT);

    /* オセロのボード */
    glColor3d(0, (double)0xb1 / 0xff, (double)0x6b / 0xff);
    glBegin(GL_POLYGON);
    glVertex2d(g_windowSizeX * 0.01, g_windowSizeY * 0.01);
    glVertex2d(g_windowSizeX * 0.99, g_windowSizeY * 0.01);
    glVertex2d(g_windowSizeX * 0.99, g_windowSizeY * 0.99);
    glVertex2d(g_windowSizeX * 0.01, g_windowSizeY * 0.99);
    glEnd();
    /* オセロのボード */

    glLineWidth(2);

    glColor3d(0, 0, 0);
    for (y = 0; y <= 8; y++) {
        glBegin(GL_LINES);
        glVertex2d(g_windowSizeX * 0.02, 0.02 * g_windowSizeY + 0.12 * y * g_windowSizeY);
        glVertex2d(g_windowSizeX * 0.98, 0.02 * g_windowSizeY + 0.12 * y * g_windowSizeY);
        glEnd();

        for (x = 0; x <= 8; x++) {
            glBegin(GL_LINES);
            glVertex2d(0.02 * g_windowSizeX + 0.12 * x * g_windowSizeX, g_windowSizeY * 0.02);
            glVertex2d(0.02 * g_windowSizeX + 0.12 * x * g_windowSizeX, g_windowSizeY * 0.98);
            glEnd();
        }
    }

    for (y = 0; y < 8; y++) {
        for (x = 0; x < 8; x++) {
            switch (g_othello.board[x][y]) {
                case BLACK:
                    glColor3d(0, 0, 0);
                    ui_display_circle(0.08 * g_windowSizeX + 0.12 * x * g_windowSizeX, 0.08 * g_windowSizeY + 0.12 * y * g_windowSizeY, g_windowSizeX < g_windowSizeY ? g_windowSizeX * 0.04 : g_windowSizeY * 0.04);
                    break;
                case WHITE:
                    glColor3d(1, 1, 1);
                    ui_display_circle(0.08 * g_windowSizeX + 0.12 * x * g_windowSizeX, 0.08 * g_windowSizeY + 0.12 * y * g_windowSizeY, g_windowSizeX < g_windowSizeY ? g_windowSizeX * 0.04 : g_windowSizeY * 0.04);
                    break;
                case EMPTY:
                    break;
            }

            if (g_cursor_x == x && g_cursor_y == y) {
                glColor3d(1, 0, 0);
                ui_display_circle(0.08 * g_windowSizeX + 0.12 * x * g_windowSizeX, 0.08 * g_windowSizeY + 0.12 * y * g_windowSizeY, g_windowSizeX < g_windowSizeY ? g_windowSizeX * 0.01 : g_windowSizeY * 0.01);
            }
        }
    }

    glfwSwapBuffers(window);
}

void ui_callback_windowSize(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
    glLoadIdentity();
    glOrtho(-0.5, (GLdouble)width - 0.5, (GLdouble)height - 0.5, -0.5, -1.0, 1.0);
    glfwGetWindowSize(window, &g_windowSizeX, &g_windowSizeY);
}

void ui_callback_key_cursor(int key) {
    switch (key) {
        case GLFW_KEY_UP:
            g_cursor_y--;
            break;
        case GLFW_KEY_DOWN:
            g_cursor_y++;
            break;
        case GLFW_KEY_LEFT:
            g_cursor_x--;
            break;
        case GLFW_KEY_RIGHT:
            g_cursor_x++;
            break;
    }

    if (g_cursor_x < 0) {
        g_cursor_x = 7;
    } else if (g_cursor_x > 7) {
        g_cursor_x = 0;
    }

    if (g_cursor_y < 0) {
        g_cursor_y = 7;
    } else if (g_cursor_y > 7) {
        g_cursor_y = 0;
    }

    printf("%d, %d\n", g_cursor_x, g_cursor_y);
}

void ui_callback_key(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (action == GLFW_PRESS) {
        switch (key) {
            case GLFW_KEY_ESCAPE:
                othello_free(&g_othello);
                break;
            case GLFW_KEY_SPACE:
                othello_set(&g_othello, g_cursor_x, g_cursor_y);
                break;
            case GLFW_KEY_UP:
            case GLFW_KEY_DOWN:
            case GLFW_KEY_LEFT:
            case GLFW_KEY_RIGHT:
                ui_callback_key_cursor(key);
                break;
        }
    }
}

void ui_callback_cursor(GLFWwindow* window, double x, double y) {
    double xx, yy;

    xx = round(0.5 + (8 * x) / (18 + 0.98 * g_windowSizeX));
    yy = round(0.5 + (8 * y) / (18 + 0.98 * g_windowSizeY));

    if (xx >= 1 && xx <= 8 && yy >= 1 && yy <= 8) {
        g_cursor_x = xx - 1;
        g_cursor_y = yy - 1;
    }
}

void ui_callback_click(GLFWwindow* window, int button, int action, int mods) {
    if (action == GLFW_PRESS) {
        othello_set(&g_othello, g_cursor_x, g_cursor_y);
    }
}


void ui_init(GLFWwindow* window) {
    ui_callback_windowSize(window, g_windowSizeX, g_windowSizeY);
}

/* ui.c */

int main()
{
    GLFWwindow* window;

    othello_init(&g_othello, 8, 8);

    if (!glfwInit()) { return -1; }
    if (!(window = glfwCreateWindow(g_windowSizeX, g_windowSizeY, "Othello", NULL, NULL)))
    {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glfwSetWindowSizeCallback(window, ui_callback_windowSize);
    glfwSetKeyCallback(window, ui_callback_key);
    glfwSetCursorPosCallback(window, ui_callback_cursor);
    glfwSetMouseButtonCallback(window, ui_callback_click);

    ui_init(window);

    while (!glfwWindowShouldClose(window))
    {
        ui_display(window);

        glfwPollEvents();

        if (g_othello.sizeX == -1) {
            break;
        }
    }

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
