def eratosthenes(maximum):
    maximum += 1
    table = [False] * maximum
    table[1] = True
    print("1 is prime.")

    for n in range(2, maximum):
        if table[n] == False:
            print(f"{n} is prime.")

            for nn in range(n, maximum, n):
                table[nn] = True

if __name__ == '__main__':
    eratosthenes(23)
