import json
from Trial import *

class TestSuite:
    def __init__(self, suite_id, flag_num, distance):
        self.suite_id = suite_id
        self.flag_num = flag_num
        self.distance = distance
        self.trial_id = 0
        self.trials = []
    
    def generate():
        pass

    def save(self, file):
        data = {
            "suite_id": self.suite_id,
            "flag_num": self.flag_num,
            "distance": self.distance,
            "trials": self.trials
        }

        with open(file, 'w') as f:
            json.dump(data, f)