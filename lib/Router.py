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
