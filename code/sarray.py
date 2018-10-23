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



def main():
    txt = "baobab"
    pat = "ba"
    txt = sys.argv[1]
    pat = sys.argv[2]
    sa = build_sarr_naive(txt)
    L = succ(txt, pat, sa)
    R = pred(txt, pat, sa)
    for i in range(len(txt)):
        print i,":", txt[sa[i]:] 
    print "L=",L, "R=", R



if __name__ == "__main__":
    main()


