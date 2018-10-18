

nid = 0

class Node(object):
    def __init__(self, l, r=float('inf')):
        """TODO: to be defined1. """
        global nid
        self.id = nid
        nid+=1
        self.l = l
        self.r = r
        self.chd = {}
        self.slink = None

def print_node(node, level, txt, end):
    print level*" ", 
    print "[id="+str(node.id)+ " l="+str(node.l)+" r="+str(node.r)+" in_edge="+txt[node.l: end+1 if node.r==float('inf') else node.r]+" slink="+(str(node.slink.id if node.slink else -1))+"]"
    ll = node.chd.keys()
    ll.sort()
    for a in ll:
        print_node( node.chd[a], level+1, txt, end)



def print_cst(ground, txt, end):
    root = ground.chd[ground.chd.keys()[0]]
    print_node(root, 0, txt, end)
    print "------------------------------"




# find the locus of x already represented in the tree
def find_locus(root, x):
    m = len(x)
    cur = root
    i = 0
    while i<m:
        nxt = cur.chd[x[i]]
        edge_len = nxt.r - nxt.l
        if edge_len <= m-i:
            cur = nxt
            i += edge_len
        else:
            return (cur, (nxt.l,nxt.l+(m-i)))
    return (cur, (0,0))



def update((u,(l,r)), txt, i):
    w_prev = None
    (is_term, w) = test_and_split((u,(l,r)), txt, i)
    while not is_term:
        leaf = Node(i)
        if w_prev :
            w_prev.slink = w
        w_prev = w
        (u,(l,r)) = canonise((u,(l,r)), txt)
        (is_term, w) = test_and_split((u,(l,r)), txt, i)
    if w_prev :
        w_prev.slink = w
    return (u,(l,r))


def test_and_split((u,(l,r)), txt, i):
    if r<=l:
        if txt[i] in u.chd:
            return (True, None)
        else:
            return (False, u)
    else:
        v = u.chd[txt[l]]
        if txt[u.l+(r-l)]==txt[i] :
            return (True, None)
        else:
            w = Node(u.l+(r-l), u.r)
            w.chd[txt[u.l+(r-l)]] = v
            v.l += (r-l)
            u.chd[txt[l]] = w
            return (False, w)


def canonise((u,(l,r)), txt):
    if r<=l:
        return (u,(l,r))
    else:
        v = u.chd[txt[l]]
        while (v.r-v.l)<=(r-l):
            u = v
            l += (v.r-v.l)
            if l<r:
                v = u.chd[txt[l]]
        return (u,(l,r))


def ukkonen(txt, ab):
    n = len(txt)
    ground = Node(-1)
    root = Node(0,0)
    for a in ab:
        ground.chd[a] = root
    print_cst(ground, txt, 0) 
    (u,(l,r)) = (root,(0,0))
    for i in range(n):
        (u,(l,r)) = update((u,(l,r)), txt, i)
        (u,(l,r)) = canonise((u,(l,r)), txt)
        print_cst(ground, txt, i) 


def main():
    txt = "ababc"
    ukkonen(txt, "abc")


if __name__ == "__main__":
    main()

