from TestSuite import *
from Trial import *
from itertools import combinations

radius = 1

suite_id = 1
flag_num = 3
distance = 4.46

ts1 = TestSuite(suite_id, flag_num, distance)
ts1.generate()
file_name = './test_' + str(flag_num) + '_'+ str(distance) + '.json'
ts1.save(file_name)

# combs = combinations(Flag, 3)

# for comb in list(combs): 
#     dist = 1
#     for i in range(2):
#         curr = comb[i]
#         next = comb[i+1]
#         dist += ts1.distance_between(curr, next)
#     print(dist)
