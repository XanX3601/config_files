import git

class CloneProgress(git.remote.RemoteProgress):
    """Used to update a repo clone task progress from a ``rich`` ``Progress``."""
    def __init__(self, progress, task_id):
        super().__init__()
        self.progress = progress
        self.task_id = task_id
        self.started = False

    def update(self, op_code, cur_count, max_count=None, message=''):
        if not self.started and max_count is not None:
            self.started = True
            self.progress.start_task(self.task_id)

        if self.started:
            self.progress.update(self.task_id, total=max_count, completed=cur_count)

