def compound_match(words, target):
    l=len(words)
    for i in range(0,l):
        for j in range(i,l):
            if words[i]+words[j] == target:
               return [words[i],words[j],[i,j]]
               break
            if words[j]+words[i] == target:
               return [words[i],words[j],[j,i]]
               break
    return None




arr1 = ['super','bow','bowl','tar','get','book','let']
arr2 = ['bow','crystal','organic','ally','rain','line']
arr3 = ['top','main','tree','ally','fin','line']
#arr4 = ['bel', 'bed', 'low', 'grab', 'be', 'knight']

a = compound_match(arr1, 'superbowl')
print (a)
b = compound_match(arr2, 'rainbow')
print(b)

c = compound_match(arr3, 'treefinally')
print(c)