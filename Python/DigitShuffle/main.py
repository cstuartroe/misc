import itertools


def digits_in_base(n: int, base: int) -> tuple[int, ...]:
    if n == 0:
        return ()

    return *digits_in_base(n // base, base), n % base


def digits_to_num(digits: tuple[int, ...], base: int) -> int:
    out = 0
    for i, d in enumerate(digits):
        power = len(digits) - i - 1
        out += d*(base**power)
    return out


def shuffle(n: int, base: int) -> list[int]:
    out = set()

    for perm in itertools.permutations(digits_in_base(n, base)):
        new_n = digits_to_num(perm, base)
        if new_n != n:
            out.add(new_n)

    return sorted(out)


for i in range(1, 101):
    print(i, shuffle(i, 6))
