from lib.Mesh import Mesh
from lib.CommFlow import CommFlow
from lib.Task import Task
import numpy as np
import copy

# Consts
btasks = [
    Task(1, 0.27),
    Task(2, 0.31),
    Task(3, 0.22),
    Task(4, 0.15),
    Task(5, 0.28),
    Task(6, 0.11),
    Task(7, 0.08),
    Task(8, 0.19),
    Task(9, 0.22),
    Task(10, 0.06),
    Task(11, 0.05),
    Task(12, 0.04),
    Task(13, 0.03),
    Task(14, 0.03),
    Task(15, 0.06),
    Task(16, 0.08),
    Task(17, 0.66),
    Task(18, 0.03),
    Task(19, 0.09),
    Task(20, 0.14),
    Task(21, 0.55),
    Task(22, 0.34),
    Task(23, 0.07),
    Task(24, 0.48),
    Task(25, 0.22),
    Task(26, 0.2),
    Task(27, 0.33),
    Task(28, 0.48),
    Task(29, 0.1),
    Task(30, 0.34),
    Task(31, 0.16),
    Task(32, 0.09),
    Task(33, 0.35),
    Task(34, 0.17),
    Task(35, 0.08),
    Task(36, 0.12),
    Task(37, 0.14),
    Task(38, 0.23),
    Task(39, 0.55),
    Task(40, 0.03),
    Task(41, 0.45),
    Task(42, 0.04),
    Task(43, 0.09),
    Task(44, 0.12)
]

# TODO: Add the rest of the commflows
bcomm_flows = [
    CommFlow(1, 0.44, 36, 37),
    CommFlow(2, 0.41, 2, 32),
    CommFlow(3, 0.17, 22, 25),
    CommFlow(4, 0.21, 32, 24),
    CommFlow(5, 0.31, 17, 35),
    CommFlow(6, 0.39, 3, 38)
]


class Simulation:

    def __init__(self, meshX, meshY, factor_fc, factor_fi, mapping):
        self.factor_fc = factor_fc
        self.factor_fi = factor_fi
        self.meshX = meshX
        self.meshY = meshY

        self.tasks = copy.deepcopy(btasks)
        self.comm_flows = copy.deepcopy(bcomm_flows)

        self.modify_util()

        # 2D array of router classes with [y][x] in array form
        self.mesh = Mesh(self, meshX, meshY, self.tasks, self.comm_flows, mapping)
        self.mesh.run_mesh()

    def get_cost_mark(self):
        return (self.meshX * self.meshY) + self.factor_fc * self.factor_fi

    def get_fitness(self):
        # Need to make a better fitness function
        alpha = 1 # Inital cost
        beta = 1 # How well distributed is the work over processors
        zeta = 1 # How much noc util is there

        # Inital cost
        f1 = (self.meshX * self.meshY) + self.factor_fc * self.factor_fi

        # How much noc util is there
        f2 = 0

        for i in self.mesh.mesh:
            for rout in i:
                f2 += sum(rout.util)
                f2 += rout.processor.commflow_util

        # How well distributed is the work over processors
        proc_util = []

        for i in self.mesh.mesh:
            for rout in i:
                proc_util.append(rout.processor.util)

        f3 = np.var(proc_util)

        return f1*alpha + f2*zeta + f3*beta

    def modify_util(self):
        for t in self.tasks:
            t.util = t.util / self.factor_fi
        for c in self.comm_flows:
            c.util = c.util / self.factor_fc
