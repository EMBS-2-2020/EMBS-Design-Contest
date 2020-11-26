from lib.Processor import Processor
from lib.Router import Router


class Mesh:
    def __init__(self, sim, meshX, meshY, tasks, comm_flows, mapping):
        # 2D array of router classes with [y][x] in array form
        self.mesh = []
        self.tasks = tasks
        self.comm_flows = comm_flows
        self.sim = sim
        self.mapping = mapping

        for y in range(meshY):
            x_line = []
            for x in range(meshX):
                x_line.append(Router(x, y, self, Processor(self)))
            self.mesh.append(x_line)

    def run_mesh(self):
        self.run_map(self.mapping)
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
        print("Mapping length {}".format(len(mapping)))
        for id, x, y in mapping:
            router = self.get_router(x, y)
            if not router.push_task(self.get_task(id)):
                raise Exception("SIMULATION FAILED - PROCESSOR UTIL EXCEEDED")

    def populate_routes(self):
        #print(self.mesh)

        for comm_flow in self.comm_flows:
            print("Searching for start task {}".format(comm_flow.send_task_id))
            has_routed = False
            for y in range(len(self.mesh)):
                for x in range(len(self.mesh[0])):
                    router = self.get_router(x, y)
                    print("Tasks for processor {},{}: {}".format(router.x, router.y, router.processor.ass_tasks))
                    if router.processor.has_task(comm_flow.send_task_id):
                        # do routing
                        has_routed = True
                        dest_router = None
                        for y1 in range(len(self.mesh)):
                            for x1 in range(len(self.mesh[0])):
                                print("Searching for dest task {}".format(comm_flow.dest_task_id))
                                i_router = self.get_router(x1, y1)
                                if i_router.processor.has_task(comm_flow.dest_task_id):
                                    dest_router = i_router
                        if dest_router is None:
                            raise Exception("Destination task not found on any processor!")
                        self.do_route(router, dest_router, comm_flow)
            if not has_routed:
                raise Exception("CommFlow {} not routed! Start task not found on any processor".format(comm_flow.id))

    def do_route(self, r1, r2, comm_flow):
        if not r1.push_comm_flow(comm_flow):
            raise Exception("SIMULATION FAILED - ROUTER UTIL EXCEEDED")
        # do x alignment
        print("Origin: {},{}. Dest: {},{}".format(r1.x, r1.y, r2.x, r2.y))
        if not r1.x == r2.x:
            for i in range(r1.x, r2.x):
                new_x = r1.x + i
                print("Moving in X to router {}, {}".format(new_x, r1.y))
                router = self.get_router(new_x, r1.y)
                if not router.push_comm_flow(comm_flow):
                    raise Exception("SIMULATION FAILED - ROUTER UTIL EXCEEDED")
        # do y alignment
        if not r1.y == r2.y:
            for i in range(r1.y, r2.y):
                new_y = r1.y + i
                print("Moving in Y to router {}, {}".format(r2.x, new_y))
                router = self.get_router(r2.x, new_y)
                if not router.push_comm_flow(comm_flow):
                    raise Exception("SIMULATION FAILED - ROUTER UTIL EXCEEDED")
