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
    CommFlow(6, 0.39, 3, 38),
    CommFlow(7, 0.32, 12, 28),
    CommFlow(8, 0.2, 18, 39),
    CommFlow(9, 0.33, 42, 21),
    CommFlow(10, 0.22, 7, 1),
    CommFlow(11, 0.1, 21, 9),
    CommFlow(12, 0.12, 38, 39),
    CommFlow(13, 0.28, 25, 8),
    CommFlow(14, 0.17, 24, 17),
    CommFlow(15, 0.22, 5, 38),
    CommFlow(16, 0.18, 38, 5),
    CommFlow(17, 0.15, 33, 21),
    CommFlow(18, 0.29, 8, 34),
    CommFlow(19, 0.2, 19, 26),
    CommFlow(20, 0.23, 13, 28),
    CommFlow(21, 0.19, 16, 42),
    CommFlow(22, 0.4, 28, 43),
    CommFlow(23, 0.21, 28, 15),
    CommFlow(24, 0.34, 1, 34),
    CommFlow(25, 0.41, 37, 24),
    CommFlow(26, 0.2, 23, 41),
    CommFlow(27, 0.14, 28, 38),
    CommFlow(28, 0.18, 20, 40),
    CommFlow(29, 0.29, 25, 34),
    CommFlow(30, 0.22, 35, 17),
    CommFlow(31, 0.11, 21, 27),
    CommFlow(32, 0.3, 5, 3),
    CommFlow(33, 0.24, 7, 39),
    CommFlow(34, 0.1, 19, 29),
    CommFlow(35, 0.07, 27, 21),
    CommFlow(36, 0.22, 10, 21),
    CommFlow(37, 0.13, 34, 30),
    CommFlow(38, 0.38, 2, 22),
    CommFlow(39, 0.11, 27, 28),
    CommFlow(40, 0.12, 28, 27),
    CommFlow(41, 0.44, 9, 23),
    CommFlow(42, 0.44, 9, 41),
    CommFlow(43, 0.44, 9, 33),
    CommFlow(44, 0.09, 9, 28),
    CommFlow(45, 0.31, 34, 7),
    CommFlow(46, 0.37, 32, 2),
    CommFlow(47, 0.09, 33, 24),
    CommFlow(48, 0.11, 24, 33),
    CommFlow(49, 0.14, 24, 8),
    CommFlow(50, 0.07, 3, 27),
    CommFlow(51, 0.36, 11, 30),
    CommFlow(52, 0.22, 14, 28),
    CommFlow(53, 0.1, 3, 17, 22),
    CommFlow(54, 0.22, 39, 24),
    CommFlow(55, 0.44, 4, 39),
    CommFlow(56, 0.33, 39, 4),
    CommFlow(57, 0.3, 26, 33),
    CommFlow(58, 0.39, 25, 1),
    CommFlow(59, 0.4, 40, 44),
    CommFlow(60, 0.2, 8, 16, 10),
    CommFlow(61, 0.09, 17, 25),
    CommFlow(62, 0.42, 30, 31),
    CommFlow(63, 0.04, 30, 41),
    CommFlow(64, 0.33, 29, 26),
    CommFlow(65, 0.2, 26, 29),
    CommFlow(66, 0.32, 31, 8),
    CommFlow(67, 0.29, 44, 6),
    CommFlow(68, 0.14, 27, 20)
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
        alpha = 1  # Inital cost
        beta = 1  # How well distributed is the work over processors
        zeta = 1  # How much noc util is there

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

        return f1 * alpha + f2 * zeta + f3 * beta

    def modify_util(self):
        for t in self.tasks:
            t.util = t.util / self.factor_fi
        for c in self.comm_flows:
            c.util = c.util / self.factor_fc
