#!/usr/bin/env python

"""
Custom logging support.  Enables level-specific formatting.
"""

import logging
import logging.config
# logging.basicConfig()


import sys
from ansi_color import TermColor

COLOR = TermColor()

if not COLOR.strip_codes:
    COLOR_START_MARKER = '${color_start}'
    COLOR_END_MARKER = '${color_end}'
else:
    COLOR_START_MARKER = ''
    COLOR_END_MARKER = ''


class MyFormatter(logging.Formatter):
    """Custom color-enabled formatter for our logging"""
    def __init__(self, fmt="%(levelno)s: %(msg)s", datefmt=None):
        self.datefmt = datefmt
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        result = super(MyFormatter, self).format(record)
        if not COLOR.strip_codes:
            if record.levelno == logging.DEBUG:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.light_black)
            elif record.levelno == logging.INFO:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.light_blue)
            elif record.levelno == logging.WARNING:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.light_yellow)
            elif record.levelno == logging.ERROR:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.light_red)
            elif record.levelno == logging.CRITICAL:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.light_red)
            else:
                result = result.replace(COLOR_START_MARKER,
                                        COLOR.dark_white)
        result = result.replace(COLOR_END_MARKER, COLOR.end())
        return result


FORMATTER = MyFormatter(COLOR_START_MARKER +
                        '%(asctime)-15s %(name)s[%(levelname)s]' +
                        COLOR_END_MARKER +
                        ' %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(FORMATTER)
logging.root.addHandler(HANDLER)
logging.root.setLevel(logging.WARNING)


def get_logger(logger_name):
    """Function to get default logger for this application"""
    return logging.getLogger(logger_name)
