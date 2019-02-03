from copy import deepcopy

class ModNumber:
    def __init__(self,x):
        try:
            assert(round(x) == x)
        except AssertionError:
            raise ValueError("Must intantiate ModNumber from integer")
        self.val = x % self.mod

    def __repr__(self):
        return "%d (mod %d)" % (self.val, self.mod)

    def __str__(self):
        return self.__repr__()

    def verify(self,other):
        if self.mod != other.mod:
            raise ValueError("Mods not equal: (mod %d), (mod %d)" % (self.mod, other.mod))
        return deepcopy(other)

    def __add__(self,other):
        out = self.verify(other)
        out.val = (out.val + self.val) % self.mod
        return out

    def __mul__(self,other):
        out = self.verify(other)
        out.val = 0
        to_add = self.val
        left = other.val
        while left != 0:
            if left%2 == 0:
                to_add = (to_add*2)%self.mod
                left = left / 2
            else:
                out.val = (out.val + to_add)%self.mod
                left = left - 1
        return out

    def __pow__(self,other):
        out = self.verify(other)
        out.val = 1
        to_mul = self.val
        left = other.val
        while left != 0:
            if left%2 == 0:
                to_mul = (to_mul**2)%self.mod
                left = left / 2
            else:
                out.val = (out.val * to_mul)%self.mod
                left = left - 1
        return out

    def __eq__(self,other):
        self.verify(other)
        return self.val == other.val
        
    def makeclass(n):
        class ModNNumber(ModNumber):
            def __init__(self,x):
                self.mod = n
                super(ModNNumber,self).__init__(x)

        return ModNNumber

Mod32416190071Number = ModNumber.makeclass(32416190071)

x = Mod32416190071Number(7435656)
y = Mod32416190071Number(4234323)
