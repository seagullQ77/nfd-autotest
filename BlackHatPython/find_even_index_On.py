from collections import Counter


s1 = "my&friend&Paul has heavy hats! &"
s2 = "my friend John has many many friends &"

def mix(s1, s2):
    c1 = Counter(filter(str.islower, s1))
    c2 = Counter(filter(str.islower, s2))
    res = []

    for c in set(list(c1.keys()) + list(c2.keys())):
        n1, n2 = c1.get(c, 0), c2.get(c, 0)
        if n1 > 1 or n2 > 1:
            res.append(('1', c, n1) if n1 > n2 else('2', c, n2) if n2 > n1 else('=', c, n1))

    res = ["{}:{}".format(i, c * n) for i, c, n in res]
    return "/".join(sorted(res, key=lambda s: (-len(s), s)))