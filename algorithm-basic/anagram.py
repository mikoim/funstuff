import timeit


def anagram(s: str) -> str:
    """
    fastest method
    """
    return ''.join(reversed(s))


def anagram_recursion(s: str) -> str:
    """
    nothing to say
    Three times slower than reversed() way
    """
    if len(s) == 1:
        return s
    return s[-1] + anagram_recursion(s[:-1])


if __name__ == '__main__':
    text = 'lolcat'

    print(
        anagram(text),
        anagram_recursion(text)
    )

    print(
        timeit.timeit('anagram(text)', number=100000, globals=globals()),
        timeit.timeit('anagram_recursion(text)', number=100000, globals=globals())
    )
