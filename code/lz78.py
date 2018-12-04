

class Dict(object):
    def __init__(self):
        self.data = {"":0}
        self.datainv = [""]

    def index(self, txt):
        n = len(txt)
        for i in range(n-1,-1,-1):
            if txt[:i] in self.data:
                return self.data[txt[:i]], i

    def find(self, i):
        return self.datainv[i]

    def add(self, w):
        self.data[w] = len(self.data)
        self.datainv.append(w)
        
    def __str__(self):
        return "".join([str(i)+":"+self.datainv[i]+"\n" for i in range(len(self.datainv))])



def int_encode(x, ab):
    if x==0:
        return ab[0]
    base = len(ab)
    code = ""
    while x:
        bit = x % base
        code = ab[bit] + code
        x /= base
    return code

def int_decode(x, ab):
    base = len(ab)
    power = 1
    val = 0
    for c in x[::-1]:
        val = val + ab.index(c)*power
        power *= base
    return val

def gprime(y, ab):
    print "gprime encoding", y
    return y if len(y)<=1 else gprime(int_encode(len(y)-2,ab), ab)+y

def cw_encode(w, ab):
    print "g encoding", w
    return gprime(ab[1]+w, ab)+ab[0]


def encode(txt, ab):
    code = ""
    n = len(txt)
    D = Dict()
    i = 0
    while i<n:
        print txt[:i]+"|"+txt[i:]
        print D
        print
        j, l = D.index(txt[i:])
        print "found", D.find(j)
        cj = cw_encode(int_encode(j, ab), ab)
        print "g(%d)=%s"%(j,cj)
        code = code + cj + txt[i+l]
        print "code=",code
        D.add(txt[i:i+l+1])
        i += l+1
    return code


def decode(code, ab):
    D = Dict()
    i = 0
    n = len(code)
    txt = ""
    while i<n:
        w = code[i]
        l = int_decode(w, ab)
        i += 1 
        while True:
            if code[i]==ab[0]:
                dic_entry = D.find(int_decode(w[1:],ab))
                txt += dic_entry
                i+=1
                c = code[i]
                txt += c
                i+=1
                D.add(dic_entry+c)
                print D
                break
            w = code[i:i+l+2]
            i = i+l+2
            l = int_decode(w,ab)
    return txt

def main():
    txt = "aabcbcbcbacbabcbabccbabb"
    ab = "abc"
    code = encode(txt,ab)
    print code
    decoded = decode(code,ab)
    print decoded
    assert txt==decoded




if __name__ == "__main__":
    main()
