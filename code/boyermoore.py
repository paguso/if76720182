
import sys

def bad_char(pat, ab):
    m = len(pat)
    l = len(ab)
    C = { a:-1 for a in ab }
    for j in range(0,m):
        C[pat[j]] = j
    return C


def sim(x,y):
    return x.endswith(y) or y.endswith(x)

def border_bf(s):
    if s=="":
        return -1
    n = len(s)
    for i in range(n-1,0,-1):
        if s[:i] == s[n-i:] :
            return i
    return 0


def good_suffix(pat):
    m = len(pat)
    S = (m+1) * [m]
    for j in range(0,m):
        for k in range(m-1,0,-1):
            if sim ( pat[j+1:], pat[:k] ):
                S[j] = m - k
                break
    S[-1] = border_bf(pat)   
    return S


def bm(txt, pat, ab, C=None, S=None):
    n = len(txt)
    m = len(pat)
    l = len(ab)
    if not C:
        C = bad_char(pat, ab)
    if not S:
        S = good_suffix(pat)
    occ = []
    i = 0
    while i <= n-m :
        j = m-1
        while j>=0 and txt[i+j]==pat[j] :
            j -= 1
        #print 
        #print txt
        #print "%s%s%s%s"%(i*" ", j*" ", "!" if j>0 else "", (m-j-1)*"=")
        #print "%s%s"%(i*" ", pat)
        #print
        if j == -1:
            occ.append(i)
            i += S[-1]
        else:
            i += max(S[j], j-C[txt[i+j]])
    return occ




def amain():
    txt = "abracadabra"
    pat = "abra"
    ab  = map(chr, range(32,127)) 
    
    occ = bm(txt, pat, ab )

    print occ


def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    ab  = map(chr, range(0,256)) 

    nocc = 0
    C = bad_char(pat, ab)
    S = good_suffix(pat)
    for line in inpfile:
        occ = bm(line, pat, ab, C, S)
        print line 
        if occ:
            print line
        nocc += len(occ)
    inpfile.close()
    print pat, "occurred", nocc, "times"

if __name__ == "__main__":
    main()
