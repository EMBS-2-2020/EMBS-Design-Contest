class Processor:
    def __init__(self, mesh):
        self.ass_tasks = []
        self.util = 0
        self.mesh = mesh
        self.commflow_util = 0

    def push_task(self, task):
        if self.has_capacity(task):
            self.ass_tasks.append(task)
            self.util += task.util
            return True
        else:
            return False

    def has_capacity(self, task):
        return self.util + task.util <= 1

    def has_task(self, id):
        for task in self.ass_tasks:
            if id == task.id:
                return True
        return False


    def has_comm_capacity(self, flow):
        return self.commflow_util + flow.util <= 1

    def create_flow(self, flow, router):
        if self.has_comm_capacity(flow):
            self.commflow_util += flow.util
            router.recieve_flow(flow)
        else:
            raise Exception("Flow overflow on processor to noc")
    
