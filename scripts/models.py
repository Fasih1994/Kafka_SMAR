"""
Model classes
"""

class PendingTask:
    def __init__(self, msg, task, tries) -> None:
        self.msg = msg
        self.task = task
        self. tries = tries

    def tried(self):
        self.tries -= 1
        if self.tries < 0:
            self.tries = 14

    def __repr__(self) -> str:
        return self.msg