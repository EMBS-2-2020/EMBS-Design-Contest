class Proccessor:
    def __init__(self):
        self.ass_tasks = []
        self.util = 0

    def pushTask(self, task):
        self.ass_tasks.append(task)
        self.util += task.util