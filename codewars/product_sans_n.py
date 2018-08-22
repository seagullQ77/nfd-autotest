"""
def product_sans_n(nums):
    lenn = len(nums)
    new_nums = []
    for i in range(0,lenn):
        pro = 1
        for j in range(0,lenn):
            #Product 积
            if i==j:
                j+=1
            else:
                pro = pro*nums[j]
        new_nums.append(pro)
    return new_nums

"""
from copy import deepcopy
from functools import reduce
from operator import mul

def product_sans_n(nums):
    lenn = len(nums)
    new_array = []
    for i in range(0, lenn):
        new_nums = deepcopy(nums)
        del new_nums[i]
        pro = reduce(mul, new_nums)
        new_array.append(pro)
    return new_array




a = product_sans_n([4,7,3,6,2, 11, 14, 4, 7, 5])
print(a)
#, [1, 1, 1])
    # Test.assert_equals(product_sans_n([0,-99,0]), [0, 0, 0])
    # Test.assert_equals(product_sans_n([9,0,-2]), [0, -18, 0])
    # Test.assert_equals(product_sans_n([1,2,3,4]), [24, 12, 8, 6])
    # Test.assert_equals(product_sans_n([2,3,4,5]), [60, 40, 30, 24])
    # Test.assert_equals(product_sans_n([-8,1,5,13,-1]),[-65, 520, 104, 40, -520])
    # Test.assert_equals(product_sans_n([3,14,9,11,11]), [15246, 3267, 5082, 4158, 4158])
    # Test.assert_equals(product_sans_n([4,7,3,6,2, 11, 14, 4, 7, 5]), [5433120, 3104640, 7244160, 3622080, 10866240, 1975680, 1552320, 5433120, 3104640, 4346496])



