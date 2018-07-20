def wave(str):
    lenstr=len(str)
    list=[]
    for i in range(0,lenstr):
        if str[i] == ' ':
            i+=1
        else:
            str1 = str[:i]+str[i].upper()+str[i+1:]
            list.append(str1)
    return list