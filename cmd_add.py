#!/usr/bin/env python

"""
Command to add a task
"""

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'add'"""
    if args.edit:
        task = taskinfo.TaskInfo("<description>", "quick")
        task.edit()
    else:
        task = taskinfo.TaskInfo(args.summary, args.type)
    log = get_logger('task')
    log.info("task id = %s" % task.id)
    log.info("task type = %s" % task.type)


def create_parser(subparsers):
    """Create argument subparser for command 'add'"""
    subparser = subparsers.add_parser('add', help='Add task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-e", "--edit", action="store_true",
                           help="Invoke an editor for the task")
    subparser.add_argument("-s", "--summary", help="Summary of task")
    subparser.add_argument("-t", "--type", help="Type of task",
                           choices=['test', 'build', 'mentor', 'quick'],
                           default='quick')
