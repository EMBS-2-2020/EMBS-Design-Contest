from lib.CommFlow import CommFlow
from lib.Task import Task


class Simulation:
    tasks = [
        Task(1, 0.27), Task(2, 0.31), Task(3, 0.22), Task(4, 0.15), Task(5, 0.28), Task(6, 0.11), Task(7, 0.08),
        Task(8, 0.19), Task(9, 0.22), Task(10, 0.06), Task(11, 0.05), Task(12, 0.04), Task(13, 0.03), Task(14, 0.03),
        Task(15, 0.06), Task(16, 0.08), Task(17, 0.66), Task(18, 0.03)
    ]
    # Add the rest of the tasks

    commFlows = [
        CommFlow(1, 0.44, 36, 37)
    ]

    # Add the rest of the commflows

    # alloc_arr is 2d array representing the NoC platform
    # the innermost array contains list of task ids to be run on that processor
    # middle array contains list of processor in x-axis
    # top array contains list of processors in y-axis
    # e.g. [[[1,2,3],[4,5,6]],
    #       [[7,8,9],[10,11,12]]]
    def __init__(self, alloc_arr, factor_fc, factor_fi):
        self.alloc_arr = alloc_arr
        self.factor_fc = factor_fc
        self.factor_fi = factor_fi

    def get_mesh_x(self):
        # No protection here if alloc_arr defined with no rows
        return len(self.alloc_arr[0])

    def get_mesh_y(self):
        # No protection here if alloc_arr defined with no rows
        return len(self.alloc_arr[0])

    def get_cost(self):
        return (self.get_mesh_x * self.get_mesh_y) + self.factor_fc * self.factor_fi