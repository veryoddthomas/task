"""Task Manager"""

from custom_logger import *

# import logging
# logging.basicConfig()
# logger = logging.getLogger('task')
# logger.setLevel(logging.INFO)
import argparse
import os
try:
    import argcomplete
except ImportError:
    argcomplete = None

version = "1.0.0"


# def initialize_settings(settings_file_name):
#     global settings
#     if os.path.isfile(settings_file_name):
#         with open(settings_file_name, "r+") as settings_file:
#             settings = json.load(settings_file)
#     else:
#         with open(settings_file_name, "w+") as settings_file:
#             json.dump(settings, settings_file, sort_keys=True, indent=4,
#                       separators=(',', ': '))


def find_commands():
    all_commands = []
    for (_, _, filenames) in os.walk(os.path.dirname(
            os.path.realpath(__file__))):
        filenames = [f for f in filenames
                     if f.startswith("cmd_") and f.endswith(".py")]
        c = [f[:-3] for f in filenames]
        all_commands.extend(c)
    return all_commands


def create_command_line_parser(modules):
    global version
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s version {}'.format(version))
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")
    subparsers = parser.add_subparsers(title="commands", metavar=None)

    # cmd_add.create_parser(subparsers)
    # cmd_del.create_parser(subparsers)
    for m in modules:
        m.create_parser(subparsers)

    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser


def main(params):
    commands = find_commands()
    command_modules = []
    for command in commands:
        new_module = __import__(command)
        command_modules.append(new_module)

    p = create_command_line_parser(command_modules)
    parsed_args = p.parse_args(params)

    if parsed_args.verbosity > 0:
        logger.setLevel(logging.DEBUG)

    # logger.debug("logmsg")
    # logger.info("Log level = {}".format(logger.getEffectiveLevel()))

    log = get_logger('task')
    log.error("error")
    log.info("info")
    log.debug("debug")

    # if parsed_args.verbosity > 0:
    #     print "Verbosity: {}".format(parsed_args.verbosity)

    # updater = update.Updater()
    # updater.update()
    # initialize_settings("$HOME/.task/settings")

    retval = 0
    try:
        parsed_args.func(parsed_args)
    except Exception:
        retval = 1

    return retval
