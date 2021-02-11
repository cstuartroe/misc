import math


def cents(r):
    return round(1200 * math.log2(r), 1)


CENTS_31EDO = [round(1200 * i / 31) for i in range(31)]

RMAX = 32
CENTS_RATIOS = []

for denom in range(1, RMAX + 1):
    for num in range(denom, RMAX + 1):
        if math.gcd(num, denom) == 1 and (num / denom <= 2):
            CENTS_RATIOS.append(((num, denom), cents(num / denom)))

CENTS_RATIOS.sort(key=lambda x: x[1])

APPROX_THRESHOLD = 18.5
DEGREE_APPROXIMATIONS = {}

for deg, cents_deg in enumerate(CENTS_31EDO):
    DEGREE_APPROXIMATIONS[deg] = []
    for (num, denom), cents_ratio in CENTS_RATIOS:
        if math.fabs(cents_deg - cents_ratio) <= APPROX_THRESHOLD:
            DEGREE_APPROXIMATIONS[deg].append((
                (num, denom),
                round(cents_deg - cents_ratio, 1),
            ))


def lcm(*ints):
    out = ints[0]
    for n in ints[1:]:
        out = int(out * n / math.gcd(out, n))
    return out


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def euler_dissonance(*ints):
    return sum((n-1) for n in prime_factors(lcm(*ints))) + 1


def vogel_dissonance(*ints):
    return sum((n-1) for n in prime_factors(lcm(*ints)) if n != 2) + 1


def gill_purves_dissonance(n1, n2):
    return round(100*(1-((n1+n2-1)/(n1*n2))))


if __name__ == "__main__":
    for deg, approximations in DEGREE_APPROXIMATIONS.items():
        print(deg)
        for (num, denom), diff in approximations:
            print(f"{num}:{denom}    {vogel_dissonance(denom, num)}   ({'+' if diff > 0 else ''}{diff})")
        print()
