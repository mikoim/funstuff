#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Bot:
    def __init__(self, command):
        self.command = command['command']
        self.data = command['data']
        self.hash = None

    def generate_hash(self):
        def calc(string):
            return modified_scientific_notation(ascii_digits(string))

        self.hash = '{:x}'.format(calc(self.command) + calc(self.data))


def ascii_digits(string):
    """
    Convert string to digits based on ASCII codes.

    >>> ascii_digits('a')  # same as ord('a')
    97
    >>> ascii_digits('ab')
    9798
    >>> ascii_digits('abc')
    979899

    :type string: str
    :rtype: int
    """

    return int(''.join([str(ord(c)) for c in string]))


def modified_scientific_notation(num):
    """
    Convert numerical value to modified scientific notation.

    If length of num is greater than 22, return num as it is.
    >>> modified_scientific_notation(1)
    1

    Otherwise, return concatenated two parts, mantissa without integral part and exponent.
    >>> modified_scientific_notation(123456789012345678901234567890)  # 1.2345678901234568e+29
    234567890123456829

    :type num: int
    :rtype: int
    """

    if len(str(num)) < 22:
        return num

    import re
    p = re.split('(\.|e\+)', '{:.16e}'.format(num))

    return int(p[2] + p[4])


if __name__ == '__main__':
    import doctest

    doctest.testmod()
