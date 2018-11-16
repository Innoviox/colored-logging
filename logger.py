import logging as _logging
import time
import enum
import itertools
import os
import sys

class Colors(enum.Enum):
    """
    These values represent the colors that can be used in
    the terminal. They are the standard ANSI codes and should
    work on any system. Every color has to be terminated with
    the RESET code so that it doesn't carry over.
    """
    BLACK   = '\u001b[30m'
    RED     = '\u001b[31m'
    GREEN   = '\u001b[32m'
    YELLOW  = '\u001b[33m'
    BLUE    = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN    = '\u001b[36m'
    WHITE   = '\u001b[37m'
    RESET   = '\u001b[0m'

"""
These macros are expanded from the Logger.fstr attribute.
Anything that is not in these macros will be interpreted
as a raw string. For example, if Logger.fstr is ['$T', '$U', '$M'],
the output will be the time, the user, and the message. The
output is space-separated. If you want part of the
output to be colored, put the color after like this: $T:RED.
No color means black output.
"""
MACROS = {
    "$T": "time.strftime(self.datefmt, time.gmtime())",
    "$U": "self.user",
    "$L": "level",
    "$M": "m"
}

def _colorize(m, color):
    """
    Returns a string colored with the given color.
    If the color is not a valid member of the Colors
    enum, simply returns the string.
    """
    c = color.upper()
    if c in Colors.__members__:
        return Colors[c].value + m + Colors.RESET.value
    return m

class Logger:
    def __init__(self, file='logs/nephos.log', user=os.getlogin(),
                 fstr=['$T:BLUE', '$U:MAGENTA', '$L:CYAN', '$M'],
                 max_line_length=50, datefmt='%m/%d/%Y %H:%M:%S'):
        """
        This class handles the logging. Multiple Loggers can be instantiated.
        file: the file to write to in DEBUG mode
        user: the user logging, default is the current user
        fstr: the way the output should be formatted. See MACROS.
        max_line_length: maximum output length per line. None for all in one line.
        datefmt: the way the date should be formatted
        """
        self.file = file
        self.user = user
        self.fstr = fstr
        self.max_line_length = max_line_length
        self.datefmt = datefmt

    def _get_str(self, message, level, _colors=None):
        """
        Get the colored string given the Logger's fstr.
        The _colors option is to override the user's given colors.
        """
        mll = len(message) if self.max_line_length is None else self.max_line_length
        for m in [message[i:i+mll] for i in range(0, len(message), mll)]:
            split = [i.split(":") if ":" in i else [i, "none"] for i in self.fstr]
            macros = [MACROS.get(macro, "'{}'".format(macro)) for macro, _ in split]
            colors = [color for _, color in split] if _colors is None else _colors
            yield from itertools.starmap(_colorize, itertools.zip_longest(map(eval, macros), colors, fillvalue='none'))
            yield None

    def _output(self, message, level, file, _colors=None):
        """
        Utility method to output message with given level to given file.
        """
        for colored_str in self._get_str(message, level, _colors=_colors):
            if colored_str is None:
                print(file=file)
            else:
                print(colored_str, end=' ', file=file)
                
    def debug(self, message):
        """
        The default debug method to output to a file without colors.
        """
        with open(self.file, 'a') as file:
            self._output(message, "DEBUG", file, _colors=["none"])

    def info(self, message):
        """
        The default info method to log to stdout with given colors.
        """
        self._output(message, "INFO", sys.stdout)

    def config(self, **config):
        """
        Configure the Logger with the given keyword arguments.
        """
        attrs = ['file', 'user', 'fstr', 'max_line_length', 'datefmt']
        for name, value in config.items():
            if name in attrs:
                setattr(self, name, value)
                
_logger = Logger()

"""
The following are utility methods that act on a shared Logger instance.
You can either call these directly from the module, or instantiate
a Logger class and log with that.
"""
def set_file(f):
    _logger.file = f

def set_colors(colors):
    _logger.colors = colors

def set_format(fstr):
    _logger.fstr = fstr

def config(**config):
    _logger.config(**config)

def debug(m):
    _logger.debug(m)

def info(m):
    _logger.info(m)
