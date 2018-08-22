from collections import defaultdict
def merge(*dicts):
    d = defaultdict(list)
    for dict in dicts:
        for key,value in dict.items():
            d[key].append(value)
    return d




d = merge({"A": 1, "B": 2, "C": 3}, {"A": 4, "D": 5})
print (d)


{"A": [1, 4], "B": [2], "C": [3], "D": [5]}