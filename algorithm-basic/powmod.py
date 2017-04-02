def powmod(a, k, m):
    return pow(a, k) % m

def powmod_opt(a, k, m):
    t = 1
    for _ in range(k):
        t = (t * a) % m
    return t

def powmod_opt_alt(a, k, m):
    if k == 0:
        return 1

    t = powmod_opt_alt(a, int(k / 2), m)
    t = (t * t) % m
    if k % 2 == 1:
        t = (t * a) % m

    return int(t)


if __name__ == '__main__':
    print(powmod(2, 3, 5),powmod_opt(2, 3, 5),powmod_opt_alt(2, 3, 5))
