import sys


def build_sarr_naive(txt):
    return sorted(range(len(txt)), key=lambda i:txt[i:])


def leq_m(a,b,m):
    return a[:m] <= b[:m]


def lt_m(a,b,m):
    return a[:m] < b[:m]


def succ(txt, pat, sa):
    n = len(txt)
    m = len(pat)
    if lt_m(txt[sa[n-1]:], pat, m):
        return n
    elif leq_m(pat, txt[sa[0]:], m):
        return 0
    else:
        l,r = 0, n-1 # l < succ <= r
        while r-l>1:
            h = (l+r)/2
            if leq_m(pat, txt[sa[h]:], m):
                r = h
            else:
                l = h
        return r

def pred(txt, pat, sa):
    n = len(txt)
    m = len(pat)
    if leq_m(txt[sa[n-1]:], pat, m):
        return n-1
    elif lt_m(pat, txt[sa[0]:], m):
        return -1
    else:
        l, r = 0, n-1 # l <= pred < r 
        while r-l > 1:
            h = (l+r)/2
            if leq_m(txt[sa[h]:], pat, m) :
                l = h
            else:
                r = h
        return l


def lcp(X,Y):
    m = len(X)
    n = len(Y)
    i = 0
    while i<m and i<n and X[i]==Y[i]:
        i+=1
    return i


def fill_lrlcp(txt, sa, l, r, L, R):
    if (r-l)<=1 :
        return 
    h = (l+r)/2
    L[h] = lcp(txt[sa[l]:], txt[sa[h]:])
    R[h] = lcp(txt[sa[r]:], txt[sa[h]:])
    fill_lrlcp(txt, sa, l, h, L, R)
    fill_lrlcp(txt, sa, h, r, L, R)

def lrlcp(txt, sa):
    n = len(txt)
    L = n*[0]
    R = n*[0]
    fill_lrlcp(txt, sa, 0, n-1, L, R)
    return L,R


def succ2(txt, pat, sa, (Llcp, Rlcp)):
    n = len(txt)
    m = len(pat)
    if lt_m(txt[sa[n-1]:], pat, m):
        return n
    elif leq_m(pat, txt[sa[0]:], m):
        return 0
    else:
        L = lcp(pat, txt[sa[0]:])
        R = lcp(pat, txt[sa[n-1]:])
        l, r = 0, n-1
        while (r-l) > 1 :
            h = (l+r) / 2
            if L >= R:
                if Llcp[h] > L:
                    l = h
                elif Llcp[h] < L:
                    r = h
                    R = Llcp[h]
                else:
                    print "comparing P=",pat, "to", txt[sa[h]:], "from", L 
                    #assert len(pat)>=L and 
                    H = L + lcp(pat[L:], txt[sa[h]+L:])
                    if H<m  and H<(n-sa[h]) and txt[sa[h]+H]<pat[H]:
                        l, L = h, H
                    else:
                        r, R = h, H
            else:
                if Rlcp[h] > R:
                    r = h
                elif Rlcp[h] < R:
                    l = h
                    L = Rlcp[h]
                else:
                    H = R + lcp(pat[R:], txt[sa[h]+R:])
                    if H<m  and H<(n-sa[h]) and txt[sa[h]+H]<pat[H]:
                        l, L = h, H
                    else:
                        r, R = h, H
        return r 
                        


def main():
    txt = "baobab"
    pat = "ba"
    txt = sys.argv[1]
    pat = sys.argv[2]
    sa = build_sarr_naive(txt)
    L = succ(txt, pat, sa)
    Ls = succ2(txt, pat, sa, lrlcp(txt, sa))
    print L
    print Ls
    R = pred(txt, pat, sa)
    for i in range(len(txt)):
        print i,":", txt[sa[i]:] 
    print "L=",L, "R=", R



if __name__ == "__main__":
    main()


