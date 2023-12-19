#!/usr/bin/env python3

"""
Debug module.  We can put code here to try things out.  This command could
be removed completely when we deploy the tool.  Nothing else should
depend on this.
"""

from custom_logger import get_logger
log = get_logger('task')


def demonstrate_logging():
    """Demonstrate logging"""
    # DEBUG, INFO, WARNING, ERROR, CRITICAL
    print("=" * 72)
    print("Demonstrating Logging Levels")
    print("=" * 72)
    log.critical("This is a critical message")
    log.error("This is an error message")
    log.warning("This is a warning message")
    log.info("This is an info message")
    log.debug("This is a debug message")


def process_command(args):
    """Process sub-command 'debug'"""
    if args.demo_logging:
        demonstrate_logging()


def create_parser(subparsers):
    """Create argument subparser for command 'add'"""
    subparser = subparsers.add_parser('debug', help='Debug tools')
    subparser.set_defaults(func=process_command)
    subparser.add_argument("-l", "--demo-logging", help="Demonstrate logging",
                           action='store_true')
