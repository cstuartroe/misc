import random
from collections import namedtuple

OP = namedtuple('OutputPattern',['pattern','probability'])

class CFLang:
    #rules is dict of form {'S':[OP('aSb',.4),...],...}
    #where S is variable, aSb is a pattern S may be sent to, and .4 is a probability
    def __init__(self,rules):
        self.rules = rules

    def generate(self):
        string = 'S'
        replace_index = 0
        while not replace_index is None:
            replacement = self.replace(string[replace_index])
            string = string[:replace_index] + replacement + string[replace_index+1:]
            replace_index = self.find_vbl(string)
        return string
        
    def find_vbl(self,string):
        for i in range(len(string)):
            if string[i] in self.rules:
                return i

    def replace(self,vbl):
        replacements = self.rules[vbl]
        r = random.random()
        for i in range(len(replacements)):
            if sum([choice.probability for choice in replacements[:i+1]]) > r:
                return replacements[i].pattern

cfl = CFLang({
    'S':[OP('A I.',.3),OP('A T N.',.7)],
    'I':[OP('slept',.5),OP('ran',.5)],
    'T':[OP('kicked',.5),OP('ate',.5)],
    'N':[OP('A',.4),OP('a baseball',.3),OP('my soup',.3)],
    'A':[OP('john',.4),OP('jane',.3),OP('my sister',.3)]
    })

for i in range(10):
    print(cfl.generate())
