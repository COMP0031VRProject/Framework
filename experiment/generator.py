from TestSuite import *
from Trial import *
from itertools import combinations

radius = 1

suite_id = 1
flag_num = 5
distance = 7.46

ts1 = TestSuite(suite_id, flag_num, distance)
ts1.generate()
file_name = './test_' + str(flag_num) + '_'+ str(distance) + '.json'
ts1.save(file_name)
