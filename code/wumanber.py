
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


def wu_manber(txt, pat, ab, r, C=None):
    n = len(txt)
    m = len(pat)
    C = C if C else char_mask(pat, ab)
    S = [BitArray(bin = m*"1") for q in range(r+1)]
    occ = []
    for j in range(n):
        S[0] = (S[0] << 1) | C[txt[j]]
        Sprev = S[0]
        for q in range(1,r+1):
            Sprev2 = S[q]
            S[q] = ((S[q]<<1)|C[txt[j]]) & (S[q-1]<<1) & (Sprev<<1) & (Sprev)
            Sprev = Sprev2
        if not S[r][0]:
            occ.append(j)
    return occ


def amain():
    txt = "abadac"
    pat = "cada"
    ab = "abcd"
    r = 2
    C = char_mask(pat, ab)
    occ = wu_manber(txt, pat, ab, r, C)
    print occ


def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    r = int(sys.argv[3])
    ab = [chr(i) for i in range(128)]

    nocc = 0
    C = char_mask(pat, ab)
    for line in inpfile:
        #print ".",
        occ = wu_manber(line, pat, ab,r, C)
        if occ:
            print line
        nocc += len(occ)
    inpfile.close()
    print pat, "occurred", nocc, "times"




if __name__ == "__main__":
    main()
