"""
TaskInfo class to encapsulate data and operations we want want to use
"""

import uuid
import enum


class TaskPriority(enum.Enum):
    """Task Priorities"""
    SHOWSTOPPER = 0  # [tbd] Stuck to front of queue, top of stack?
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskInfo:
    """Stores all information about a task"""
    def __init__(self, description, task_type):
        self.id = uuid.uuid4()
        self.description = description
        self.type = task_type
        self.priority = TaskPriority.MEDIUM

    def set_priority(self):  # pylint: disable=no-self-use
        """Load task from persistent storage"""
        # TBD
        return

    def store(self):  # pylint: disable=no-self-use
        """Store task to persistent storage"""
        # TBD
        return
