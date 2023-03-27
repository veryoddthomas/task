#!/usr/bin/env python

"""
Helper module for simple generation of ANSI escape sequences used for terminal
color control.
"""

import sys

# The following info is from http://ascii-table.com/ansi-escape-sequences.php

# Esc[Value;...;Valuem    Set Graphics Mode:
# Calls the graphics functions specified by the following values. These
# functions remain active until the next occurrence of this escape sequence.
# Graphics mode changes the colors and attributes of text (such as bold and
# underline) displayed on the screen.

# Text attributes
# 0   All attributes off
# 1   Bold on
# 4   Underscore (on monochrome display adapter only)
# 5   Blink on
# 7   Reverse video on
# 8   Concealed on

# Foreground colors
# 30  Black         90  Bright Black
# 31  Red           91  Bright Red
# 32  Green         92  Bright Green
# 33  Yellow        93  Bright Yellow
# 34  Blue          94  Bright Blue
# 35  Magenta       95  Bright Magenta
# 36  Cyan          96  Bright Cyan
# 37  White         97  Bright White

# Background colors
# 40  Black
# 41  Red
# 42  Green
# 43  Yellow
# 44  Blue
# 45  Magenta
# 46  Cyan
# 47  White

# Parameters 30 through 47 meet the ISO 6429 standard.

# Base colors
BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

# Attributes
RESET = 0
BOLD = 1
UNDERLINE = 4
BLINK = 5
REVERSE = 7
CONCEALED = 8


def fg(color):  # pylint: disable=invalid-name
    """Constructs foreground color from color offset"""
    return color+30


def bg(color):  # pylint: disable=invalid-name
    """Constructs background color from color offset"""
    return color+40


def light(color):
    """Constructs light foreground color from color offset"""
    return color+60


class TermColor(object):
    """Provides methods to emit ANSI escape sequences to control terminal
       color if appropriate.  Will emit empty strings if current stdout
       is not a tty. """

    def __init__(self):
        if sys.stdout.isatty():
            self.strip_codes = False
        else:
            self.strip_codes = True

    def start(self, color):
        """Generate ANSI escape sequence to set color"""
        if self.strip_codes:
            return ""
        return '\033[{}m'.format(color)

    def reset(self):
        """Generate ANSI escape sequence to reset color to default"""
        if self.strip_codes:
            return ""
        return '\033[{}m'.format(RESET)

    @property
    def dark_black(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(BLACK))

    @property
    def dark_red(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(RED))

    @property
    def dark_green(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(GREEN))

    @property
    def dark_yellow(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(YELLOW))

    @property
    def dark_blue(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(BLUE))

    @property
    def dark_magenta(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(MAGENTA))

    @property
    def dark_cyan(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(CYAN))

    @property
    def dark_white(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(fg(WHITE))

    @property
    def light_black(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(BLACK)))

    @property
    def light_red(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(RED)))

    @property
    def light_green(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(GREEN)))

    @property
    def light_yellow(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(YELLOW)))

    @property
    def light_blue(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(BLUE)))

    @property
    def light_magenta(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(MAGENTA)))

    @property
    def light_cyan(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(CYAN)))

    @property
    def light_white(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(fg(WHITE)))

    @property
    def dark_black_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(BLACK))

    @property
    def dark_red_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(RED))

    @property
    def dark_green_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(GREEN))

    @property
    def dark_yellow_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(YELLOW))

    @property
    def dark_blue_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(BLUE))

    @property
    def dark_magenta_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(MAGENTA))

    @property
    def dark_cyan_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(CYAN))

    @property
    def dark_white_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(bg(WHITE))

    @property
    def light_black_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(BLACK)))

    @property
    def light_red_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(RED)))

    @property
    def light_green_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(GREEN)))

    @property
    def light_yellow_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(YELLOW)))

    @property
    def light_blue_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(BLUE)))

    @property
    def light_magenta_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(MAGENTA)))

    @property
    def light_cyan_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(CYAN)))

    @property
    def light_white_bg(self):
        """Generate ANSI escape sequence to set color to named value"""
        return self.start(light(bg(WHITE)))

    @property
    def end(self):
        return self.reset()


if __name__ == '__main__':
    # pylint: disable=fixme
    c = TermColor()
    print(f"{c.light_red}{c.light_black_bg}Hello{c.end} there")
