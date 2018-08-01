#统计字符个数
def numericals(s):
   lens = len(s)
   lnum = []
   for i in range(0,lens):
       cn = s[0:i+1].count(s[i])
       lnum.append(cn)
   snum = map(str, lnum)
   return ''.join(snum)


a= numericals("Hello, World! It's me, JomoPipi!")
print(a)
#, "1112111121311")
# Test.assert_equals(numericals("Hello, World! It's me, JomoPipi!"), "11121111213112111131224132411122")
# Test.assert_equals(numericals("hello hello"), "11121122342")
# Test.assert_equals(numericals("Hello"), "11121")
# Test.assert_equals(numericals("aaaaaaaaaaaa"),"123456789101112")


#Time out#

