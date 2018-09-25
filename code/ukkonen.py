import sys

class Node(object):
    def __init__(self):
        self.idx = -1
        self.chd = [None, None, None] 


def tree_find(root, s):
    cur = root
    i = 1
    while i<len(s):
        d = s[i]-s[i-1]
        if cur.chd[d+1]:
            cur = cur.chd[d+1]
            i+=1
        else:
            break
    if i==len(s):
        return cur.idx
    else:
        return None


def tree_add(root, s, idx):
    cur = root
    i = 1
    while i<len(s):
        d = s[i]-s[i-1]
        if cur.chd[d+1]:
            cur = cur.chd[d+1]
            i+=1
        else:
            break
    while i<len(s):
        nn = Node()
        nn.idx = idx
        d = s[i] - s[i-1]
        cur.chd[d+1] = nn
        cur = nn
        i += 1



def next_column(s, pat, a, r):
    m = len(pat)
    t = (m+1 ) * [0]
    for i in range(1, m+1):
        t[i] = min(s[i]+1, t[i-1]+1, s[i-1]+int(pat[i-1]!=a), r+1 )
    return tuple(t)



def build_ukk_fsm(pat, ab, r):
    m = len(pat)
    s = tuple(range(0, m+1))
    queue = [(s,0)]
    Q = Node() 
    tree_add(Q, s, 0)
    F = set()
    idx = 0
    delta = {}
    if s[-1] <= r:
        F.add(idx)
    while queue:
        (s,idx_s) = queue.pop(0)
        for a in ab:
            t = next_column(s, pat, a, r)
            idx_t = tree_find(Q,t)
            if idx_t == None:
                idx += 1
                idx_t = idx
                tree_add(Q, t, idx)
                queue.append((t,idx_t))
                if t[-1]<=r :
                    F.add(idx)
            delta[(idx_s, a)] = idx_t
    return (delta, F, idx)




def ukk(txt, pat, ab, r, fsm=None):
    if fsm:
        (delta, F, l) = fsm
    else:
        (delta, F, l) = build_ukk_fsm(pat, ab, r)
    s = 0
    n = len(txt)
    occ = []
    if s in F:
        occ.append(i)
    for i in range(n):
        s = delta[(s,txt[i])]
        if s in F:
            occ.append(i)
    return occ



def amain():
    txt = "abadac"
    pat = "cada"
    ab = "abcd"
    r = 2
    (delta, F, l) = build_ukk_fsm(pat, ab, r)
    print "# states = ",l
    #k = [k for k in delta]
    #k.sort()
    #for sa in k:
    #    print "%d ---[%c]---> %d"%(sa[0], sa[1], delta[sa])
    #print k
    #print delta
    #print F
    occ = ukk(txt, pat, ab, r)
    print occ

def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    ab = [chr(i) for i in range(128)]
    err = int(sys.argv[3])

    (delta, F, l) = build_ukk_fsm(pat, ab, err)
    print "# states = ",l
    
    for line in inpfile:
        occ = ukk(line, pat, ab, err, (delta, F, l))
        if occ:
            print line
    inpfile.close()


if __name__ == "__main__":
    main()
