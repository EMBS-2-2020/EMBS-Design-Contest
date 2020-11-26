from lib.Processor import Processor
from lib.Router import Router


class Mesh:
    def __init__(self, sim, meshX, meshY, tasks, comm_flows, mapping):
        # 2D array of router classes with [y][x] in array form
        self.mesh = []
        self.tasks = tasks
        self.comm_flows = comm_flows
        self.sim = sim

        for y in range(meshY):
            x_line = []
            for x in range(meshX):
                x_line.append(Router(x, y, self, Processor(self)))
            self.mesh.append(x_line)
        self.run_map(mapping)
        self.populate_routes()

    def get_router(self, x, y):
        # TODO: Doesn't allow for xy failure
        return self.mesh[y][x]

    def get_task(self, t_id):
        for i in self.tasks:
            if i.id == t_id:
                return i
        return False

    def get_comm_flow_by_send_id(self, id):
        flows = []

        for i in self.comm_flows:
            if i.send_task == id:
                flows.append(i)

        return flows

    def run_map(self, mapping):
        # Put tasks to processors, this also adds util to the processor
        # TODO: Adjust based off factor value
        for id, x, y in mapping:
            router = self.get_router(x,y)
            if not router.push_task(self.get_task(id)):
                raise Exception("SIMULATION FAILED - PROCESSOR UTIL EXCEEDED")

    def populate_routes(self):
        for y in len(self.mesh):
            for x in len(self.mesh[0]):
                router = self.get_router(x,y)
                for comm_flow in self.comm_flows:
                    has_routed = False
                    if router.processor.has_task(comm_flow.send_task):
                         # do routing
                        has_routed = True
                        dest_router = None
                        for y1 in len(self.mesh):
                             for x1 in len(self.mesh[0]):
                                 i_router = self.get_router(x1,y1)
                        if dest_router is None:
                            raise Exception("Destination task not found on any processor!")
                    if not has_routed:
                        raise Exception("CommFlow not routed! Start task not found on any processor")