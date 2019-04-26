#!/usr/bin/env python

"""
Command to show a task
"""

from __future__ import print_function

import taskinfo
# from custom_logger import get_logger


def print_task_summary(task_data):
    """Print one line summary of task information"""
    from ansi_color import TermColor
    tc = TermColor()
    print("{red}{id}{endc} {desc}".format(
        id=task_data["id"][:7],
        desc=task_data["description"],
        red=tc.light_red,
        endc=tc.end()
        ))


def process_command(args):
    """Process sub-command 'show'"""
    cur_task = None
    with taskinfo.TaskMaster() as taskmaster:
        if args.id is None:
            cur_task = taskmaster.current_task
        else:
            cur_task = taskmaster.find(args.id)

    if not cur_task:
        print("No tasks found!")
        return

    data = cur_task.dict()
    print_task_summary(data)


def create_parser(subparsers):
    """Create argument subparser for command 'add'"""
    subparser = subparsers.add_parser('show', help='Show current task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("id", nargs="?", default=None,
                           help="Task id")
