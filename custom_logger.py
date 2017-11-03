#!/usr/bin/env python

import sys
import logging
import logging.config
from ansi_color import TermColor

color = TermColor()


class MyFormatter(logging.Formatter):
    def __init__(self, fmt="%(levelno)s: %(msg)s", datefmt=None):
        self.datefmt = datefmt
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        result = super(MyFormatter, self).format(record)
        if not color.strip_codes:
            if record.levelno == logging.DEBUG:
                result = result.replace("${color_start}", color.dark_white())
            elif record.levelno == logging.INFO:
                result = result.replace("${color_start}", color.light_white())
            elif record.levelno == logging.ERROR:
                result = result.replace("${color_start}", color.light_red())
        return result


if not color.strip_codes:
    color_start_marker = '${color_start}'
else:
    color_start_marker = ''

formatter = MyFormatter(color_start_marker +
                        '%(asctime)-15s %(name)s[%(levelname)s]' +
                        color.end() +
                        ' %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logging.root.addHandler(handler)
logging.root.setLevel(logging.DEBUG)


def get_logger(logger_name):
    return logging.getLogger(logger_name)
