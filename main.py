"""Task Manager main module"""

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

from custom_logger import get_logger
log = get_logger('task')

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
    """Dynamically discover cmd_*.py files and return the list of names
       to import"""
    all_commands = []
    for (_, _, filenames) in os.walk(os.path.dirname(
            os.path.realpath(__file__))):
        filenames = [filename for filename in filenames
                     if filename.startswith("cmd_") and
                     filename.endswith(".py")]
        commands = [filename[:-3] for filename in filenames]
        all_commands.extend(commands)
    return all_commands


def create_command_line_parser(modules):
    """Create top level command-line parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s version {}'.format(version))
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")
    subparsers = parser.add_subparsers(title="commands", metavar=None)

    for module in modules:
        module.create_parser(subparsers)

    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser


def main(params):
    """Create top level command-line parser"""
    commands = find_commands()
    command_modules = []
    for command in commands:
        new_module = __import__(command)
        command_modules.append(new_module)

    parser = create_command_line_parser(command_modules)
    parsed_args = parser.parse_args(params)

    # updater = update.Updater()
    # updater.update()
    # initialize_settings("$HOME/.task/settings")

    retval = 0
    try:
        parsed_args.func(parsed_args)
    except RuntimeError:
        retval = 1

    return retval
