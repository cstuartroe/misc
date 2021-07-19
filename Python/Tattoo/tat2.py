from bitstring import BitArray
from unicodeblock import blocks as ublocks
from tqdm import tqdm

CODEBLOCK_GROUPS = {
    "latin": [
        "BASIC_LATIN",
        "LATIN_1_SUPPLEMENT",
        "LATIN_EXTENDED_LETTER",
        "LATIN_EXTENDED_A",
        "LATIN_EXTENDED_B",
        "IPA_EXTENSIONS",
        "COMBINING_DIACRITICAL_MARKS",
        "LATIN_EXTENDED_ADDITIONAL",
        "LATIN_EXTENDED_C",
    ],
    "greek": [
        "GREEK",
        "GREEK_EXTENDED",
    ],
    "cyrillic": [
        "CYRILLIC",
        "CYRILLIC_SUPPLEMENTARY",
        "CYRILLIC_EXTENDED_A",
    ],
    "arabic": [
        "ARABIC",
        "ARABIC_SUPPLEMENT",
    ],
    "ethiopic": [
        "ETHIOPIC",
        "ETHIOPIC_SUPPLEMENT",
        "ETHIOPIC_EXTENDED",
    ],
    "georgian": [
        "GEORGIAN",
        "GEORGIAN_SUPPLEMENT",
    ],
    "cjk": [
        "CJK_UNIFIED_IDEOGRAPHS",
        "CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A",
    ]
}


CODEBLOCK_PARENTS = {}
for group_name, blocks in CODEBLOCK_GROUPS.items():
    for b in blocks:
        CODEBLOCK_PARENTS[b] = group_name


def block_or_group(c):
    block = ublocks.of(c)
    return CODEBLOCK_PARENTS.get(block, block)


def rrs(ba):
    if isinstance(ba, str):
        ba = BitArray(bytes(ba, "utf-8"))

    out = []
    for _ in range(ba.length):
        try:
            out.append(ba.bytes.decode('utf-8'))
        except UnicodeDecodeError:
            pass
        ba.ror(1)
    ba.reverse()
    for _ in range(ba.length):
        try:
            out.append(ba.bytes.decode('utf-8'))
        except UnicodeDecodeError:
            pass
        ba.ror(1)
    ba.reverse()

    return out


def shared_block(s):
    first_char_block = block_or_group(s[0])
    if first_char_block in {None, "PRIVATE_USE_AREA", "BASIC_PUNCTUATION"}:
        return None
    else:
        if all(block_or_group(c) == first_char_block for c in s[1:]):
            return first_char_block
        else:
            return None


class CharRing:
    def __init__(self, block, chars):
        self.block = block
        self.chars = chars

    def __repr__(self):
        return f"CharRing(block={self.block}, chars={repr(self.chars)})"


class TattooChecker:
    def __init__(self):
        self.seen_rots = set()

    def meaningful_rrs(self, ba):
        out = []

        for rr in rrs(ba):
            block = shared_block(rr)
            if block is not None:
                out.append(CharRing(block=block, chars=rr))

        return out

    def main(self):
        with open("tats.txt", "w") as fh:

            for i in tqdm(range(256 ** 3), total=256**3):
                ba = BitArray(length=24, uint=i)
                if ba.bytes in self.seen_rots:
                    continue

                rrs = self.meaningful_rrs(ba)

                if all(rr.block == 'cjk' for rr in rrs):
                    pass
                else:
                    fh.writelines([f"{[r.chars for r in rrs]} {[r.chars for r in rrs]}\n"])


def all_blocks():
    out = set()
    for i in range(255 ** 3):
        ba = BitArray(length=24, uint=i)
        try:
            c = ba.bytes.decode('utf-8')[0]
            block = ublocks.of(c)
            if block not in out:
                yield block
                out.add(block)
        except UnicodeDecodeError:
            pass


# TattooChecker().main()
# for b in all_blocks():
#     print(b)
while True:
    print(rrs(input()))
