def find_even_index(arr):
    arr_len = len(arr)
    #print('arr_len=%d' %arr_len)
    for index in range(0,arr_len):
        sum1 = 0
        sum2 = 0
        for i in range(index,arr_len-1):
            sum1+=arr[i+1]
        for j in range(0,index):
            sum2+=arr[j]
        #print('sum1=%d,sum2=%d'%(sum1,sum2))
        if sum1==sum2:
            return index
    return -1


import unittest
import traceback


class TestEqualSidesOfAnArray(unittest.TestCase):
    def describe(self, des):
        print(des)

    def assert_equals(self, func, exp, msg=None):
        try:
            self.assertEqual(func, exp, msg)
        except AssertionError:
            traceback.print_exc()


if __name__ == '__main__':
    Test = TestEqualSidesOfAnArray()
    Test.describe("Basic tests")
    Test.assert_equals(find_even_index([1, 2, 3, 4, 3, 2, 1]), 3)
    Test.assert_equals(find_even_index([1, 100, 50, -51, 1, 1]), 1)
    Test.assert_equals(find_even_index([1, 2, 3, 4, 5, 6]), -1)
    Test.assert_equals(find_even_index([20, 10, 30, 10, 10, 15, 35]), 3)
    Test.assert_equals(find_even_index([20, 10, -80, 10, 10, 15, 35]), 0)
    Test.assert_equals(find_even_index([10, -80, 10, 10, 15, 35, 20]), 6)
    Test.assert_equals(find_even_index([10]), 0)
    Test.assert_equals(find_even_index(range(1, 100)), -1)
    Test.assert_equals(find_even_index([0, 0, 0, 0, 0]), 0, "Should pick the first index if more cases are valid")
    Test.assert_equals(find_even_index([-1, -2, -3, -4, -3, -2, -1]), 3)
    Test.assert_equals(find_even_index(range(-100, -1)), -1)

    Test.describe("Random tests")
    from random import randint

    find_even_sol = lambda arr, l=0, r="null", i=0: (
    lambda r: -1 if i >= len(arr) else i if r == l else find_even_sol(arr, l + arr[i],
                                                                      r - (0 if i + 1 >= len(arr) else arr[i + 1]),
                                                                      i + 1))(r if r != "null" else sum(arr[1:]))
    contract = lambda arr: (lambda pos: arr[:pos] + [sum(arr[pos:])])(randint(0, len(arr) - 1))

    for _ in range(40):
        left = [randint(-20, 20) for qu in range(randint(10, 20))]
        right = left[:]
        if randint(0, 1): left[randint(0, len(left) - 1)] += randint(-20, 20)
        left = sorted(contract(left), key=lambda a: randint(1, 1000));
        right = sorted(contract(right), key=lambda a: randint(1, 1000))
        arr = ([] + left[:] + [randint(-20, 20)] + right[:])[:]
        # Test.describe("Testing for %s" %arr)
        Test.assert_equals(find_even_index(arr[:]), find_even_sol(arr), "It should work for random inputs too")

# if __name__ == '__main__':
#     arr0 = [1, 2, 3, 4, 3, 2, 1]
#     arr1 = [1, 100, 50, -51, 1, 1]
#     arr2 = [20, 10, -80, 10, 10, 15, 35]
#     index0 = find_even_index(arr0)
#     index1 = find_even_index(arr1)
#     index2 = find_even_index(arr2)
#     print(index0,index1,index2)


