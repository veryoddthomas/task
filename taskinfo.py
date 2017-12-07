"""
TaskInfo class to encapsulate data and operations we want want to use
"""

import datetime
import enum
import queue
import uuid

import priority_queue

# pylint: disable=W0511
# FIXME: It's a bit ridiculous that we have to add the above disable just to
#        allow TODOs & FIXMEs


class TasksInProgress(object):
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

    def peek(self):
        """Returns the most recently added item without removing it"""
        return self.stack[-1]

    def empty(self):
        """Returns True if the stack is empty; False otherwise"""
        return len(self.stack) == 0

    def dump(self):
        """Dump the stack"""
        for task in reversed(self.stack):
            print(task)


class TaskBacklog(object):
    """Priority queue for managing a backlog of tasks.  Tasks are moved to and
       from the TasksInProgress stack as they are activated/deactivated."""
    def __init__(self):
        self.queue = priority_queue.PriorityQueue()

    def put(self, task):
        """Insert a task into the backlog"""
        self.queue.put(task, task.priority)

    def get(self):
        """Remove a task from the backlog"""
        item = self.queue.get()
        return item[1]

    def empty(self):
        """Returns True if the queue is empty; False otherwise"""
        return self.queue.empty()

    def peek(self):  # pylint: disable=R0201
        """Look at the next task on the queue without removing it"""
        assert False, "Not implemented due to PriorityQueue limitations"


class TaskLimbo(object):
    """Reference-counted dictionary of sets indexed by blocker. When a stored
       item loses all of its references, the item is removed and the
       registered callback is triggered returning a reference to the item"""
    def __init__(self, callback):
        """Constructor for TaskLimbo class"""
        if not callable(callback):
            raise TypeError("'callback' must be callable")

        self._callback = callback
        self._blocked_items = {}
        self._blockers = {}

    def block(self, item, blocked_by):
        """Stores 'item' internally, indexed by 'blocked_by'"""
        item_meta = self._blocked_items.get(item)
        if item_meta is None:
            item_meta = RefCount(item)
            self._blocked_items[item] = item_meta

        blocked_items = self._blockers.get(blocked_by, set())
        if item_meta in blocked_items:
            raise ValueError("'{}' is already blocked by '{}'".format(
                str(item_meta.data), str(blocked_by)))

        blocked_items.add(item_meta)
        self._blockers[blocked_by] = blocked_items
        item_meta.add_ref()

    def unblock(self, completed_item):
        """Unblock all items blocked by 'completed_item'"""
        blocked_items = self._blockers.get(completed_item, set())
        for item_meta in blocked_items:
            item_meta.remove_ref()
            if item_meta.refcount == 0:
                self._callback(item_meta.data)
                del self._blocked_items[item_meta.data]

        del self._blockers[completed_item]


class TaskDorm(object):
    """Stores sleeping Tasks in the order that they will wake up. Items
       can be woken/fetched by id, but it may be inefficient"""
    def __init__(self, callback):
        """Constructor for TaskDorm class"""
        if not callable(callback):
            raise TypeError("'callback' must be callable")

        self._callback = callback
        self._queue = priority_queue.PriorityQueue()

    def sleep(self, item, duration):
        """Put 'item' to sleep for datetime.timedelta 'duration'"""
        if not isinstance(duration, datetime.timedelta):
            raise TypeError(
                "timestamp must be a timedelta object (given '{}')"
                .format(str(type(duration))))

        wake_at = datetime.datetime.now() + duration
        self.wake_at(item, wake_at)

    def wake_at(self, item, timestamp):
        """Put 'item' to sleep until 'timestamp'"""
        if not isinstance(timestamp, datetime.datetime):
            raise TypeError(
                "timestamp must be a datetime object (given '{}')"
                .format(str(type(timestamp))))

        self._queue.put(item, timestamp)

    def wake(self, item_id):  # pylint: disable=R0201,W0613
        """Immediately wake the item with id 'item_id'"""
        assert False, "Not implemented due to PriorityQueue limitations"""

    # NOTE: Due to how iteration & our stack work, if multiple items are
    #       woken at the same time, they will be placed on the stack in a
    #       rather 'backwards' manner, where the task set to wake most urgently
    #       is actually blocked by tasks set to wake afterwards. This is
    #       currently a design limitation and should be addressed as needed.
    def reveille(self):
        """Wake up all items that are ready to wake"""
        now = datetime.datetime.now()
        # TODO: this logic can be optimized if our queue has a peek() method
        while self._queue.size() > 0:
            item = self._queue.get_tuple()
            if item[1] <= now:
                self._callback(item[0])
            else:
                # put the item back & terminate iteration
                self._queue.put(item[0], item[1])
                break


