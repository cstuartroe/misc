import matplotlib.pyplot as plt

UP_TO = 1000000

powers = set()

for i in range(2, UP_TO):
    n = i**2

    while n < UP_TO:
        powers.add(n)

        n *= i

powers = sorted(list(powers))

powers_abundance = []
i = 1
powers_seen = 0
powers_i = 0

while i < UP_TO:
    if powers_i < len(powers) and i == powers[powers_i]:
        powers_seen += 1
        powers_i += 1

    powers_abundance.append(powers_seen)

    i += 1

plt.yscale("log")
plt.xscale("log")
plt.plot(powers_abundance)
plt.savefig("blah.png")
