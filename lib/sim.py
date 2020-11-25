from lib.Mesh import Mesh
from lib.CommFlow import CommFlow
from lib.Task import Task

# Consts
tasks = [
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
commFlows = [
    CommFlow(1, 0.44, 36, 37),
    CommFlow(2, 0.41, 2, 32),
    CommFlow(3, 0.17, 22, 25),
    CommFlow(4, 0.21, 32, 24),
    CommFlow(5, 0.31, 17, 35),
    CommFlow(6, 0.39, 3, 38)
]

def get_task(id):
    for i in tasks:
        if i.id == id:
            return i
    return False

def get_commflow_start(id):
    flows = []

    for i in commFlows:
        if i.send_task == id:
            flows.append(i)

    return flows


class Simulation:

    def __init__(self, meshX, meshY, factor_fc, factor_fi):
        self.factor_fc = factor_fc
        self.factor_fi = factor_fi

        # 2D array of router classes with [y][x] in array form
        self.mesh = Mesh(meshX, meshY)


    def run_map(self, mapping):

        # Put tasks to proccessors, this also adds util to the proccesor
        # TODO: Adjust based off factor value
        for id, x,y in mapping:
            self.mesh.task_onto_proccessor(get_task(id), x,y)

        # Now calc util for each router flow
        # TODO: Adjust based off factor value

        # For all tasks
        for id, x,y in mapping:

            # Search for all flows that start with this task
            flows = get_commflow_start(id)

            # Check mapping to see if dest is in the same proccessor
            noc_flows = []
            for i in flows:

                for did, dx, dy in mapping:
                    if did == i.dest_task and (x!=dx or y!=dy):
                        noc_flows.append(i)

            print(noc_flows)
            # TODO: Now create a way to start those comm flows through the network

            


    def get_cost_mark(self):
        return (self.get_mesh_x * self.get_mesh_y) + self.factor_fc * self.factor_fi