import math, sys

def prefix_match_bf(txt, pat, ab):
    n = len(txt)
    m = len(pat)
    p = 0
    l = 0
    for i in range(n):
        j = 0
        while j<m-1 and txt[i+j]==pat[j]:
            j+=1
        if j>l:
            p = i
            l = j
    return p,l


def build_fsm(pat, ab):
    m = len(pat)
    l = len(ab)
    delta = {}
    for c in ab:
        delta[(0,c)] = 0
    delta[(0,pat[0])] = 1
    brd = 0
    for i in range(1,m):
        for a in ab:
            delta[(i,a)] = delta[(brd, a)]
        delta[(i,pat[i])] = i+1
        brd = delta[(brd, pat[i])]
    for a in ab:
        delta[(m,a)] = delta[(brd, a)]

    #print "delta pat=",pat 
    #for a in ab:
    #    print a,":", " ".join(map(str, [delta[(i,a)] for i in range(m)]))
    return delta


def prefix_match(window, pat, ab):
    fsm = build_fsm(pat, ab)
    #print fsm
    maxlen = 0
    cur = 0
    pos = 0
    n = len(window)
    ls = n - len(pat)
    for i in range(n):
        cur = fsm[(cur, window[i])]
        if cur > maxlen and i-cur+1 < ls:
            maxlen = cur
            pos = i-cur+1
    maxlen = min(len(pat)-1, maxlen)
    return pos, maxlen


def int_encode(x, size, ab):
    base = len(ab)
    codesize = int(math.ceil(math.log(size, base)))
    code = ""
    while x:
        bit = x % base
        code = ab[bit] + code
        x /= base
    return (codesize-len(code))*ab[0] + code


def int_decode(x, ab):
    base = len(ab)
    power = 1
    val = 0
    for c in x[::-1]:
        val = val + ab.index(c)*power
        power *= base
    return val


def lz77_encode(txt, ls, ll, ab):
    W = ls*ab[0] + txt
    n = len(W)
    j = ls
    code = ""
    while j<n:
        #print "<",W[j-ls:j],"|",W[j:min(n,j+ll)],">"
        p, l = prefix_match(W[j-ls:min(n,j+ll)],W[j:min(n,j+ll)],ab)
        code += int_encode(p,ls,ab)
        code += int_encode(l,ll,ab)
        code += W[j+l]
        j += (l+1)
        print j
    return code


def lz77_decode(code, ls, ll, ab):
    txt = ls*ab[0]
    l = len(ab)
    bs = int(math.ceil(math.log(ls,l)))
    bl = int(math.ceil(math.log(ll,l)))
    j = 0
    sb_init = 0
    while j < len(code):
        p = int_decode(code[j:j+bs], ab)
        j += bs
        l = int_decode(code[j:j+bl], ab)
        j += bl
        c = code[j]
        j+=1
        for i in range(l):
            txt += txt[sb_init+p+i]
        txt += c
        sb_init += (l+1)
    return txt[ls:]




def main():
    ftxt = open(sys.argv[1],"r")
    txt = ""
    for line in ftxt:
        txt += line 
    ascab = [chr(i) for i in range(128)]
    ls = 512 
    ll = 128
    code = lz77_encode(txt, ls, ll, ascab)
    fzip = open(sys.argv[2], "w")
    fzip.write("%s"%code)
    fzip.close()
    ftxt.close()
    #encoded = lz77_decode(code, ls, ll, ascab)
    #print encoded
    #assert txt == encoded



if __name__ == "__main__":
    main()
