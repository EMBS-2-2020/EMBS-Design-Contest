class Router:
    def __init__(self, x, y, mesh, processor):
        self.x = x
        self.y = y
        self.mesh = mesh

        self.processor = processor
        self.comm_flows = []
        self.util = 0

    def push_task(self, task):
        return self.processor.push_task(task)

    def push_comm_flow(self, comm_flow):
        if self.has_capacity(comm_flow):
            self.util += comm_flow.util
            self.comm_flows.append(comm_flow)
            return True
        else:
            return False

    def has_capacity(self, comm_flow):
        return self.util + comm_flow.util <= 1
