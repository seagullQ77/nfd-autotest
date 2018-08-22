def insert_missing_letters(st):
    newlist = []
    lenst = len(st)
    for i in range(0,lenst):
        sti = [st[i]]
        if i==0 or st[0:i].find(st[i])==-1:
            tem=ord(st[i].upper())
            for j in range(tem+1,91):
                cj = chr(j)
                print()
                if st.find(cj.lower())==-1:
                    sti.append(cj)
                    j+=1
                else:
                    j+=1
        newlist.extend(sti)
    return ''.join(newlist)



a=insert_missing_letters("hello")
print(a)
#hIJKMNPQRSTUVWXYZeFGIJKMNPQRSTUVWXYZlMNPQRSTUVWXYZloPQRSTUVWXYZ
#hIJKMNPQRSTUVWXYZeFGIJKMNPQRSTUVWXYZlMNPQRSTUVWXYZloPQRSTUVWXYZ
#hIJKMNPQRSTUVWXYZeFGIJKMNPQRSTUVWXYZlMNPQRSTUVWXYZlMNPQRSTUVWXYZoPQRSTUVWXYZ
#hIJKLMNOPQRSTUVWXYeFGHIJKLMNOPQRSTUVWXYlMNOPQRSTUVWXYlMNOPQRSTUVWXYoPQRSTUVWXY

"""
def insert_missing_letters(s):
    s, lst, found, inside = s.lower(), [], set(), set(s.upper())
    for a in s:
        lst.append(a if a in found else
                   a + ''.join(c for c in map(chr, range(ord(a) - 31, 91)) if c not in inside))
        found.add(a)

    return ''.join(lst)


"""