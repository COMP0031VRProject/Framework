from itertools import permutations 
from Trial import *
from TestSuite import *

radius = 1

suite_id = 1
flag_num = 3
distance = 4.46

ts1 = TestSuite(suite_id, flag_num, distance)
perms = permutations(Flag, 5)

# for perm in list(perms): 
#     print(perm)

dist_set = set()

for perm in list(perms): 
    dist = 2
    for i in range(4):
        curr = perm[i]
        next = perm[i+1]
        dist += ts1.distance_between(curr, next)
    dist_set.add(round(dist,2))
print (dist_set)