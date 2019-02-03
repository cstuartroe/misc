from bitstring import BitString
import re
import nltk

def dutch_words():
    with open("10000mostfrequentdutchwords.txt","r") as fh:
        lines = fh.readlines()[4:-1]
    words = []
    for line in lines:
        words.append(line.split("\t")[1].strip())
    return words

def chinese_characters():
    with open("3000.txt","r",encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    words = [line for line in lines if len(line)==1]
    return words

def isalpha(word):
    for letter in word:
        if letter not in set("QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"):
            return False
    return True

def isalpha2(word):
    if re.match("[A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff]{%d}" % len(word),word):
        return True
    else:
        return False

def bits(word):
    b = bytes(word,"utf-8")
    return BitString(b)

def loops(bits,start=1):
    for i in range(start,len(bits)):
        looped = bits[i:] + bits[:i]
        try:
            yield looped.tobytes().decode("utf-8")
        except UnicodeDecodeError:
            pass

all_words = dutch_words() + nltk.corpus.words.words()
words_set = set(all_words)

def l(word):
	for newword in loops(bits(word)):
		print(newword)
	for newword in loops(bits(word)[::-1]):
		print(newword)
