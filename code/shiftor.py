from bitstring import BitArray
import sys

def char_mask(pat, ab):
    m = len(pat)
    C = {a:BitArray(bin=m*"1") for a in ab}
    pos_mask = BitArray(bin=(m-1)*"1"+"0")
    one = BitArray(bin=(m-1)*"0" + "1")
    for i in range(m):
        C[pat[i]] = C[pat[i]] & pos_mask
        pos_mask <<= 1
        pos_mask |= one
    return C


def shift_or(txt, pat, ab, C= None):
    n = len(txt)
    m = len(pat)
    S = BitArray(bin = m*"1")
    C = char_mask(pat, ab) if not C else C
    occ = []
    for i in range(n):
        S = ( S << 1 ) | C[txt[i]]
        if not S[0]:
            occ.append(i-m+1)
    return occ


def amain():
    txt = "abcabab"
    pat = "aba"
    ab = "abc"
    C = char_mask(pat, ab)
    occ = shift_or(txt, pat, ab, C)
    print occ


def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    ab = [chr(i) for i in range(128)]

    nocc = 0
    C = char_mask(pat, ab)
    for line in inpfile:
        print ".",
        occ = shift_or(line, pat, ab, C)
        if occ:
            print line
        nocc += len(occ)
    inpfile.close()
    print pat, "occurred", nocc, "times"




if __name__ == "__main__":
    main()
