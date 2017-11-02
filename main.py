import cmd_add
import cmd_del
import argparse
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
#             json.dump(settings, settings_file, sort_keys=True, indent=4, separators=(',', ': '))


def create_command_line_parser():
    global version
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s version {}'.format(version))
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")
    subparsers = parser.add_subparsers(title="commands", metavar=None)  # "<command>")

    cmd_add.create_parser(subparsers)
    cmd_del.create_parser(subparsers)

    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser


def main(params):
    p = create_command_line_parser()
    parsed_args = p.parse_args(params)

    # if parsed_args.verbosity > 0:
    #     print "Verbosity: {}".format(parsed_args.verbosity)
    #updater = update.Updater()
    #updater.update()
    #initialize_settings("$HOME/.swe/settings")

    retval = 0
    try:
        parsed_args.func(parsed_args)
    except ExceptionCommandFailed:
        retval = 1

    return retval
