import fractions

def phi(n):
    amount = 0        
    for k in range(1, n + 1):
        if fractions.gcd(n, k) == 1:
            amount += 1
    return amount

def helium(x,p=True):
    i = 0
    while True:
        if p:
            print(x)
        if i == 100:
            return ("X",None)
        if x == 8:
            return ("A",i)
        elif x == 20:
            return ("B",i)
        elif x == 398:
            return ("C",i)
        elif x == 542:
            return ("D",i)
        x = 3*phi(x)/2 + 2
        assert(int(x) == x)
        x = int(x)
        i += 1


content = "Number,Category,Steps\n"
for i in range(4,10001):
    cat, steps = helium(i,False)
    content += "%d,%s,%d\n" % (i, cat, steps)
    if i%1000 == 0:
        print(i)
        with open("helium.csv","w") as fh:
            fh.write(content)
    
