

def thirt(n):
    # your code
    lt = [1,10,9,12,3,4]
    strn = str(n)
    sum = 0
    while len(strn)>0:
        le = len(strn)
        for i in range(le):
            a = int(strn[le-1-i]) * lt[i % 6]
            sum += a
        if sum == int(strn):
            break
        else:
           strn = str(sum)
           sum = 0
    return sum
if __name__ == '__main__':
    print('178= %d' % thirt(178))
    # print('8529= %d' % thirt(85299258))
    # print('8529= %d' % thirt(5634))
    # print('8529= %d' % thirt(1111111111))
    # print('8529= %d' % thirt(987654321))

# Test.describe("thirt")
# Test.it("Basic tests")
# Test.assert_equals(thirt(8529), 79)
# Test.assert_equals(thirt(85299258), 31)
# Test.assert_equals(thirt(5634), 57)
# Test.assert_equals(thirt(1111111111), 71)
# Test.assert_equals(thirt(987654321), 30)

