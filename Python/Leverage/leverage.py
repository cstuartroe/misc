import numpy as np

with open("changes.txt", "r") as fh:
    changes = np.array(
        list(map(float, fh.readlines()))
    )

changes = changes[:1250]

PESSIMISM_INCREMENT = .00005

PERCENTILES_TO_SHOW = [0, .01, .05, .1, .25, .5, .75, .9, .95, .99, 1]

NUM_SAMPLES = 100000

YEARS = 5

LEVERAGE_RATIO = 3

for pessimism in range(1):
    print("Leverage ratio:", LEVERAGE_RATIO)
    print("Years:", YEARS)
    pessimistic_changes = changes - (PESSIMISM_INCREMENT*pessimism)
    print("Average daily change:",  np.mean(pessimistic_changes))
    print("Daily change stdev:", np.std(pessimistic_changes))

    # print(f"Pessimism amount: {pessimism}")

    sampled_gains = []
    leveraged_gains = []

    for _ in range(NUM_SAMPLES+1):
        sampled_changes = np.random.choice(pessimistic_changes, size=252*YEARS)
        sampled_gains.append(np.prod(sampled_changes))

        leveraged_changes = (sampled_changes - 1)*LEVERAGE_RATIO + 1
        leveraged_gains.append(np.prod(leveraged_changes))

    sampled_gains.sort()
    leveraged_gains.sort()

    parity_found = False

    for i, (sg, lg) in enumerate(zip(sampled_gains, leveraged_gains)):
        if i / NUM_SAMPLES in PERCENTILES_TO_SHOW or (not parity_found and lg > sg):
            if lg > sg:
                parity_found = True

            percent = i*100//NUM_SAMPLES
            print(
                f"{percent}%".rjust(4, ' '),
                '',
                f"{round(sg*100, 2)}%".ljust(8, ' '),
                f"{round(lg*100, 2)}%".ljust(9, ' '),
                round((lg-1)/(sg-1), 1),
            )



