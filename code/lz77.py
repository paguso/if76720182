import math

def prefix_match(txt, pat, ab):
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

def int_encode(x, size, ab):
    base = len(ab)
    codesize = int(math.ceil(math.log(size, base)))
    code = ""
    while x:
        bit = x % base
        code = ab[bit] + code
        x /= base
    return (codesize-len(code))*ab[0] + code


def lz77_encode(txt, ls, ll, ab):
    n = len(txt)
    W = ls*ab[0] + txt
    j = ls
    code = ""
    while j<n+ls:
        p, l = prefix_match(W[j-ls:j],W[j:j+ll],ab)
        code += int_encode(p,ls,ab)
        code += int_encode(l,ll,ab)
        code += W[j+l]
        j += (l+1)
    return code



def main():
    txt = "cbacbacbcacbacbcaac"
    ls = 7
    ll = 4 
    ascab = "0123456789abc"
    #[chr(i) for i in range(128)]
    code = lz77_encode(txt, ls, ll, ascab)
    print code



if __name__ == "__main__":
    main()
