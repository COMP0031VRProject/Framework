import json
import math
from Trial import *
from itertools import permutations
from jsonUtils import *

class TestSuite:
    def __init__(self, suite_id, flag_num, distance):
        self.suite_id = suite_id
        self.flag_num = flag_num
        self.distance = distance
        self.trial_id = 0
        self.trials = []

    def distance_between(self, x, y):
        x_val = x.value
        y_val = y.value
        rad_unit = math.pi / 3
        dist = math.sqrt(2 - 2*math.cos((x_val - y_val)*rad_unit))

        return round(dist, 2)
    
    def generate(self):
        combs = list(permutations(Flag, self.flag_num))

        for comb in combs:
            dist = 2
            sequence = []
            for flag in comb:
                sequence.append(flag.name)
            for i in range(self.flag_num - 1):
                curr = comb[i]
                next = comb[i+1]
                dist += self.distance_between(curr, next)

            if round(dist,2) == self.distance:
                self.trial_id += 1
                trial = Trial(self.trial_id, sequence)
                self.trials.append(trial.__dict__)


    def save(self, file):
        data = {
            "suite_id": self.suite_id,
            "flag_num": self.flag_num,
            "distance": self.distance,
            "trials": self.trials
        }

        with open(file, 'w') as f:
            json.dump(data, f)