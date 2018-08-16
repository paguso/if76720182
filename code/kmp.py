

def brute_force(txt, pat):
    n = len(txt)
    m = len(pat)
    i = 0
    occ = []
    while i <= n-m :
        j = 0
        while j<m and txt[i+j]==pat[j]:
            j += 1
        if j == m:
            occ.append(i)
        i += 1
    return occ
            

def border_bf(s):
    if s=="":
        return -1
    n = len(s)
    for i in range(n-1,0,-1):
        if s[:i] == s[n-i:] :
            return i
    return 0


def init_next(pat):
    m  = len(pat)
    nxt = (m+1) * [-1]
    for j in range(1,m+1):
        nxt[j] = border_bf(pat[:j])
    return nxt

def kmp(txt, pat):
    n = len(txt)
    m = len(pat)
    nxt = init_next(pat)
    occ = []
    #print nxt
    i,j = 0,0
    while i <= n-m:
        while j<m and pat[j]==txt[i+j]:
            j += 1
        print 
        print txt
        print "%s%s%s"%(i*" ", j*"=", "!" if j<m else "")
        print "%s%s"%(i*" ", pat)
        print

        if j == m :
            occ.append(i)
        i += max (1, j-nxt[j] )
        j = max (0, nxt[j])
    return occ



def main():
    txt = "abracadabra"
    pat = "abra"


    occ_bf = brute_force(txt, pat)
    occ_kmp = kmp(txt, pat)
    #assert occ_bf == occ_kmp
    print occ_bf


if __name__ == "__main__":
    main()

