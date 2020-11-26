class Processor:
    def __init__(self, mesh):
        self.ass_tasks = []
        self.util = 0
        self.mesh = mesh

    def push_task(self, task):
        if self.has_capacity(task):
            self.ass_tasks.append(task)
            self.util += task.util
            return True
        else:
            return False

    def has_capacity(self, task):
        return self.util + task.util <= 1

    def has_remaining_task(self):
        return len(self.ass_tasks) > 1

    def has_task(self, id):
        for task in self.ass_tasks:
            if id == task.id:
                return True
        return False
