from Utils import *
class Bot:
    def __init__(self, speed=0.1):
        self.speed = speed
    def step(self, position, target):
        """[summary]

        Args:
            destination ([type]): [description]
        """        
        return normalize(target - position) * min(self.speed, np.linalg.norm(target - position))
