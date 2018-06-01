def compound_match(words, target):
    a0 = None
    a1 = None
    for word in words:
        if a0 == None and word == target[0:len(word)]:
            a0 = words.index(word)
            s0 = word
        if a1 == None and word == target[len(word):]:
            a1 = words.index(word)
            s1 = word
    if a0 != None and a1 != None and s0+s1 == target :
        if a0 < a1:
            return [s0, s1, [a0, a1]]
        else:
            return [s1, s0, [a0, a1]]
    else:
        return None




# arr1 = ['super','bow','bowl','tar','get','book','let']
# arr2 = ['bow','crystal','organic','ally','rain','line']
arr3 = ['top','main','tree','ally','fin','line']
#arr4 = ['bel', 'bed', 'low', 'grab', 'be', 'knight']

# a = compound_match(arr1, 'superbowl')
# print (a)
# b = compound_match(arr2, 'rainbow')
# print(b)

c = compound_match(arr3, 'treefinally')
print(c)