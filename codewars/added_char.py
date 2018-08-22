# Average runtime: ?? ms
#get
def added_char(s1, s2):
    for i in s2:
        flag = 0
        for j in s1:
            if i == j:
                s1 = s1.replace(j, '',1)
                flag = 1
                break
        if flag == 0:
            return i
            break

c = added_char("aabbcc","aacccbbcc")
print (c)