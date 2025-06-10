t = int(input())

alist=[]
blist=[]
klist=[]

for kasus in range(0,t):
    alist.append(int(input()))
    blist.append(int(input()))
    klist.append(int(input()))

for kasus in range(0, t):
    hasil = []
    for x in range(alist[kasus], blist[kasus]+1):
        if x%klist[kasus]==0:
            hasil.append(x)
    print('Case ',kasus+1,':', len(hasil))