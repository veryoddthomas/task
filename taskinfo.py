"""
TaskInfo class to encapsulate data and operations we want want to use
"""

# system imports
import abc
import datetime
# import enum  # FIXME
import json
import os
import platform
import queue
import tempfile
import uuid

# local imports
import gitrepo
import priority_queue

# FIXME - hardcoded structure files (no versioncontrol)
DEFAULT_STACK = os.path.join(gitrepo.DEFAULT_REPOSITORY_PATH, "stack.json")
DEFAULT_QUEUE = os.path.join(gitrepo.DEFAULT_REPOSITORY_PATH, "queue.json")
DEFAULT_LIMBO = os.path.join(gitrepo.DEFAULT_REPOSITORY_PATH, "limbo.json")
DEFAULT_DORM = os.path.join(gitrepo.DEFAULT_REPOSITORY_PATH, "dorm.json")


class TaskSyntaxError(ValueError):
    """Represents a user syntax error when authoring a task spec"""
    pass


class ISerializable(object):
    """Base class representing a (JSON) serializable object"""
    __metaclass__ = abc.ABCMeta

    @classmethod
    def format(cls):
        """Returns the serialization format"""
        return "json"

    @staticmethod
    def pretty(data, sort=True, indent=4):
        """Dumps arbitrary data as pretty-printed JSON"""
        return json.dumps(data, sort_keys=sort, indent=indent,
                          separators=(',', ': '))

    @abc.abstractmethod
    def serialize(self, to_file=None):
        """Saves the class to 'to_file' of format self.format"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def load(cls, from_file):
        """Loads the contents of 'from_file' into a valid class instance"""
        raise NotImplementedError


class TasksInProgress(ISerializable):
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

    def find(self, task_id):
        """Searches for a task by 'task_id'. Uses prefix-matching."""
        for task_obj in self.stack:
            if task_obj.id.startswith(task_id):
                return task_obj

        raise LookupError("No such task in stack: '{}'".format(task_id))

    def serialize(self, to_file=None):
        """Saves the stack to 'to_file'"""
        assert to_file is not None  # FIXME
        task_list = [task.id for task in self.stack]
        with open(to_file, "w") as outfile:
            outfile.write(json.dumps(task_list, sort_keys=True, indent=4,
                                     separators=(',', ': ')))

    @classmethod
    def load(cls, from_file):
        """Loads a stack from 'from_file'"""
        with open(from_file) as infile:
            task_list = json.loads(infile.read())

        stack = cls()
        for task_id in task_list:
            stack.push(TaskInfo.from_id(task_id))

        return stack


class TaskBacklog(ISerializable):
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

    def find(self, task_id):
        """Searches for a task by 'task_id'. Uses prefix-matching."""
        for task_obj in self.queue:
            if task_obj.id.startswith(task_id):
                return task_obj

        raise LookupError("No such task in queue: '{}'".format(task_id))

    def serialize(self, to_file=None):
        """Saves the queue to 'to_file'"""
        assert to_file is not None  # FIXME
        task_list = [task.id for task in self.queue]
        with open(to_file, "w") as outfile:
            outfile.write(self.pretty(task_list))

    @classmethod
    def load(cls, from_file):
        """Loads a queue from 'from_file'"""
        with open(from_file) as infile:
            task_list = json.loads(infile.read())

        queue_obj = cls()
        for task_id in task_list:
            queue_obj.put(TaskInfo.from_id(task_id))

        return queue_obj


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

    def find(self, task_id):
        """Searches for a task by 'task_id'. Uses prefix-matching."""
        for task_obj in self._blocked_items:
            if task_obj.id.startswith(task_id):
                return task_obj

        raise LookupError("No such task in limbo: '{}'".format(task_id))


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

    def find(self, task_id):
        """Searches for a task by 'task_id'. Uses prefix-matching."""
        for task_obj in self._queue:
            if task_obj.id.startswith(task_id):
                return task_obj

        raise LookupError("No such task in dorm: '{}'".format(task_id))


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
        """TaskMaster constructor"""
        self.backlog = None
        self.blocked = None
        self.graveyard = []  # TODO - just load from file; not memory
        self.sleeping = None
        self.stack = None
        self._load()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._save()

    def _load(self):
        """Load structure from file"""
        if os.path.exists(DEFAULT_STACK):
            self.stack = TasksInProgress.load(DEFAULT_STACK)
        else:
            self.stack = TasksInProgress()

        if os.path.exists(DEFAULT_QUEUE):
            self.backlog = TaskBacklog.load(DEFAULT_QUEUE)
        else:
            self.backlog = TaskBacklog()

        self.blocked = TaskLimbo(callback=self.stack.push)
        # FIXME: implement serialization for TaskLimbo
        # if os.path.exists(DEFAULT_LIMBO):
        #     self.blocked.load(DEFAULT_LIMBO)

        self.sleeping = TaskDorm(callback=self.stack.push)
        # FIXME: implement serialization for TaskDorm
        # if os.path.exists(DEFAULT_DORM):
        #     self.sleeping.load(DEFAULT_DORM)

    def _save(self):
        """Save structures to file"""
        self.stack.serialize(DEFAULT_STACK)
        self.backlog.serialize(DEFAULT_QUEUE)
        # self.blocked.serialize(DEFAULT_LIMBO)
        # self.sleeping.serialize(DEFAULT_DORM)

    def find(self, task_id):
        """Searches for a task by 'task_id'. Uses prefix-matching."""
        _structs = [
            self.stack,
            self.backlog,
            self.blocked,
            self.sleeping,
        ]
        for struct in _structs:
            try:
                task_obj = struct.find(task_id)
                return task_obj
            except LookupError:
                # not found; try next structure
                continue

        # the graveyard is just a list; search it
        for task_obj in self.graveyard:
            if task_obj.id.startswith(task_id):
                return task_obj

        raise LookupError("No such task: '{}'".format(task_id))

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

    @property
    def current_task(self):
        """Returns the current task without removing it from the stack"""
        try:
            return self.active_item(remove=False)
        except queue.Empty:
            return None


# FIXME - figure out proper conversions/serialization for python3 Enum
# class TaskPriority(enum.Enum):
class TaskPriority:  # pylint: disable=too-few-public-methods
    """Task Priorities"""
    SHOWSTOPPER = 0  # [tbd] Stuck to front of queue, top of stack?
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskInfo(ISerializable):
    """Stores all information about a task"""
    _READ_ONLY_FIELDS = [
        "id",
    ]

    def __init__(self, description, task_type, **kwargs):
        self.id = uuid.uuid4().hex
        self.description = description
        self.type = task_type
        self.priority = None
        self._unknown_args = None

        self._load_dict(kwargs)

    def _load_dict(self, kwargs):
        """Loads keyword arguments from 'kwargs' dictionary"""
        # TaskInfo always needs a description and task_type, but all other
        # supported (optional) parameters are loaded from kwargs to
        keyword_args = dict(kwargs)
        task_id = TaskInfo._dpop(keyword_args, "id")
        if task_id is not None:
            self.id = task_id

        priority = TaskInfo._dpop(keyword_args, "priority")
        if priority is None:
            priority = TaskPriority.MEDIUM
        else:
            priority = int(priority)

        description = TaskInfo._dpop(keyword_args, "description")
        if description is not None:
            self.description = description

        task_type = TaskInfo._dpop(keyword_args, "type")
        if task_type is not None:
            self.type = task_type

        # store unknown args so that they are not lost across
        # serialization/deserialization
        self._unknown_args = keyword_args

        self.set_priority(priority)

    @staticmethod
    def _dpop(dictionary, key, default=None):
        """Removes & returns the value of 'key' from dictionary"""
        try:
            ret = dictionary[key]
            del dictionary[key]
        except KeyError:
            ret = default

        return ret

    def set_priority(self, priority):
        """Set task priority"""
        # FIXME - workaround for Enum issues
        # if not isinstance(priority, TaskPriority):
        if not isinstance(priority, int):
            raise TypeError("Invalid priority '{}' of type '{}'".format(
                str(priority), str(type(priority))))

        self.priority = priority

    def do_nothing(self):
        """TBD"""
        return self

    def __str__(self):
        _str_keys = [
            "id",
            "description",
            "task_type",
            "priority",
        ]

        temp_dict = self.dict()
        filtered_dict = {key: temp_dict[key] for key in _str_keys}
        return self.pretty(filtered_dict)

    def dict(self):
        """Converts TaskInfo object to a dictionary"""
        retval = {
            "id": self.id,
            "description": self.description,
            "task_type": self.type,
            "priority": self.priority,
        }

        retval.update(self._unknown_args)

        return retval

    def edit(self):
        """Opens up an editor and allows the user to update the task directly.
        """
        template = TaskInfo._generate_template(self.dict())
        tempf = tempfile.mkstemp()[1]
        try:
            with open(tempf, 'w') as outfile:
                outfile.write(template)

            editor_cmd = [
                TaskInfo._select_editor(),
                tempf,
            ]
            os.system(" ".join(editor_cmd))

            # validate edited file
            while True:
                try:
                    self._file_update(tempf)
                    break
                except TaskSyntaxError as e:
                    input(
                        # pylint: disable=line-too-long
                        "Task syntax error (enter returns to editor): {}".format(  # nopep8
                            str(e)))
                    os.system(" ".join(editor_cmd))
                    continue
        finally:
            if os.path.exists(tempf):
                os.remove(tempf)

        # commit changes
        self.serialize()

    @staticmethod
    def _generate_template(dictionary):
        """Generates a template for user file-editing"""
        task_dict = dict(dictionary)
        lines = []
        for key in sorted(TaskInfo._READ_ONLY_FIELDS):
            if key not in task_dict:
                continue

            value = TaskInfo._dpop(task_dict, key)
            lines.extend([
                "# {}:".format(key),
                "# {}".format("\n#".join(value.splitlines())),
                "",
            ])

        for key in sorted(task_dict.keys()):
            lines.extend([
                "{}:".format(key),
                str(task_dict[key]),
                "",
            ])

        return "\n".join(lines)

    def _file_update(self, filename):
        """Updates task object data based on the user values in 'filename'"""
        values = TaskInfo._parse_file(filename)
        self._load_dict(values)

    @staticmethod
    def _parse_file(filename):
        """Parses & returns a map of task field values from a user-authored
           file"""
        with open(filename) as infile:
            data = infile.read()

        values = {}
        blank_line = True  # beginning of file always counts as a blank line
        field_name = None
        cur_field = []
        for line in data.splitlines():
            if line.startswith("#"):
                continue  # skip comments

            if not line:
                blank_line = True
                cur_field.append(line)
                continue

            if blank_line and line.endswith(":") and len(line.split()) == 1:
                # this is a new field name
                while cur_field and not cur_field[-1]:
                    # remove trailing blank lines
                    cur_field.pop()

                if cur_field and not field_name:
                    # there is data for a field present, but no field name
                    raise TaskSyntaxError(
                        "Missing field name for data:\n{}".format(
                            "\n".join(cur_field)))

                if field_name:
                    values[field_name] = "\n".join(cur_field)
                    cur_field = []

                field_name = line[:-1]
                if field_name in TaskInfo._READ_ONLY_FIELDS:
                    raise TaskSyntaxError(
                        "'{}' field is read-only".format(field_name))

                blank_line = False
                continue

            blank_line = False
            cur_field.append(line)

        # FIXME - redundant code
        while cur_field and not cur_field[-1]:
            # remove trailing blank lines
            cur_field.pop()

        if cur_field and not field_name:
            # there is data for a field present, but no field name
            raise TaskSyntaxError(
                "\nMissing field name for data:\n{{\n{}\n}}".format(
                    "\n".join(cur_field)))

        if field_name:
            values[field_name] = "\n".join(cur_field)

        return values

    @staticmethod
    def _select_editor():
        """Selects an editor based on the following rules:
           1) TASKEDITOR env var, if defined
           2) EDITOR env var, if defined
           3) vi (unix)
           4) notepad (windows)"""
        editor = os.environ.get("TASKEDITOR")
        if editor is not None:
            return editor

        editor = os.environ.get("EDITOR")
        if editor is not None:
            return editor

        is_windows = platform.system().lower().startswith("windows")
        return "notepad" if is_windows else "vi"

    def serialize(self, to_file=None):
        """Saves the task to file'"""
        if to_file is not None:
            raise ValueError(
                "TaskInfo does not support serialization to a custom filename")

        to_file = self.filename
        gitrepo.write_task(to_file, self.pretty(self.dict()))

    @staticmethod
    def _filename(task_id):
        """Constructs task filename from 'task_id'"""
        return "{}.json".format(task_id)

    @property
    def filename(self):
        """Property accessor for task filename"""
        return TaskInfo._filename(self.id)

    @classmethod
    def load(cls, from_file):
        """Loads a task from 'from_file'"""
        json_str = gitrepo.read_task(from_file)
        task_dict = json.loads(json_str)
        return cls(**task_dict)

    @classmethod
    def from_id(cls, task_id):
        """Returns a task object for the given task id"""
        return cls.load(TaskInfo._filename(task_id))


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
