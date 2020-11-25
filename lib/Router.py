class Router:
    def __init__(self, x, y, ass_processor):
        self.x = x
        self.y = y

        self.core = ass_processor
        self.util = 0

    def pushtask_ass_processor(self, task):
        self.core.pushTask(task)