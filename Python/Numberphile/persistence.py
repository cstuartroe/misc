from tqdm import tqdm


def persistence(n):
    if n < 10:
        return 0

    digit_product = 1
    for d in str(n):
        digit_product *= int(d)

    return persistence(digit_product) + 1


max_persistence = 0

for i in range(10000000):
    p = persistence(i)
    if p > max_persistence:
        print(f"{i} has set a new max persistence ({p})!")
        max_persistence = p
