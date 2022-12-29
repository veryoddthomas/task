#!/usr/bin/env python

"""
Command to show a task
"""

from __future__ import print_function

import taskinfo
from ansi_color import TermColor
# from custom_logger import get_logger


def print_task_summary(task_data, color=None):
    """Print one line summary of task information"""
    tc = TermColor()
    if color is None:
        color = tc.light_green
    print("  {c1}{id}{endc}  {c2}{pri}{endc}  {desc}".format(
        id=task_data["id"][:7],
        pri=task_data["priority"],
        desc=task_data["description"],
        c1=color,
        c2=tc.light_black,
        endc=tc.end()
        ))


def print_tasks(tm):
    tc = TermColor()
    _task_groups = [
        ("Active Tasks", tm.stack, tc.light_green),
        ("Blocked Tasks", tm.blocked, tc.light_red),
        ("Sleeping Tasks", tm.sleeping, tc.light_black),
        ("Backlog Tasks", tm.backlog, tc.light_blue),
    ]
    # for struct in _structs
    for group_name, group, color in _task_groups:
        print("{}{}{}".format(tc.light_white, group_name, tc.end()))
        # print("=" * len(group_name))
        found = False
        for task in group:  # .find_all():
            data = task.dict()
            print_task_summary(data, color)
            found = True
        if not found:
            print("  None")


def process_command(args):
    """Process sub-command 'show'"""
    with taskinfo.TaskMaster() as taskmaster:
        if args.show_all:
            print_tasks(taskmaster)
            return

        stack_size = len(taskmaster.stack)
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
    subparser.add_argument("-a", "--show-all", action="store_true",
                           help="Show all tasks")
    subparser.add_argument("id", nargs="?", default=None,
                           help="Task id")
