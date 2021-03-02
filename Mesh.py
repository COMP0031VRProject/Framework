import json
import numpy as np

class Mesh:
    def __init__(self, verts, tInd):
        self.verts = verts
        self.tInd = tInd

    def copy(self):
        return Mesh(self.verts.copy(), self.tInd.copy())

    def print_data(self):  # dump Mesh data to stdout
        print("------ VERTS ------")
        print(self.verts)
        print("------ tIND ------")
        print(self.tInd)

    def save(self, file):  # save data to specified file
        data = {
            "verts": self.verts,
            "tInd": self.tInd
        }

        with open(file, 'w') as f:
            json.dump(data, f)

    def load(self, file):  # load data to specified file (will overwrite existing data in object)
        with open(file) as f:
            data = json.load(f)
        self.verts = data["verts"]
        self.tInd = data["tInd"]

    def loadNodeAndEle(self, nodeFileName, eleFileName):
        self.verts = []
        with open(nodeFileName) as file:
            line = file.readline().strip()
            while line[0] == '#':
                line = file.readline().strip()
            # first line
            
            for line in file.readlines():
                if line.split()[0] == '#':
                    continue
                words = line.split()
                x = float(words[1])
                y = float(words[2])
                self.verts.append(np.array([x, y]))
        self.tInd = []
        with open(eleFileName) as file:
            line = file.readline().strip()
            while line[0] == '#':
                line = file.readline().strip()
            # first line

            for line in file.readlines():
                if line.split()[0] == '#':
                    continue
                words = line.split()
                self.tInd.append((int(words[1]) - 1, \
                    int(words[2]) - 1, \
                    int(words[3]) - 1))