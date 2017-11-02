#!/usr/bin/env python

import os
from runner import *


class Task:
    task_count = 0

    def __init__(self, task_type):
        self.id = Task.task_count
        self.type = task_type
        Task.task_count += 1


def process_command(args):
    task = Task(args.type)
    print "task id = {}".format(task.id)
    print "task type = {}".format(task.type)
    print args


def create_parser(subparsers):
    subparser = subparsers.add_parser('add', help='Add task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-t", "--type", help="type of task",
                           choices=['test', 'build', 'mentor'],
                           default='test')
