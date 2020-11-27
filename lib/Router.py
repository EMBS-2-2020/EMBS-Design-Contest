class Router:
    def __init__(self, x, y, mesh, processor):
        self.x = x
        self.y = y
        self.mesh = mesh

        self.processor = processor
        self.comm_flows = []
        self.util = [0]*5

    def recieve_flow(self, flow):
        temp = self.mesh.get_router_of_task(flow.dest_task_id).x
        temp2 = self.mesh.get_router_of_task(flow.dest_task_id).y

        if self.x > temp:
            self.mesh.get_router(self.x-1, self.y).recieve_flow(flow)
            self.push_comm_flow(flow, 0)
        elif self.x < temp:
            self.mesh.get_router(self.x+1, self.y).recieve_flow(flow)
            self.push_comm_flow(flow, 1)
        elif self.y > temp2:
            self.mesh.get_router(self.x, self.y-1).recieve_flow(flow)
            self.push_comm_flow(flow, 2)
        elif self.y < temp2:
            self.mesh.get_router(self.x, self.y+1).recieve_flow(flow)
            self.push_comm_flow(flow, 3)
        else:
            self.push_comm_flow(flow, 4)

    def push_task(self, task):
        return self.processor.push_task(task)

    def push_comm_flow(self, comm_flow, direction):
        if self.has_capacity(comm_flow, direction):
            self.util[direction] += comm_flow.util
            return True
        else:
            print('Router {},{},{}'.format(comm_flow.util, direction, self.util))
            raise Exception("Capacity is overflowed on router {},{}".format(self.x,self.y))

    def has_capacity(self, comm_flow, direction):
        return self.util[direction] + comm_flow.util <= 1
