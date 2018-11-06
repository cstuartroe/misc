import math
import urllib.request as ur
import json
import random
from bitstring import BitArray, BitStream
import codecs

def log2(n):
    return math.log(n)/math.log(2)

def log10(n):
    return math.log(n)/math.log(10)

#accesses the random.org API to generate a random number from atmospheric particle noise
def randomAPI(min,max):
    reqdata = '{"jsonrpc":"2.0","method":"generateIntegers","params":{"apiKey":\
    "3599f140-9b92-4707-86f8-3c5901240643","n":1,"min":%d,"max":%d},"id":87}' % (min,max)
    req = ur.Request('https://api.random.org/json-rpc/1/invoke',data=bytes(reqdata,encoding='utf-8'))
    req.add_header('Content-Type','application/json-rpc')
    with ur.urlopen(req) as response:
        output = response.read()
    j = json.loads(str(output,encoding='utf-8'))
    if j['result']['requestsLeft'] % 50 == 0:
        print('Alert: only %d random.org API requests remaining today.' % j['result']['requestsLeft'])
    return j['result']['random']['data'][0]

def modexp(base,exp,mod):
    total = 1
    while exp > 0:
        if exp%2 == 0:
            base = base*base%mod
            exp = exp//2
        else:
            total = total*base%mod
            exp = exp - 1
    return total

def fermat_test(n,base=2):
    return modexp(base,n-1,n) == 1

def prime_before(n):
    while True:
        if fermat_test(n):
            return n
        else:
            n -= 1

def randprime(bits):
    seed = randomAPI(2**(bits-1),2**bits)
    return prime_before(seed)

def gcd(a,b):
    big = max(a,b)
    small = min(a,b)
    while small != 0:
        big, small = small, big%small
    return big

class LCG:
    def __init__(self, mod, mult, add):
        self.mod = mod
        self.mult = mult
        self.add = add

    def gen(self, seed, length):
        state = seed
        out = []

        for i in range(length):
            state = (self.mult*state + self.add)%self.mod
            out.append(state)

        return out

    def __repr__(self):
        return 'LCG(%d,%d,%d)' % (self.mod, self.mult, self.add)

##lcg = LCG(randprime(16),randomAPI(1,65536),randomAPI(1,65536))
##yes = lcg.gen(randomAPI(1,65536),10)
##ba = BitArray('')
##for term in yes:
##    ba.append('uint:16=%d' % term)
##
code = BitArray('uint:64=%d' % random.randrange(2**64)).hex

##with open('alice.txt','rb') as fh:
##    bytestream = fh.read()
##
##ba = BitArray(bytestream)
##ba.prepend('0b000000')
##ba.append('0b00')
##
##with open('storytime.txt','wb') as fh:
##    fh.write(ba.bytes)
