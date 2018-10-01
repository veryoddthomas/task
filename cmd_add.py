#!/usr/bin/env python

"""
Command to add a task
"""

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'add'"""

    taskmaster = taskinfo.TaskMaster()
    task = taskinfo.TaskInfo(args.summary, args.type)
    taskmaster.add(task)
    log = get_logger('task')
    log.info("task id = %s" % task.id)
    log.info("task type = %s" % task.type)


def create_parser(subparsers):
    """Create argument subparser for command 'add'"""
    subparser = subparsers.add_parser('add', help='Add task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-s", "--summary", help="Summary of task")
    subparser.add_argument("-t", "--type", help="Type of task",
                           choices=['test', 'build', 'mentor', 'quick'],
                           default='quick')
