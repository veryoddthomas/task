#!/usr/bin/env python

import uuid


class Task:
    def __init__(self, task_type):
        self.id = uuid.uuid4()
        self.type = task_type


def process_command(args):
    task = Task(args.type)
    print("task id = {}".format(task.id))
    print("task type = {}".format(task.type))
    print(args)


def create_parser(subparsers):
    subparser = subparsers.add_parser('add', help='Add task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-t", "--type", help="type of task",
                           choices=['test', 'build', 'mentor', 'quick'],
                           default='quick')
