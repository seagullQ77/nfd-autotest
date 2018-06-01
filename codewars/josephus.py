def josephus(items,k):
    s = []
    i=0
    li = len(items)
    if li:
        while 1:
            if (i+1)%k == 0:
                s.append(items[i])
            else:
                items.append(items[i])
            i+=1
            if len(s) == li:
                break
        return s
    else:
        return items



s1 = josephus([1,2,3,4,5,6,7,8,9,10],2)
print(s1)
#[2, 4, 6, 8, 10, 3, 7, 1, 9, 5]
s2=josephus(["C","o","d","e","W","a","r","s"],4)
print(s2)
['e', 's', 'W', 'o', 'C', 'd', 'r', 'a']
s3=josephus([1,2,3,4,5,6,7],3)
print(s3)
#[3, 6, 2, 7, 5, 1, 4]
s5 = josephus([],3)
print(s5)
#[]

s = josephus([1,2,3,4,5,6,7,8,9,10],1)
print(s)
#[1,2,3,4,5,6,7,8,9,10]



def josephus(xs, k):
    i, ys = 0, []
    while len(xs) > 0:
        i = (i + k - 1) % len(xs)
        ys.append(xs.pop(i))
    return ys