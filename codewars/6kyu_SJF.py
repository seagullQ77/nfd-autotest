#短作业优先
def SJF(jobs, index):
    lenlj = len(jobs)
    sumt = jobs[index]
    for i in range(0,lenlj):
        if jobs[i] < jobs[index] :
            sumt =  sumt + jobs[i]
        elif jobs[i] == jobs[index] and i<index:
            sumt = sumt + jobs[i]
        else:
            i+=1
    return sumt
#
#
# a= SJF([3,10,20,1,2], 1)
# print(a)
# # , 100)
# # Test.assert_equals(SJF([3,10,20,1,2], 0), 6)
# # Test.assert_equals(SJF([3,10,20,1,2], 1), 16)