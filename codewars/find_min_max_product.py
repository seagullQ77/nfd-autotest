
def find_min_max_product(arr, k):
    mina = min(arr)
    maxa = max(arr)
    lena = len(arr)
    #print(lena)
    if 1<k<lena:
        for i in range(1,k):
            mina = mina * arr[lena-i]
            maxa = maxa * arr[lena-1-i]
        return mina, maxa
    elif k==1:
        return mina, maxa
    else:
        return None


arr = [1, -2, -3, 4, 6, 7]

# k = 1: -3, 7
mina,maxa = find_min_max_product(arr, 2)
print(mina,maxa)
#(-3, 7))

# k = 2: -3 * 7 = -21, 6 * 7 = 42
#find_min_max_product(arr, 2)
   # (-21, 42)