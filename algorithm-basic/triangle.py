import timeit


def triangle(n: int) -> int:
    """
    fastest method
    """
    return sum([x for x in range(1, n + 1)])


def triangle_for(n: int) -> int:
    """
    2nd method
    """
    sum = 0
    for i in range(1, n + 1):
        sum += i
    return sum


def triangle_recursion(n: int) -> int:
    """
    slowest method
    Three times slower than other two methods.
    """
    if n == 1:
        return 1
    else:
        return triangle_recursion(n - 1) + n


if __name__ == '__main__':
    print(
        triangle(5),
        triangle_for(5),
        triangle_recursion(5)
    )

    print(
        timeit.timeit('triangle(100)', number=10000, globals=globals()),
        timeit.timeit('triangle_for(100)', number=10000, globals=globals()),
        timeit.timeit('triangle_recursion(100)', number=10000, globals=globals())
    )
