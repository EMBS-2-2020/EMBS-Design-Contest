class CommFlow:
    def __init__(self, id, util, send_task_id, dest_task_id):
        self.id = id
        self.util = util
        self.send_task_id = send_task_id
        self.dest_task_id = dest_task_id