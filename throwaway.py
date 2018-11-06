def relprime(s,t):
    for i in range(2,min(s,t)+1):
        if s%i == 0 and t%i == 0:
            return False
    return True

triples = []

for t in range(1,40,2):
    for s in range(t+2,40,2):
        if relprime(s,t):
            a = s*t
            b = (s**2-t**2)//2
            c = (s**2+t**2)//2
            if c > 1000:
                triples.append((s,t,a,b,c))

by_s = sorted(triples, key = lambda x: x[0])
by_t = sorted(triples, key = lambda x: x[1])
by_a = sorted(triples, key = lambda x: x[2])
by_b = sorted(triples, key = lambda x: x[3])
by_c = sorted(triples, key = lambda x: x[4])
