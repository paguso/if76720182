import sys

def print_fsm(g,f,o,ab):
    nxt = len(o)
    print "goto"
    for s in range(nxt):
        print s,":", 
        for a in ab:
            if (s,a) in g:
                print "%c-->%s"%(a,g[(s,a)])," ",
        print
    print
    print "occ"
    for s in range(nxt):
        print s,":",
        print o[s]
    print 


def build_goto(P, ab):
    g, o = {}, [[]]
    nxt = 0
    for k in range(0, len(P)):
        pat = P[k]
        m = len(pat)
        cur, j = 0, 0
        while j<m and (cur, pat[j]) in g:
            cur = g[(cur, pat[j])]
            j += 1
        while j<m :
            nxt += 1
            o.append([])
            g[(cur, pat[j])] = nxt
            cur = nxt
            j += 1
        o[cur].append(k)
        #print_fsm(g,None,o,ab)

    for a in ab:
        if (0,a) not in g:
            g[(0,a)] = 0
    #print_fsm(g,None,o,ab)
    return g, nxt+1, o



def build_fail(P, ab, g, n, o):
    Q = []
    f = n * [0]
    for a in ab:
        if g[(0,a)] != 0:
            Q.append(g[(0,a)])
            f[g[(0,a)]] = 0
    while Q:
        #print Q
        #raw_input()
        cur = Q.pop(0)
        for a in ab:
            if (cur,a) in  g:
                nxt = g[(cur, a)]
                Q.append(nxt)
                brd = f[cur]
                while (brd, a) not in g:
                    brd = f[brd]
                f[nxt] = g[(brd, a)]
                o[nxt].extend(o[f[nxt]])
    return f, o



def build_fsm(P, ab):
    g, n, o  = build_goto(P, ab)
    f, o = build_fail(P, ab, g, n, o)
    print_fsm(g,f,o,ab)
    return (g, f, o)

def ahocorasick(txt, P, ab, fsm=None):
    n = len(txt)
    m = [len(p) for p in P]
    (g,f,o) = fsm if fsm else build_fsm(P, ab)
    cur = 0
    occ = [[] for pat in P]
    for i in range(n):
        a = txt[i]
        while (cur, a) not in g:
            cur = f[cur]
        cur = g[(cur, a)]
        for p in o[cur]:
            occ[p].append(i-m[p]+1)
    return occ


def oldmain():
    txt = "she sells sea shells at the sea shore for her friends"
    P = ["he", "she", "his", "hers"]
    ab = [chr(i) for i in range(0,128)]
    fsm = build_fsm(P, ab)
    occ = ahocorasick(txt, P, ab, fsm)
    print occ


def main():
    ftxt = open(sys.argv[1], "r")
    fpat = open(sys.argv[2], "r")
    ab = [chr(i) for i in range(0,128)]
    P = []
    for line in fpat:
        P.append(line.strip())
    print "Patterns", P
    fsm = build_fsm(P, ab)
    for line in ftxt:
        occ = ahocorasick(line, P, ab, fsm)
        if sum(map(len, occ))>0:
            print line
    ftxt.close()
    fpat.close()


if __name__ == "__main__":
    main()
