from app.calculator import parser, lexer


def main(argv):
    if len(argv) != 1:
        exit(1)

    formula = argv[0]

    if len(formula.replace(' ', '')) == 0:
        exit(1)

    if formula.count('(') != formula.count(')'):
        exit(3)

    parser.parse(formula)
