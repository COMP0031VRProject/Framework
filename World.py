import numpy as np
from Mesh import Mesh
from Record import Record
class World:
    def __init__(self, virtual_mesh, real_mesh, start_position, bot, targets, threshold=0.1):
        self.virtual_mesh = virtual_mesh
        self.real_mesh = real_mesh
        self.start_position = start_position
        self.bot = bot
        self.virtual_position = start_position
        self.real_position = self.virtual2real(self.virtual_position)
        self.targets = targets
        self.threshold = threshold

    def simulate(self):
        real_record = Record()
        virtual_record = Record()
        real_record.record(self.real_position.copy())
        virtual_record.record(self.virtual_position.copy())

        i = 0
        while i < len(self.targets):
            while not self.reach(self.targets[i]):
                self.real_position += self.bot.step(self.virtual_position, self.targets[i])
                self.virtual_position = self.real2virtual(self.real_position)
                real_record.record(self.real_position.copy())
                virtual_record.record(self.virtual_position.copy())
            i += 1
        return real_record, virtual_record

    def reach(self,target):
        return np.linalg.norm(self.virtual_position - target) < self.threshold

    def real2virtual(self, position):
        return position
    
    def virtual2real(self, position):
        return position