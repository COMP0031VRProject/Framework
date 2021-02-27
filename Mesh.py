import json


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
