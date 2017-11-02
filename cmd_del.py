#!/usr/bin/env python

import os
from runner import *


def process_command(args):
    print args


def create_parser(subparsers):
    subparser = subparsers.add_parser('del', help='Delete task')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("task", help="task id")
