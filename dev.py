import json,os,sys,urllib.request
def post(p,d={}):
    q=urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+p,json.dumps(d).encode(),{'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(q).read())
KN=(-21,-19,-12,-8,8,12,19,21)
VL={'P':100,'N':320,'B':330,'R':500,'Q':900,'K':0}
def fen(f):
    global B,S,C,E
    B=[' ']*120
    for i in range(120):
        if 20<=i<100 and 1<=i%10<=8:B[i]='.'
    p,s,c,e=f.split()[:4];i=21
    for ch in p:
        if ch=='/':i+=2
        elif ch.isdigit():i+=int(ch)
        else:B[i]=ch;i+=1
    S=s=='w';C='' if c=='-' else c;E=0 if e=='-' else (10-int(e[1]))*10+ord(e[0])-96
def sq2i(s):return (10-int(s[1]))*10+ord(s[0])-96
def i2sq(i):return chr(96+i%10)+str(10-i//10)
def uci(m):
    return i2sq(m[0])+i2sq(m[1])+(m[2].lower() if m[2] else '')
def umove(u):return (sq2i(u[:2]),sq2i(u[2:4]),u[4].upper() if len(u)>4 else None)
def atk(b,s,w):
    for d in KN:
        j=s+d
        if 0<=j<120 and b[j]==('N' if w else 'n'):return True
    f=10 if w else -10
    for d in(f-1,f+1):
        if b[s+d]==('P' if w else 'p'):return True
    for d in(-1,1,-10,10,-11,11,-9,9):
        j=s+d
        while 0<=j<120 and b[j]=='.':j+=d
        p=b[j] if 0<=j<120 else ' '
        if p=='.'or p.isupper()!=w:continue
        u=p.upper()
        if u=='Q'or(u=='K'and j==s+d):return True
        if u=='B'and d in(-9,-11,9,11):return True
        if u=='R'and d in(-1,1,-10,10):return True
    return False
def gen(b,s,c,e):
    ms=[]
    for i in range(21,99):
        p=b[i]
        if p=='.'or p==' 'or p.isupper()!=s:continue
        P=p.upper()
        if P=='P':
            d=-10 if s else 10
            t=i+d
            if b[t]=='.':
                if t<30 or t>90:
                    for q in'QNRB':ms.append((i,t,q if s else q.lower()))
                else:ms.append((i,t,None))
            if(81<=i<=88 if s else 31<=i<=38)and b[t]=='.'and b[t+d]=='.':ms.append((i,t+d,None))
            for dd in(d-1,d+1):
                t=i+dd
                if b[t]!='.'and b[t]!=' 'and b[t].isupper()!=s:
                    if t<30 or t>90:
                        for q in'QNRB':ms.append((i,t,q if s else q.lower()))
                    else:ms.append((i,t,None))
                elif e and t==e:ms.append((i,t,None))
        elif P=='K':
            for d in(-1,1,-10,10,-11,11,-9,9):
                t=i+d
                if b[t]=='.'or(b[t]!=' 'and b[t].isupper()!=s):ms.append((i,t,None))
            if s:
                if'K'in c and b[98]=='R'and b[96]==b[97]=='.'and b[95]=='K'and not atk(b,95,not s)and not atk(b,96,not s):ms.append((95,97,None))
                if'Q'in c and b[91]=='R'and b[92]==b[93]==b[94]=='.'and b[95]=='K'and not atk(b,95,not s)and not atk(b,94,not s):ms.append((95,93,None))
            else:
                if'k'in c and b[28]=='r'and b[26]==b[27]=='.'and b[25]=='k'and not atk(b,25,not s)and not atk(b,26,not s):ms.append((25,27,None))
                if'q'in c and b[21]=='r'and b[22]==b[23]==b[24]=='.'and b[25]=='k'and not atk(b,25,not s)and not atk(b,24,not s):ms.append((25,23,None))
        elif P=='N':
            for d in KN:
                t=i+d
                if b[t]=='.'or(b[t]!=' 'and b[t].isupper()!=s):ms.append((i,t,None))
        else:
            ds=(-1,1,-10,10)if P=='R'else(-9,-11,9,11)if P=='B'else(-1,1,-10,10,-11,11,-9,9)
            for d in ds:
                j=i+d
                while b[j]!=' ':
                    if b[j]=='.':ms.append((i,j,None))
                    else:
                        if b[j].isupper()!=s:ms.append((i,j,None))
                        break
                    j+=d
    return ms
def mk(b,m,s,c,e):
    f,t,p=m;pc=b[f];nb=list(b);nb[f]='.';cap=nb[t];ne=0
    if pc in'Pp':
        if t==e and e and cap=='.':nb[t+(10 if s else -10)]='.'
        elif abs(t-f)==20:ne=f+(-10 if s else 10)
    nb[t]=(p.upper() if s else p.lower())if p else pc
    nc=c
    if pc in'Kk':
        nc=c.replace('K','').replace('Q','')if s else c.replace('k','').replace('q','')
        if abs(t-f)==2:
            if t>f:nb[t-1]=nb[t+1];nb[t+1]='.'
            else:nb[t+1]=nb[t-2];nb[t-2]='.'
    for sq,r in((98,'K'),(91,'Q'),(28,'k'),(21,'q')):
        if f==sq or t==sq:nc=nc.replace(r,'')
    return nb,not s,nc,ne
def legal(b,s,c,e,ms):
    out=[]
    for m in ms:
        nb,ns,nc,ne=mk(b,m,s,c,e)
        if not atk(nb,nb.index('K' if s else'k'),not s):out.append(m)
    return out
if __name__=='__main__':
    fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    print(len(legal(B,S,C,E,gen(B,S,C,E))))
