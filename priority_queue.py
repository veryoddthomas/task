"""Iterable concurrent PriorityQueue implementation"""
# pylint: disable=W0511
# FIXME: It's a bit ridiculous that we have to add the above disable just to
#        allow TODOs & FIXMEs
# TODO - currently a VERY dumb, coarse-grained locking implementation

import threading

from queue import Empty


class IterQueue(object):
    """Simple iterable queue. Already thread-safe by nature of Python lists."""
    def __init__(self, items=None):
        """Constructor for simple queue object"""
        if items is None:
            items = []

        self._items = list(items)

    def __len__(self):
        """len() operator override"""
        return len(self._items)

    def __iter__(self):
        """Iterator for queue object"""
        for item in self._items:
            yield item

    def get(self):
        """Remove an item from the queue"""
        return self._items.pop(0)

    def peek(self):
        """Look at the top item in the queue"""
        return self._items[0]

    def put(self, item):
        """Add 'item' to the queue"""
        self._items.append(item)

    def size(self):
        """Returns the number of items in the queue"""
        return len(self._items)

    def empty(self):
        """Returns True if the Queue contains 0 items, false otherwise"""
        return self.size() == 0


class PriorityQueue(object):
    """Simple concurrent priority queue. Follows the Unix priority model."""
    DEFAULT_PRIORITY = 0

    def __init__(self):
        self._levels = []
        self._lock = threading.Lock()
        self._queues = {}

    def __iter__(self):
        """Object iterator"""
        for level in self._levels:
            for item in self._queues[level]:
                yield item

    def put(self, item, priority=None):
        """Add an item to the priority queue"""
        if priority is None:
            priority = PriorityQueue.DEFAULT_PRIORITY

        self._lock.acquire()
        try:
            queue = self._queues.get(priority)
            if queue is None:
                queue = IterQueue()
                self._queues[priority] = queue
                self._levels.append(priority)
                self._levels.sort()

            queue.put(item)
            self._queues[priority] = queue
        finally:
            self._lock.release()

    def get(self):
        """Removes & returns the highest priority item"""
        ret = self.get_tuple()
        return ret[0]

    def get_tuple(self):
        """Removes & returns a tuple of (value, priority)"""
        self._lock.acquire()
        try:
            if not self._levels:
                raise Empty

            level = self._levels[0]
            queue = self._queues[level]
            ret = queue.get()
            if queue.empty():
                del self._queues[level]
                self._levels.pop(0)

            return ret, level
        finally:
            self._lock.release()

    def peek(self):
        """Returns the highest priority item without removing it"""
        ret = self.peek_tuple()
        return ret[0]

    def peek_tuple(self):
        """Returns a tuple of (value, priority) without removing it"""
        self._lock.acquire()
        try:
            if not self._levels:
                raise Empty

            return self._queues[self._levels[0]].peek()
        finally:
            self._lock.release()

    def size(self):
        """Returns the total number of items in the queue"""
        self._lock.acquire()
        try:
            # sum([]) returns 0 in Python; the below expression is always safe
            return sum([len(queue) for queue in self._queues.values()])
        finally:
            self._lock.release()

    def empty(self):
        """Returns True if there are 0 items in the queue; False otherwise"""
        return self.size() == 0
