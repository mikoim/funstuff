def isContained(a: list, c) -> bool:
    for elem in a:
        if elem == c:
            return True
    return False

def isContained_opt(a: list, c) -> bool:
    if len(a) == 0 or max(a) < c or min(a) > c:
        return False

    mid = int(len(a) / 2)
    if a[mid] == c:
        return True

    if a[mid] < c:
        return isContained_opt(a[mid:], c)
    else:
        return isContained_opt(a[:mid], c)

if __name__ == '__main__':
    sample = [1,2,3,4,5,6,7,8,9,10]

    print(
        [isContained(sample, x) for x in range(12)],
        [isContained_opt(sample, x) for x in range(12)]
    )
