class Mesh:
    def __init__(self, verts, tInd):
        self.verts = verts
        self.tInd = tInd
    def copy(self):
        return Mesh(self.verts.copy(), self.tInd.copy())