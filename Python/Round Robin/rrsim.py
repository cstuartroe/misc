import numpy as np
import copy
import matplotlib.pyplot as plt

SAMPLE_SIZE = 100
SWAP_TIME = 1

def rrsim(burst_times,q_percentile):
    s = sorted(burst_times)
    pos = int(SAMPLE_SIZE*q_percentile)
    quantum = s[pos]
    
    print("Percentile:",q_percentile)
    print("Position:", pos)
    print("Time quantum:",quantum)

    remaining_times = copy.copy(burst_times)
    total_time = 0
    finish_times = [0]*SAMPLE_SIZE

    while any(x != 0 for x in remaining_times):
        for i in range(SAMPLE_SIZE):
            if remaining_times[i] > 0:
                to_run = min(quantum, remaining_times[i])
                total_time += SWAP_TIME + to_run
                remaining_times[i] -= to_run

                if remaining_times[i] == 0:
                    finish_times[i] = total_time

    avg_finish = sum(finish_times)/SAMPLE_SIZE
    print("Average finish time:",avg_finish)

    print()
    return avg_finish


exps = np.random.normal(10,4,SAMPLE_SIZE)
BURST_TIMES = list(map(lambda z: int(2**z), exps))

avg_finishes = [0]*9
for j in range(10):
    for i in range(1,10):
        avg_finishes[i-1] += rrsim(BURST_TIMES,i/10)

plt.scatter(avg_finishes,range(1,10))
plt.show()
