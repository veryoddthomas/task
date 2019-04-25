#!/usr/bin/env python

"""
Command to move a task to the backlog
"""

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'pop'"""

    with taskinfo.TaskMaster() as taskmaster:
        task = taskmaster.current_task
        if args.edit:
            task.edit()

        taskmaster.move()
        log = get_logger('task')
        log.debug("Moved task '%s' to backlog", task.id)


def create_parser(subparsers):
    """Create argument subparser for command 'pop'"""
    subparser = subparsers.add_parser('pop', help='Move task to backlog')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-e", "--edit", action="store_true",
                           help="Invoke an editor for the task")
