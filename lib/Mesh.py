from lib.Proccessor import Proccessor
from lib.Router import Router

class Mesh:
    def __init__(self, meshX, meshY):
        # 2D array of router classes with [y][x] in array form
        self.mesh = []

        for y in range(meshY):
            x_line = []
            for x in range(meshX):
                x_line.append(Router(x,y, Proccessor()))
            self.mesh.append(x_line)

    def get_router(self, x,y): 
        # TODO: Doesn't allow for xy failure
        return self.mesh[y][x]

    def task_onto_proccessor(self, task, x, y):
        self.get_router(x,y).pushtask_ass_processor(task)