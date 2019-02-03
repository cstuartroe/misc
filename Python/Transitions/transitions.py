import numpy as np

with open('corpus.txt','r',encoding='utf-8') as fh:
    readout = fh.read()

alphabet = 'abcdefghijklmnopqrstuvwxyz '

def preprocess(s):
    out = ''
    s = s.lower()
    for i in range(len(s)):
        if s[i] in alphabet:
            out += s[i]
    return out

pped = preprocess(readout)

transitions = np.zeros((27,27))

for i in range(1,len(pped)):
    transitions[alphabet.index(pped[i-1]),alphabet.index(pped[i])] += 1

transitions = transitions[:26,:26]
for i in range(26):
    transitions[i] = transitions[i]/np.sum(transitions[i])

u,m,v = np.linalg.svd(transitions)
