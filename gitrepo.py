"""Library of git repository operations"""

import logging
import os
import shlex
import subprocess

# Constants
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_REPOSITORY_PATH = os.path.join(EXEC_DIR, ".tasks")

# Globals
logger = logging.getLogger("task")
REPOSITORY = None


class InvalidRepository(RuntimeError):
    """Exception raised when a bad/invalid Git repository is detected"""


class GitRepository(object):
    """Class representing a Git repository"""
    def __init__(self, location):
        self._dir_stack = []
        self._location = location
        self._init_check()

    def _init_check(self):
        """Checks if this is a valid git repository, else initializes one"""
        if not os.path.exists(self._location):
            os.makedirs(self._location)

        with self:
            try:
                git_root = self._git_command("rev-parse --show-toplevel",
                                             quiet=True)
                if os.path.abspath(os.path.normpath(git_root)) != \
                        os.path.abspath(os.path.normpath(self._location)):
                    raise InvalidRepository(
                        "(invalid) git root found @{}".format(
                            git_root))

                logger.debug("valid git repo found @%s", self._location)
            except (subprocess.CalledProcessError, InvalidRepository):
                self._git_command("init")

    def __enter__(self):
        """'with' context entry handler"""
        self._dir_stack.append(os.getcwd())
        os.chdir(self._location)

    def __exit__(self, obj_type, obj_value, traceback):
        """'with' context exit handler"""
        old_pwd = self._dir_stack.pop()
        os.chdir(old_pwd)

    def _git_command(self, command, quiet=False):
        """Invoke 'git <command>' in the shell"""
        command = "git {}".format(command)
        with self:
            try:
                logger.debug(command)
                output = subprocess.check_output(command, shell=True)
                logger.debug(output)
            except subprocess.CalledProcessError as e:
                error_msg = "git cmd: {}\n{}".format(command, e.output)
                if quiet:
                    logger.debug(error_msg)
                else:
                    logger.error(error_msg)
                raise

        return output

    def add(self, filename):
        """Stages 'filename' for commit"""
        command = "add {}".format(filename)
        self._git_command(command)

    def commit(self, message):
        """Commits any pending changes"""
        escaped_message = shlex.quote(message)
        command = "commit -m {}".format(escaped_message)
        try:
            self._git_command(command)
        except subprocess.CalledProcessError as e:
            print("No change detected.  Ignoring update.")

    @property
    def location(self):
        """Property accessor for repository location"""
        return self._location


class TaskRepo(object):
    """Class wrapping a Git repository to store task objects"""
    def __init__(self, location):
        self.repo = GitRepository(location)

    def read_task(self, task_file):
        """Reads 'task_file' & returns its string contents"""
        task_path = os.path.join(self.task_path, task_file)
        with self.repo:
            with open(task_path) as infile:
                data = infile.read()

        return data

    def write_task(self, task_file, data, commit_message=None):
        """Writes 'data' to 'task_file' & commits the update with an
           optional custom 'commit_message'"""
        task_path = os.path.join(self.task_path, task_file)
        with self.repo:
            # create the directory if it does not exist
            dirname = os.path.dirname(task_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            with open(task_path, 'w') as outfile:
                outfile.write(data)

        if commit_message is None:
            task_id, _ = os.path.splitext(task_file)
            commit_message = "Update task {}".format(task_id)

        self.repo.add(task_path)
        self.repo.commit(commit_message)

    @property
    def task_path(self):
        """Property accessor for task file location"""
        return "tasks"


def get_repository(location=None):
    """Returns a singleton instance of the Git repository"""
    global REPOSITORY  # pylint: disable=global-statement
    if location is None:
        location = DEFAULT_REPOSITORY_PATH

    if REPOSITORY is None:
        REPOSITORY = TaskRepo(location)

    return REPOSITORY


def write_task(task_file, data, commit_message=None):
    """Writes 'data' to 'task_file' & commits the update"""
    taskrepo = get_repository()
    taskrepo.write_task(task_file, data, commit_message)


def read_task(task_file):
    """Reads & returns string data from 'task_file'"""
    taskrepo = get_repository()
    return taskrepo.read_task(task_file)
