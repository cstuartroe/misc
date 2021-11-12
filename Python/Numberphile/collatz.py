STOPPING_TIMES = {
    1: 0,
}


max_ventured = [1]


def get_stopping_time(n):
    if n in STOPPING_TIMES:
        return STOPPING_TIMES[n]

    if n > max_ventured[-1]:
        max_ventured.append(n)

    if n % 2 == 0:
        out = get_stopping_time(n//2) + 1
    else:
        out = get_stopping_time(3*n + 1) + 1

    STOPPING_TIMES[n] = out
    return out


max_stopping_time = -1
max_ventured_length = len(max_ventured)

max_stop_timers = []
max_venture_causers = []

for i in range(1, 10000000):
    st = get_stopping_time(i)

    if st > max_stopping_time:
        print(f"{i} has set a new stopping time record ({st})")
        max_stop_timers.append(i)
        max_stopping_time = st

    if len(max_ventured) > max_ventured_length:
        print(f"Investigating {i} has caused a new max venture to be reached ({max_ventured[-1]})")
        max_venture_causers.append(i)
        max_ventured_length = len(max_ventured)

print(max_stop_timers)
print(max_venture_causers)
print(max_ventured)
