from PIL import Image, ImageDraw
from random import randrange
from bitstring import BitString
from urllib import request as ur

def randapi():
    return eval(ur.urlopen("https://www.random.org/integers/?num=1&min=0&max=16777215&col=1&base=10&format=plain&rnd=new").read().decode("utf-8").strip())

def pyrand():
    return randrange(16777216)

class LCG:
    def __init__(self, mod, mult, add):
        self.mod = mod
        self.mult = mult
        self.add = add
        self.state = 0

    def setstate(self,seed):
        self.state = seed

    def next(self):
        self.state = (self.mult*self.state + self.add)%self.mod
        return self.state

    def __repr__(self):
        return 'LCG(%d,%d,%d)' % (self.mod, self.mult, self.add)

lcg = LCG(16777216, 33, 17)
lcg.setstate(randapi())

def tobits(n):
    return bin(n)[2:].rjust(24,'0')

def random_img(rng,size):
    assert(size%24 == 0)
    out = Image.new("RGB",(size,size))
    for col in range(size):
        bits = ""
        for i in range(size//24):
            bits += tobits(rng())
            
        for row in range(size):
            color = (0,0,0) if bits[row] == "0" else (255,255,255)
            out.putpixel((col,row),color)
    return out

p = random_img(lcg.next,48)
p.save('lcgrand.png')

p = random_img(pyrand,48)
p.save('pyrand.png')

p = random_img(randapi,48)
p.save('randapi.png')
