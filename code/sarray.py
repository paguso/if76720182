import sys
import math

def leq_m(a,b,m):
    return a[:m] <= b[:m]


def lt_m(a,b,m):
    return a[:m] < b[:m]


def lcp_bf(X,Y):
    m = len(X)
    n = len(Y)
    i = 0
    while i<m and i<n and X[i]==Y[i]:
        i+=1
    return i


def succ1(txt, pat, sa):
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


def pred1(txt, pat, sa):
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


def succ2(txt, pat, sa, Llcp, Rlcp):
    n = len(txt)
    m = len(pat)
    if lt_m(txt[sa[n-1]:], pat, m):
        return n
    elif leq_m(pat, txt[sa[0]:], m):
        return 0
    else:
        L = lcp_bf(pat, txt[sa[0]:])
        R = lcp_bf(pat, txt[sa[n-1]:])
        l, r = 0, n-1
        while (r-l) > 1 :
            h = (l+r) / 2
            print "l=", l, "  suf_l", txt[sa[l]:]
            print "h=", h, "  suf_h", txt[sa[h]:]
            print "r=", r, "  suf_r", txt[sa[r]:]
            if L >= R:
                if Llcp[h] > L:
                    l = h
                elif Llcp[h] < L:
                    r = h
                    R = Llcp[h]
                else:
                    print "comparing P=",pat, "to", txt[sa[h]:], "from", L 
                    #assert len(pat)>=L and 
                    H = L + lcp_bf(pat[L:], txt[sa[h]+L:])
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
                    H = R + lcp_bf(pat[R:], txt[sa[h]+R:])
                    if H<m  and H<(n-sa[h]) and txt[sa[h]+H]<pat[H]:
                        l, L = h, H
                    else:
                        r, R = h, H
        return r 
                        

def pred2(txt, pat, sa, Llcp, Rlcp):
    n = len(txt)
    m = len(pat)
    if leq_m(txt[sa[n-1]:], pat, m):
        return n-1
    elif lt_m(pat, txt[sa[0]:], m):
        return -1
    else:
        L = lcp_bf(pat, txt[sa[0]:])
        R = lcp_bf(pat, txt[sa[n-1]:])
        l, r = 0, n-1
        while (r-l) > 1 :
            h = (l+r) / 2
            print "l=", l, "  suf_l", txt[sa[l]:]
            print "h=", h, "  suf_h", txt[sa[h]:]
            print "r=", r, "  suf_r", txt[sa[r]:]
            if L >= R:
                if Llcp[h] > L:
                    l = h
                elif Llcp[h] < L:
                    r = h
                    R = Llcp[h]
                else:
                    print "comparing P=",pat, "to", txt[sa[h]:], "from", L 
                    #assert len(pat)>=L and 
                    H = L + lcp_bf(pat[L:], txt[sa[h]+L:])
                    if H<m  and H<(n-sa[h]) and txt[sa[h]+H]>pat[H]:
                        r, R = h, H
                    else:
                        l, L = h, H
            else:
                if Rlcp[h] > R:
                    r = h
                elif Rlcp[h] < R:
                    l = h
                    L = Rlcp[h]
                else:
                    H = R + lcp_bf(pat[R:], txt[sa[h]+R:])
                    if H<m  and H<(n-sa[h]) and txt[sa[h]+H]>pat[H]:
                        r, R = h, H
                    else:
                        l, L = h, H
        return l 


def sa_search(txt, sa, Llcp, Rlcp, pat):
    L = succ2(txt, pat, sa, Llcp, Rlcp)
    R = pred2(txt, pat, sa, Llcp, Rlcp)
    return [sa[i] for i in range(L,R+1)] if L<=R else []



def lcp(P,n, i, j):
    print "computing lcp i=",i, "j=",j

    if i==j:
        return n-i
    else:
        q = len(P)-1
        l = 0
        while q>=0 and i<n and j<n:
            if P[q][i] == P[q][j]:
                l += (2**q)
                i += (2**q)
                j += (2**q)
            q = q-1
        return l

def fill_lrlcp(sa, P, n, l, r, L, R):
    if (r-l)<=1 :
        return 
    h = (l+r)/2
    L[h] = lcp(P, n, sa[l], sa[h])
    R[h] = lcp(P, n, sa[r], sa[h])
    fill_lrlcp( sa, P, n,  l, h, L, R)
    fill_lrlcp( sa, P, n, h, r, L, R)


def lrlcp(sa, P, n):
    L = n*[0]
    R = n*[0]
    fill_lrlcp(sa, P, n, 0, n-1, L, R)
    return L,R


def sort_index(X):
    n = len(X)
    V = [(X[i],i) for i in range(len(X))]
    V.sort()
    S = n*[-1]
    r = 0
    S[V[0][1]] = r
    for i in range(1, n):
        if V[i][0]!=V[i-1][0]:
            r+=1
        S[V[i][1]] = r
    return S


def build_P(txt):
    n = len(txt)
    l = int(math.ceil(math.log(n,2)))
    P = []
    P.append(sort_index(txt))
    for k in range(1,l+1):
        j = 2**(k-1)
        V = []
        for i in range(n):
            if i+j >= n:
                V.append((P[k-1][i],-1))
            else:
                V.append((P[k-1][i],P[k-1][i+j]))
        Pk = sort_index(V)
        print Pk
        P.append(Pk)
    return P


def sa_invert(P):
    n = len(P)
    S = n*[-1]
    for i in range(n):
        S[P[i]] = i
    return S


def main():
    txt = sys.argv[1]
    P = build_P(txt)
    sa = sa_invert(P[-1])
    print sa
    Llcp, Rlcp = lrlcp(sa, P, len(txt))
    print Llcp
    print Rlcp
    pat = sys.argv[2]
    occ = sa_search(txt, sa, Llcp, Rlcp, pat)
    print occ

if __name__ == "__main__":
    main()
