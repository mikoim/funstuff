import copy

def bubble(lst : list) -> list:
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

if __name__ == '__main__':
    foo = [3, 5, 3, 5]
    print(
        foo,
        bubble(foo)
    )
