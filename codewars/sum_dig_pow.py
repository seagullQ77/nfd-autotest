import math
def sum_dig_pow(a, b): # range(a, b + 1) will be studied by the function
    # your code here
    lt = []
    for i in range(a,b+1):
        sum = 0
        a = str(i)
        for j in range(len(a)):
            b = math.pow(int(a[j],j+1))
            sum = sum + b

        if sum == i :
            lt.append(i)
        else:
            i += 1

    return lt