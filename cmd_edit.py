#!/usr/bin/env python

"""
Command to edit a task
"""

import taskinfo
# from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'edit'"""

    with taskinfo.TaskMaster() as taskmaster:
        if args.id is None:
            cur_task = taskmaster.current_task
        else:
            cur_task = taskmaster.find(args.id)

        cur_task.edit()


def create_parser(subparsers):
    """Create argument subparser for command 'edit'"""
    subparser = subparsers.add_parser('edit', help='Edit a task')
    subparser.add_argument("id", nargs="?", help="Task id to edit")
    subparser.set_defaults(func=process_command)
