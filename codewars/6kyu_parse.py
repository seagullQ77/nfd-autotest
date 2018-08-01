def parse(data):
    result = 0
    lt_result = []
    lend = len(data)
    for i in range(0,lend):
        if data[i] == 'i':
            result = result + 1
        if data[i] == 's':
            result = result ** 2
        if data[i] == 'd':
            result = result - 1
        if data[i] == 'o':
            lt_result.append(result)
    return lt_result

a=parse("codewars")
print(a)
# , [0,0,0])
# Test.assert_equals(parse("ioioio"), [1,2,3])
# Test.assert_equals(parse("idoiido"), [0,1])
# Test.assert_equals(parse("isoisoiso"), [1,4,25])
# Test.assert_equals(parse("codewars"), [0])
