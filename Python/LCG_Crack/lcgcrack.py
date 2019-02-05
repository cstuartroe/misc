from bitstring import BitString
import itertools
import matplotlib.pyplot as plt

b = BitString("0x73300dd2448e74cca17b394bd086a9941e86b407")
gap = 16
nums = [b[i:i+gap].uint for i in range(0,160,gap)]
diffs = [(nums[i] - nums[i-1]) % 60631 for i in range(1,len(nums))]
us = []
for i in range(len(diffs)-2):
    us.append(abs(diffs[i]*diffs[i+2] - (diffs[i+1])**2))

def gcd(a,b):
    big = max(a,b)
    small = min(a,b)
    while small != 0:
        big, small = small, big%small
    return big

##a_pairs = []
##for i in range(len(nums)-1):
##    for j in range(i+1,len(nums)-1):
##        #print("%d = %da + c" % (nums[i+1],nums[i]))
##        #print("%d = %da + c" % (nums[j+1],nums[j]))
##        if nums[i] > nums[j]:
##            x = nums[i] - nums[j]
##            y = nums[i+1] - nums[j+1]
##        else:
##            x = nums[j] - nums[i]
##            y = nums[j+1] - nums[i+1]
##        #print("%d = %da" % (y,x))
##        a_pairs.append((x,y))
##        #print()
##a_pairs.sort(key=lambda x: x[0])
##a_grads = []
##for i in range(len(a_pairs)-1):
##    grad = (a_pairs[i][1]-a_pairs[i+1][1])/(a_pairs[i][0]-a_pairs[i+1][0])
##    a_grads.append(grad)
##    #if grad == 91.75:
##        #print(a_pairs[i],a_pairs[i+1],
##        #      (a_pairs[i+1][0] - a_pairs[i][0], a_pairs[i+1][1] - a_pairs[i][1]))\
##a_grads.sort()
##
##c_pairs = []
##for i in range(len(nums)-1):
##    for j in range(i+1,len(nums)-1):
##        if nums[i] > nums[j]:
##            x = nums[j] - nums[i]
##            y = nums[j]*nums[i+1] - nums[j+1]*nums[i]
##        else:
##            x = nums[i] - nums[j]
##            y = nums[j+1]*nums[i] - nums[j]*nums[i+1]
##        c_pairs.append((x,y))
##c_pairs.sort(key=lambda x: x[0])
##c_grads = []
##for i in range(len(c_pairs)-1):
##    grad = (c_pairs[i][1]-c_pairs[i+1][1])/(c_pairs[i][0]-c_pairs[i+1][0])
##    c_grads.append(grad)
##    #if grad == 91.75:
##        #print(a_pairs[i],a_pairs[i+1],
##        #      (a_pairs[i+1][0] - a_pairs[i][0], a_pairs[i+1][1] - a_pairs[i][1]))
##c_grads.sort()
