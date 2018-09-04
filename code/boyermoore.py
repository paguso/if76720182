
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

def init_border(pat):
    m = len(pat)
    nxt = (m+1)*[0] 
    i = 1
    j = 0
    while i+j < m:
        while i+j<m and pat[i+j]==pat[j]:
            j += 1
            nxt[i+j] = j
        i += max(1, (j-nxt[j])) 
        j = nxt[j]
    return nxt
    return [border_bf(s[:j]) for j in range(0,len(s)+1)]

def good_suffix_bf(pat):
    m = len(pat)
    S = (m+1) * [m]
    for j in range(0,m):
        for k in range(m-1,0,-1):
            if sim ( pat[j+1:], pat[:k] ):
                S[j] = m - k
                break
    S[-1] = m-border_bf(pat)   
    return S


def good_suffix(pat):
    m = len(pat)
    R = init_border(pat[::-1])
    #print "border", R
    S = (m+1) * [m-R[m]]
    for l in range(1, m+1) :
        j = m - R[l]
        if S[j] > l - R[l] :
            S[j] = l - R[l]
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
            #print "i=",i
            #print "j=",j,  "S[j]=",S[j], "j-C[]=", j-C[txt[i+j]]
            i += max(S[j], j-C[txt[i+j]])
    return occ




def amain():
    txt="  Of his self-love to stop posterity?"  
    #txt = "abracadabra"
    pat = "love"
    ab  = map(chr, range(0,256)) 
    
    occ = bm(txt, pat, ab )

    print occ


def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    ab  = map(chr, range(0,256)) 

    nocc = 0
    C = bad_char(pat, ab)
    S = good_suffix(pat)
    print "good_suffix_bf", good_suffix_bf(pat)
    print "good_suffix", good_suffix(pat)
    for line in inpfile:
        #print "good suffix", S
        occ = bm(line, pat, ab, C, S)
        #print line 
        #if occ:
        #    print line
        nocc += len(occ)
    inpfile.close()
    print pat, "occurred", nocc, "times"

if __name__ == "__main__":
    main()
