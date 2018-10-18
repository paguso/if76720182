

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
    def __str__(self):
        return "[id="+str(self.id)+ " l="+str(self.l)+" r="+str(self.r)+" slink="+(str(self.slink.id if self.slink else -1))+"]"

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


''' 
(u,(l,r)) ref canonica para vertice ativo da arvore T(i-1)
'''
def update((u,(l,r)), txt, i):
    #print "start update form active <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
    w_prev = None
    (is_term, w) = test_and_split((u,(l,r)), txt, i)
    while not is_term:
        print "  add leaf to <", w, ">"
        leaf = Node(i)
        w.chd[txt[i]] = leaf
        if w_prev :
            w_prev.slink = w
        w_prev = w
        (u,(l,r)) = canonise((u.slink,(l,r)), txt)
        (is_term, w) = test_and_split((u,(l,r)), txt, i)
        print "w=",w
    #print "  stopped at <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
    if w_prev and w:
        w_prev.slink = w
    return (u,(l,r))


'''
testa se no canonico (u,(l,r)) eh terminador i.e. se tem txt[i]-transicao
e, caso negativo, torna-o explicito
'''
def test_and_split((u,(l,r)), txt, i):
    print "testing <", u, "txt[%d:%d]"%(l,r), txt[l:r],"> has ",txt[i],"-trans" 
    if r<=l:
        if txt[i] in u.chd:
            return (True, u)
        else:
            return (False, u)
    else:
        v = u.chd[txt[l]]
        if txt[v.l+(r-l)]==txt[i] :
            return (True, None)
        else:
            w = Node(v.l, v.l+(r-l))
            v.l += (r-l)
            w.chd[txt[v.l]] = v
            u.chd[txt[w.l]] = w
            return (False, w)


def canonise((u,(l,r)), txt):
    print "canonise <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
    if r<=l:
        return (u,(l,r))
    else:
        v = u.chd[txt[l]]
        while (v.r-v.l)<=(r-l):
            u = v
            l += (v.r-v.l)
            print "downto <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
            if l<r:
                v = u.chd[txt[l]]
        return (u,(l,r))


def ukkonen(txt, ab):
    n = len(txt)
    ground = Node(-1,-1)
    root = Node(-1,0)
    root.slink = ground
    for a in ab:
        ground.chd[a] = root
    print_cst(ground, txt, 0) 
    (u,(l,r)) = (root,(0,0))
    for i in range(n):
        print "start update form active <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
        (u,(l,r)) = update((u,(l,r)), txt, i)
        print "  stopped at <", u, "txt[%d:%d]"%(l,r), txt[l:r],">" 
        (u,(l,r)) = canonise((u,(l,i+1)), txt)
        print_cst(ground, txt, i) 


def main():
    txt = "senselessness"
    ukkonen(txt, "elns")


if __name__ == "__main__":
    main()

