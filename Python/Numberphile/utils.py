primes = [2]


def generate_primes():
    yield from primes

    n = primes[-1]

    while True:
        n += 1

        if all(n % p != 0 for p in primes):
            primes.append(n)
            yield n


def modexp(base: int, exp: int, mod: int):
    if exp == 0:
        return 1
    elif exp % 2 == 0:
        return (modexp(base, exp//2, mod)**2) % mod
    else:
        return (modexp(base, exp - 1, mod) * base) % mod
