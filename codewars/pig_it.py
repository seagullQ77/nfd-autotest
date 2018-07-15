def pig_it(text):
    lists = text.split(' ')
    print(lists)
    lenls = len(lists)
    for i in range (0,lenls):
        if lists[i][0].isalpha():
            lists[i]=lists[i].lstrip(lists[i][0])+lists[i][0]+'ay'
    text = ' '.join(lists)
    return text

a=pig_it('Pig latin is cool')
print (a)
#'igPay atinlay siay oolcay'
b=pig_it('This is my string')
print(b)
#'hisTay siay ymay tringsay'