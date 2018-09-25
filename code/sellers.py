import sys

def phi(a,b):
    return int(a!=b)


def sellers(txt, pat, r):
    n = len(txt)
    m = len(pat)
    D = []
    D.append(range(m+1))
    D.append(range(m+1))
    last, prev = 1,0
    occ = []
    for j in range(n):
        D[last][0] = 0
        for i in range(1, m+1):
            D[last][i] = min (D[prev][i-1]+phi(pat[i-1],txt[j]), D[prev][i]+1, D[last][i-1]+1)
        if D[last][m] <= r:
            occ.append(j)
        last = (last+1) % 2
        prev = (prev+1) % 2
    return occ



def amain():
    txt = "abadac"
    pat = "cada"
    r = 2
    occ = sellers(txt, pat, r)
    print occ


def main():
    inpfile = open(sys.argv[1])
    pat = sys.argv[2]
    err = int(sys.argv[3])

    for line in inpfile:
        occ = sellers(line, pat, err)
        if occ:
            print line
    inpfile.close()

if __name__ == "__main__":
    main()
