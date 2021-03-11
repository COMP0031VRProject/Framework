import torch
import numpy as np
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
class Edge:
    def __init__(self, length):
        self.length = length
        self.stiffness = 1.0
        self.rest_length = 1.0

class SpringMesh(Mesh):
    def __init__(self, verts, tInd):
        super().__init__(verts, tInd)
        self.edges = {}
        self.update_edges()
    def update_edges(self):
        for t in self.tInd:
            e1 = tuple(sorted([t[0], t[1]]))
            e2 = tuple(sorted([t[1], t[2]]))
            e3 = tuple(sorted([t[0], t[2]]))
            E = [e1, e2, e3]
            for e in E:
                if not e in self.edges.keys():
                    self.edges[e] = Edge(torch.linalg.norm(self.verts[e[0]] - self.verts[e[1]]))
    def connected(self, vIndex):
        ans = {}
        for e in self.edges.keys():
            if vIndex in e:
                k = e[0] if e[0] != vIndex else e[1]
                ans[k] = self.edges[e]
        return ans
    def copy(self):
        return SpringMesh(self.verts, self.tInd.copy())
