from utils import generate_primes


def prime_factors(n):
    factors = []

    g = generate_primes()

    p = next(g)

    while p**2 <= n:
        if (n % p) == 0:
            factors.append(p)
            n = n // p
        else:
            p = next(g)

    factors.append(n)

    return factors


def power_products(factors, i=0):
    if i < len(factors):
        p = factors[i]

        out = set()

        for product in power_products(factors, i+1):
            out.add(product)
            out.add(p * product)

        return out

    else:
        return {1}


def abundancy_index(n):
    return sum(power_products(prime_factors(n)))/n


# ABUNDANCY_INDICES = {}
# ABUNDANCY_GROUPS = {}

MAX = 10000000
max_abundancy = 0

for n in (range(2, MAX+1)):
    ai = abundancy_index(n)
    if ai > max_abundancy:
        print(f"{n} has a higher abundancy ({ai}) than any number that precedes it")
        max_abundancy = ai

    # ABUNDANCY_INDICES[n] = ai
    # ABUNDANCY_GROUPS[ai] = ABUNDANCY_GROUPS.get(ai, []) + [n]
