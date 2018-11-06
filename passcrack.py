import codecs
from bitstring import BitArray
import hashlib

b64alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'

def ba2b64(bits,bytesize):
    chunks = [int(bits[i:i+6],2) for i in range(0, len(bits), 6)]
    return ''.join([b64alph[chunk] for chunk in chunks])

def int2b64(i,bytesize):
    bits = bin(i)[2:].rjust(bytesize*6,'0')
    #bits = BitArray('uint:%d=%d' % (6*bytesize,i)).bin
    return ba2b64(bits,bytesize)

def passcrack(salt, passhash, bytesize):    
    for i in range(2**(6*bytesize)):
        attempt = int2b64(i,bytesize)
        hasher = hashlib.sha256()
        hasher.update(bytes(salt + attempt, 'ascii'))
        dig = hasher.hexdigest()
        if dig == passhash:
            return attempt

x = passcrack('a8d8585a','b324af3f54ee04f43024aec5bfbe5dda5a6b9bccd6e43c29ecb005598dfc8532',4)
print(x)
