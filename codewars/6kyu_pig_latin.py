def pig_latin(s):
    v=['a','e','i','o','u']
    lens = len(s)
    ps = []
    if s.isalpha() :
        sl = s.lower()
        if sl[0] in v:
            return sl+'way'
        else:
            for i in range(0,lens):
                ps.append(sl[i])
                if sl[i] in v:
                    return sl[i:]+''.join(ps[0:i])+'ay'
            return sl+'ay'
    else:
        return None

a=pig_latin("spaghetti")
print(a)
#, "apmay")
#Test.assert_equals(pig_latin("egg"), "eggway")
#Test.assert_equals(pig_latin("spaghetti"), "aghettispay")

