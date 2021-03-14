from TestSuite import *
from Trial import *
from itertools import combinations

radius = 1

ts1 = TestSuite(1, 3, 4.46)
ts1.generate()
ts1.save("./test_3_346.json")

# combs = combinations(Flag, 3)

# for comb in list(combs): 
#     dist = 1
#     for i in range(2):
#         curr = comb[i]
#         next = comb[i+1]
#         dist += ts1.distance_between(curr, next)
#     print(dist)
