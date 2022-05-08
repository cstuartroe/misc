def to_base(n: int, base: int = 10):
    if n == 0:
        return [0]

    digits = []
    while n:
        digits.append(int(n % base))
        n //= base

    return digits[::-1]


def autolevitate(n: int, base: int = 10):
    return sum(
        d**d
        for d
        in to_base(n, base)
    )


for base in range(2, 11):
    print("base", base)
    for i in range(2, 10000):
        if autolevitate(i, base) == i:
            print(to_base(i, base), i)
