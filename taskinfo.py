"""
TaskInfo class to encapsulate data and operations we want want to use
"""

import uuid
import enum

from queue import PriorityQueue


class TasksInProgress:
    """LIFO stack for capturing tasks as they come in.  This structure is used
       for storing interrupt items until they can be moved to the Backlog"""
    def __init__(self):
        self.stack = list()

    def push(self, task):
        """Push a task onto the stack"""
        self.stack.append(task)

    def pop(self):
        """Pop a task from the stack"""
        return self.stack.pop()

    def dump(self):
        """Dump the stack"""
        for task in reversed(self.stack):
            print(task)


class TaskBacklog:
    """Priority queue for managing a backlog of tasks.  Tasks are moved to and
       from the TasksInProgress stack as they are activated/deactivated."""
    def __init__(self):
        self.queue = PriorityQueue()

    def put(self, task):
        """Insert a task into the backlog"""
        self.queue.put(task.priority, task)

    def get(self):
        """Remove a task from the backlog"""
        return self.queue.get()


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

    def set_priority(self, priority):
        """Set task priority"""
        assert(priority in TaskPriority)
        self.priority = priority
        return

    def do_nothing(self):
        """TBD"""
        return self

    def __str__(self):
        retval = """
id: {}
description: {}
type: {}
priority: {}""".format(self.id, self.description, self.type, self.priority)
        return retval
