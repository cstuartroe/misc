from utils import generate_primes, modexp


def solutions_by_prime():
    for p in generate_primes():
        solns = []
        for n in range(1, p):
            if modexp(n, 2, p) + 1 == p:
                solns.append(n)
        yield p, solns


if __name__ == "__main__":
    for p, solns in solutions_by_prime():
        print(p, solns)
        if p > 1000:
            break
