#!/usr/bin/env python

"""
Command to add a task
"""

import taskinfo


def process_command(args):
    """Process sub-command 'add'"""
    task = taskinfo.TaskInfo(args.summary, args.type)
    print("task id = {}".format(task.id))
    print("task type = {}".format(task.type))
    print(args)


def create_parser(subparsers):
    """Create argument subparser for command 'add'"""
    subparser = subparsers.add_parser('add', help='Add task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-s", "--summary", help="Summary of task")
    subparser.add_argument("-t", "--type", help="Type of task",
                           choices=['test', 'build', 'mentor', 'quick'],
                           default='quick')
