import ply.lex as lex
import ply.yacc as yacc

"""
original program from PLY document
http://www.dabeaz.com/ply/ply.html
"""

# lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIV',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = " "


def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    exit(2)


lexer = lex.lex()

# yacc

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('right', 'UMINUS'),
)


def p_statement_expr(t):
    """statement : expression"""
    print(t[1])


def p_expression_binop(t):
    """
    expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression
    """
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] // t[3]


def p_expression_uminus(t):
    """expression : MINUS expression %prec UMINUS"""
    t[0] = -t[2]


def p_expression_group(t):
    """expression : LPAREN expression RPAREN"""
    t[0] = t[2]


def p_expression_number(t):
    """expression : NUMBER"""
    t[0] = t[1]


def p_error(t):
    exit(4)


parser = yacc.yacc()