class TaskMaster(object):
    """Contains all scopes/structures used by the task tool & controls
       movements between them:
       * TasksInProgress (current context stack)
       * TaskBacklog (backlog priority queue)
       * TaskLimbo (blocked items in a ref-counted dictionary)
       * TaskDorm (sleeping items in a sorted list)
       * Graveyard (closed issues in a simple list)
    """
    def __init__(self):
        self.stack = TasksInProgress()
        self.backlog = TaskBacklog()
        self.blocked = TaskLimbo(callback=self.stack.push)
        self.sleeping = TaskDorm(callback=self.stack.push)
        self.graveyard = []

    def active_item(self, remove=True):
        """Returns the active item"""
        self.sleeping.reveille()  # wake items whose sleep timer has expired
        if not self.stack.empty():
            pass
        elif not self.backlog.empty():
            # feed the stack the top priority item from the queue
            self.stack.push(self.backlog.get())
        else:  # both the stack & queue are empty
            raise queue.Empty

        assert not self.stack.empty(), "BUG: empty stack"

        if remove:
            return self.stack.pop()

        return self.stack.peek()

    def add(self, item):
        """Places the given item on top of the stack"""
        self.sleeping.reveille()  # wake items whose sleep timer has expired
        self.stack.push(item)

    # Calling self.active_item() could potentially wake items that we are not
    # expecting and cause unexpected behavior. Most methods (move, sleep, etc)
    # should only affect the currently observable item; this requires direct
    # stack manipulation.
    # TODO - determine what exception should be raised if the current stack is
    #        empty. Getting the active item could repopulate the stack, but
    #        that is generally not user-expected behavior.
    def move(self):
        """Move the active item on the stack to the backlog"""
        active_item = self.stack.pop()
        self.backlog.put(active_item)

    def sleep(self, duration):
        """Puts the active item to sleep for timedelta 'duration'"""
        active_item = self.stack.pop()
        self.sleeping.sleep(active_item, duration)

    def wake_at(self, timestamp):
        """Puts the active item to sleep until datetime 'timestamp'"""
        active_item = self.stack.pop()
        self.sleeping.wake_at(active_item, timestamp)

    def close(self):
        """Closes out the active item"""
        active_item = self.stack.pop()
        self.graveyard.append(active_item)


class TaskPriority(enum.Enum):
    """Task Priorities"""
    SHOWSTOPPER = 0  # [tbd] Stuck to front of queue, top of stack?
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskInfo(object):
    """Stores all information about a task"""
    def __init__(self, description, task_type, priority=None):
        if priority is None:
            priority = TaskPriority.MEDIUM

        self.id = uuid.uuid4()
        self.description = description
        self.type = task_type
        self.priority = None

        self.set_priority(priority)

    def set_priority(self, priority):
        """Set task priority"""
        if not isinstance(priority, TaskPriority):
            raise TypeError("Invalid priority '{}' of type '{}'".format(
                str(priority), str(type(priority))))

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


class RefCount(object):
    """Reference counter wrapper for an object"""
    def __init__(self, data, count=0):
        self.data = data
        self._refcount = count

    # equivalance is useful on its own but is also required for hash support
    def __eq__(self, other):
        """equivalence override"""
        if isinstance(other, RefCount):
            return self.data == other.data

        return self.data == other

    def add_ref(self):
        """Add a reference"""
        self._refcount += 1

    def remove_ref(self):
        """Remove a reference"""
        self._refcount -= 1
        assert self._refcount >= 0, "BUG: negative refcount"

    @property
    def refcount(self):
        """Property accessor for active reference count"""
        return self._refcount
