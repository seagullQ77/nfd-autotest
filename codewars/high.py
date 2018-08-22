#Highest Scoring Word

def high(x):
    listx= x.split()
    sumhigh = 0
    for i in listx:
        sum=0
        for j in i:
            sum += ord(j.lower())-96
        if sum>sumhigh:
            sumhigh = sum
            highstr = i
    return highstr




highstr=high('take me to semynak')
print(highstr)
#, 'taxi')
#test.assert_equals(high('what time are we climbing up the volcano'), 'volcano')
#test.assert_equals(high('take me to semynak'), 'semynak')
