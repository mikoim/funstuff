#!/usr/bin/env python3

import sys

from .calendar import Calender


def main(argv):
    try:
        year, month, week = map(int, argv[:3])
        date_string = argv[3]

        print(Calender(year, month, week).calc(date_string))
    except ValueError as e:
        print(e, file=sys.stderr)
        print(-1)


if __name__ == '__main__':
    main(sys.argv[1:])
