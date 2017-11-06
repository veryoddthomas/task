"""
TaskInfo class to encapsulate data and operations we want want to use
"""

import uuid

DEFAULT_TASK_PRIORITY = 3


class TaskInfo:
    """Stores all information about a task"""
    def __init__(self, description, task_type):
        self.id = uuid.uuid4()
        self.description = description
        self.type = task_type
        self.priority = DEFAULT_TASK_PRIORITY

    def set_priority(self):  # pylint: disable=no-self-use
        """Load task from persistent storage"""
        # TBD
        return

    def store(self):  # pylint: disable=no-self-use
        """Store task to persistent storage"""
        # TBD
        return
