import math


def cents(r):
    return round(1200 * math.log2(r), 1)


def degree_approximations(edo_steps):
    step_cents = [round(1200 * i / edo_steps) for i in range(edo_steps)]

    RMAX = 32
    cents_ratios = []

    for denom in range(1, RMAX + 1):
        for num in range(denom, RMAX + 1):
            if math.gcd(num, denom) == 1 and (num / denom <= 2):
                cents_ratios.append(((num, denom), cents(num / denom)))

    cents_ratios.sort(key=lambda x: x[1])

    APPROX_THRESHOLD = 1200/(edo_steps*2)
    approximations = {}

    for deg, cents_deg in enumerate(step_cents):
        approximations[deg] = []
        for (num, denom), cents_ratio in cents_ratios:
            if math.fabs(cents_deg - cents_ratio) <= APPROX_THRESHOLD:
                approximations[deg].append((
                    (num, denom),
                    round(cents_deg - cents_ratio, 1),
                ))

    return approximations


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


def compromise_dissonance(n1, n2):
    return euler_dissonance(n1, n2) + gill_purves_dissonance(n1, n2)/10


if __name__ == "__main__":
    for deg, approximations in degree_approximations(31).items():
        print(deg)
        for (num, denom), diff in approximations:
            if compromise_dissonance(denom, num) < 40:
                print(f"{num}:{denom}    {euler_dissonance(denom, num)} {gill_purves_dissonance(denom, num)} ({'+' if diff > 0 else ''}{diff})")
        print()
