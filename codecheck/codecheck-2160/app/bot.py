#!/usr/bin/env python3

__all__ = ['Bot']


class Bot:
    def __init__(self, command, data):
        self._command = command
        self._data = data
        self._hash = None

    @property
    def command(self):
        """
        :rtype: str
        """
        return self._command

    @property
    def data(self):
        """
        :rtype: str
        """
        return self._data

    @property
    def hash(self):
        """
        :rtype: str
        """

        def calc(string):
            return modified_scientific_notation(ascii_digits(string))

        if not self._hash:
            self._hash = self._hash = '{:x}'.format(calc(self._command) + calc(self._data))

        return self._hash


def ascii_digits(string):
    """
    Convert string to digits based on ASCII codes.

    >>> ascii_digits('a')  # same as ord('a')
    97

    >>> ascii_digits('ab')
    9798

    >>> ascii_digits('abc')
    979899

    >>> ascii_digits('I ♥️ Python.')
    Traceback (most recent call last):
    ...
    ValueError: string has non-ascii character

    :type string: str
    :rtype: int
    """

    digits = [ord(c) for c in string]
    if any(d > 127 for d in digits):
        raise ValueError('string has non-ascii character')

    return int(''.join([str(d) for d in digits]))


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
