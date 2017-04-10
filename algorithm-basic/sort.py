import copy
import random

def bubble(lst: list) -> list:
    lst = copy.deepcopy(lst)
    length = len(lst)

    for outside in range(length):
        for inside in range(outside + 1, length):

            a = lst[outside]
            b = lst[inside]
            if a > b:
                lst[outside] = b
                lst[inside] = a

    return lst


def selection(lst: list) -> list:
    lst = copy.deepcopy(lst)
    length = len(lst)

    for sorted in range(length):
        minimumIndex = sorted

        for unsorted in range(sorted + 1, length):
            if lst[minimumIndex] > lst[unsorted]:
                minimumIndex = unsorted

        if minimumIndex != sorted:
            a = lst[sorted]
            b = lst[minimumIndex]
            lst[sorted] = b
            lst[minimumIndex] = a

    return lst


if __name__ == '__main__':
    foo = [random.randint(0, 10) for _ in range(10)]
    print(
        foo,
        bubble(foo),
        selection(foo)
    )
