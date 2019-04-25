#!/usr/bin/env python

"""
Command to move a task to the dorm (sleep)
"""

import datetime

import taskinfo
from custom_logger import get_logger

# log = get_logger('task')


def process_command(args):
    """Process sub-command 'sleep'"""

    with taskinfo.TaskMaster() as taskmaster:
        task = taskmaster.current_task
        if args.edit:
            task.edit()

        duration = datetime.timedelta(minutes=args.duration)
        taskmaster.sleep(duration)
        log = get_logger('task')
        log.debug("Sleep task '%s' for %d minutes", task.id, args.duration)


def create_parser(subparsers):
    """Create argument subparser for command 'sleep'"""
    subparser = subparsers.add_parser(
        'sleep', help='Defer the current task for some time')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-e", "--edit", action="store_true",
                           help="Invoke an editor for the task")
    # TODO: implement more flexible (free-text?) units
    subparser.add_argument("duration", type=int, help="Duration in minutes")
