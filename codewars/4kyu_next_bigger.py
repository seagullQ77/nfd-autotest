def next_bigger(n):
    sn = str(n)
    lsn = list(sn)
    cn = 1
    if ''.join(sorted(lsn,reverse = True))== sn:
        return -1
    elif n < 10 :
        return -1
    else:
        i=-1
        lenn = len(sn)
        while i>-lenn:
            j=i-1
            t=i-1
            while j>-lenn-1:
                t = i - 1
                if int(lsn[i]) > int(lsn[j]):
                    lsn[i],lsn[j]=lsn[j],lsn[i]
                    lsns=sorted(lsn[j+1:])
                    lsn= lsn[-lenn-1:j+1]+lsns
                    n = ''.join(lsn)
                    return int(n)
                elif i==-1 and int(lsn[i]) == int(lsn[j]):
                    cn+=1
                    while j <= t:
                        if int(lsn[t]) > int(lsn[j]):
                            lsn[t], lsn[j] = lsn[j], lsn[t]
                            lsns = sorted(lsn[j + 1:])
                            lsn = lsn[-lenn - 1:j + 1] + lsns
                            n = ''.join(lsn)
                            return int(n)
                        else:
                            t-=1
                    j -= 1
                else:
                    while j <= t:
                        if int(lsn[t]) > int(lsn[j]):
                            lsn[t], lsn[j] = lsn[j], lsn[t]
                            lsns = sorted(lsn[j + 1:])
                            lsn = lsn[-lenn - 1:j + 1] + lsns
                            n = ''.join(lsn)
                            return int(n)
                        else:
                            t-=1
                    j-=1
            i-=1
        if cn == lenn:
            return -1
a=next_bigger(15667553649644)
# b=next_bigger(513)
# c=next_bigger(2017)
# d=next_bigger(414)
# f=next_bigger(144)
print(a)
# Test.assert_equals(next_bigger(12),21)
# Test.assert_equals(next_bigger(513),531)
# Test.assert_equals(next_bigger(2017),2071)
# Test.assert_equals(next_bigger(414),441)
# Test.assert_equals(next_bigger(144),414)
#  Testing for 21138722
# It should work for random inputs too: 21182237 should equal 21172238
#  Testing for 15667553649644
# It should work for random inputs too: 15667553944466 should equal 15667553664449


"""
import itertools
def next_bigger(n):
    s = list(str(n))
    for i in range(len(s)-2,-1,-1):
        if s[i] < s[i+1]:
            t = s[i:]
            m = min(filter(lambda x: x>t[0], t))
            t.remove(m)
            t.sort()
            s[i:] = [m] + t
            return int("".join(s))
    return -1


"""