import time

class Array: # doesn't support resizing
    def __init__(self,l):
        if type(l) == int:
            self.len = l
            self.list = [None]*self.len
        elif type(l) == list:
            self.len = len(l)
            self.list = l
        else:
            raise TypeError("Invalid type to instantiate Array: " + type(l).__name__)

    def get(self, i):
        return self.list[i]

    def set(self, i, value):
        self.list[i] = value

def brute_prime(n):
    for i in range(2,n):
        if n%i == 0:
            return False
    return True

def search_primes(n):
    return [i for i in range(n) if brute_prime(i)]

def timer(f,args=[],kwargs={}):
    start = time.time()
    f(*args,**kwargs)
    end = time.time()
    return end - start

print(timer(search_primes,[100000]))
