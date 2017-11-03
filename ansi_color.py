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


def fg(color): return color+30


def bg(color): return color+40


def light(color): return color+60


class TermColor(object):

    def __init__(self):
        if sys.stdout.isatty():
            self.strip_codes = False
        else:
            self.strip_codes = True

    def start(self, color):
        if self.strip_codes:
            return ""
        else:
            return '\033[{}m'.format(color)

    def end(self):
        if self.strip_codes:
            return ""
        else:
            return '\033[{}m'.format(RESET)

    def dark_black(self):
        return self.start(fg(BLACK))

    def dark_red(self):
        return self.start(fg(RED))

    def dark_green(self):
        return self.start(fg(GREEN))

    def dark_yellow(self):
        return self.start(fg(YELLOW))

    def dark_blue(self):
        return self.start(fg(BLUE))

    def dark_magenta(self):
        return self.start(fg(MAGENTA))

    def dark_cyan(self):
        return self.start(fg(CYAN))

    def dark_white(self):
        return self.start(fg(WHITE))

    def light_black(self):
        return self.start(light(fg(BLACK)))

    def light_red(self):
        return self.start(light(fg(RED)))

    def light_green(self):
        return self.start(light(fg(GREEN)))

    def light_yellow(self):
        return self.start(light(fg(YELLOW)))

    def light_blue(self):
        return self.start(light(fg(BLUE)))

    def light_magenta(self):
        return self.start(light(fg(MAGENTA)))

    def light_cyan(self):
        return self.start(light(fg(CYAN)))

    def light_white(self):
        return self.start(light(fg(WHITE)))

    def dark_black_bg(self):
        return self.start(bg(BLACK))

    def dark_red_bg(self):
        return self.start(bg(RED))

    def dark_green_bg(self):
        return self.start(bg(GREEN))

    def dark_yellow_bg(self):
        return self.start(bg(YELLOW))

    def dark_blue_bg(self):
        return self.start(bg(BLUE))

    def dark_magenta_bg(self):
        return self.start(bg(MAGENTA))

    def dark_cyan_bg(self):
        return self.start(bg(CYAN))

    def dark_white_bg(self):
        return self.start(bg(WHITE))

    def light_black_bg(self):
        return self.start(light(bg(BLACK)))

    def light_red_bg(self):
        return self.start(light(bg(RED)))

    def light_green_bg(self):
        return self.start(light(bg(GREEN)))

    def light_yellow_bg(self):
        return self.start(light(bg(YELLOW)))

    def light_blue_bg(self):
        return self.start(light(bg(BLUE)))

    def light_magenta_bg(self):
        return self.start(light(bg(MAGENTA)))

    def light_cyan_bg(self):
        return self.start(light(bg(CYAN)))

    def light_white_bg(self):
        return self.start(light(bg(WHITE)))


if __name__ == '__main__':
    color = TermColor()
    print(color.light_black() + "HELLO FG LIGHT BLACK" + color.end())
    print(color.light_red() + "HELLO FG LIGHT RED" + color.end())

    print(color.light_yellow() + color.light_black_bg() +
          "HELLO - FG LIGHT YELLOW - BG LIGHT BLACK" + color.end())
    print(color.light_red() + color.light_black_bg() +
          "HELLO - FG LIGHT RED - BG LIGHT BLACK" + color.end())
