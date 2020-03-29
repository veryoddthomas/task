#!/usr/bin/env python

"""
Command to move a task from the backlog to the active stack
"""

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'activate'"""

    with taskinfo.TaskMaster() as taskmaster:
        taskmaster.activate(args.id)
        task = taskmaster.current_task
        assert task.id.startswith(args.id)
        if args.edit:
            task.edit()

        log = get_logger('task')
        log.debug("Activated task '%s'", task.id)


def create_parser(subparsers):
    """Create argument subparser for command 'activate'"""
    subparser = subparsers.add_parser('activate',
                                      help='Activate task from the backlog')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-e", "--edit", action="store_true",
                           help="Invoke an editor for the task")
    subparser.add_argument("id", help="Task id to activate")
