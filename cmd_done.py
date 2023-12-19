#!/usr/bin/env python3

"""
Command to close out a task
"""

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'done'"""

    with taskinfo.TaskMaster() as taskmaster:
        task = taskmaster.current_task
        if args.edit:
            task.edit()

        taskmaster.close()
        log = get_logger('task')
        log.debug("Completed task '%s'", task.id)
        # TODO: close this out in a way visible to git & its history


def create_parser(subparsers):
    """Create argument subparser for command 'done'"""
    subparser = subparsers.add_parser(
        'done', help='Close out the current task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-e", "--edit", action="store_true",
                           help="Invoke an editor for the task")
