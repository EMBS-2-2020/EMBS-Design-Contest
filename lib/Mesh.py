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

    def get_router_of_task(self, id):
        for tsk, x, y in self.mapping:
            if tsk == id:
                return self.mesh[y][x]
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
        # print("Mapping length {}".format(len(mapping)))
        for id, x, y in mapping:
            router = self.get_router(x, y)
            router.push_task(self.get_task(id))

    def populate_routes(self):
        for comm_flow in self.comm_flows:
            # print("Searching for start task {}".format(comm_flow.send_task_id))
            has_routed = False
            for y in range(len(self.mesh)):
                for x in range(len(self.mesh[0])):
                    router = self.get_router(x, y)
                    # print("Tasks for processor {},{}: {}".format(router.x, router.y, router.processor.ass_tasks))
                    if router.processor.has_task(comm_flow.send_task_id):
                        # do routing
                        has_routed = True

                        dest_router = self.get_router_of_task(comm_flow.dest_task_id)
                        if not (dest_router.x == router.x and dest_router.y == router.y):
                            router.processor.create_flow(comm_flow, router)
                        # otherwise do nothing - dest task and sender task are on same processor
                    if has_routed:
                        break
                if has_routed:
                    break

            if not has_routed:
                raise Exception("CommFlow {} not routed! Start task not found on any processor".format(comm_flow.id))

