#!/usr/bin/env python3

"""
Command to delete a task
"""


def process_command(args):
    """Process sub-command 'del'"""
    print(args)


def create_parser(subparsers):
    """Create argument subparser for command 'del'"""
    subparser = subparsers.add_parser('del', help='Delete task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("task", help="task id")
