from random import randrange

class ZipfSet:
    def __init__(self, max_word_count=1000):
        l = []

        i = 1
        while round(max_word_count/i) > 0:
            l.append((i, round(max_word_count/i)))
            i += 1

        self.l = l

    def generate_vocabulary(self, vocab_size):
        words = []
        for w, count in self.l:
            words += [w]*count

        out = set()
        while len(out) < vocab_size:
            out.add(words[randrange(len(words))])

        return out

    def sample_knowledge(self, vocab, bin_size):
        out = []

        for i in range(len(self.l)//bin_size):
            known = 0

            start = bin_size*i
            for j in range(bin_size):
                if self.l[start + j][0] in vocab:
                    known += 1

            out.append((start, known))

        return out


if __name__ == "__main__":
    zs = ZipfSet(1000000)

    v = zs.generate_vocabulary(10000)

    k = zs.sample_knowledge(v, 100)

    for a, b in k[:50]:
        print(a, b)

