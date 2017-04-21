#!/usr/bin/env python3
def main(argv):
    for x in argv:
        print(watanize(x))


def watanize(x: str) -> str:
    n = number(x)
    if n is None:
        return 'invalid'

    idiot = n % 3 == 0
    stupid = '3' in x
    dumb = idiot and stupid

    if dumb:
        return 'dumb'
    elif idiot:
        return 'idiot'
    elif stupid:
        return 'stupid'
    else:
        return 'smart'


def number(x: str) -> int:
    try:
        return int(x)
    except ValueError:
        return None
