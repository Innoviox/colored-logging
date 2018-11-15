import logging as _logging
import time
import enum
import itertools

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
output is space-separated.
"""
MACROS = {
    "$T": "time.ctime()",
    "$U": "self.user",
    "$L": "level",
    "$M": "m"
}

def _write(m, color):
    """
    Returns a string colored with the given color.
    If the color is not a valid member of the Colors
    enum, simply returns the string.
    """
    c = color.upper()
    if c in Colors.__members__:
        return f"{Colors[c].value}{m}{Colors['RESET'].value}"
    return m

class Logger:
    def __init__(self, file=f'LOGS {time.ctime()}.txt', user='root',
                 colors=['blue', 'magenta', 'cyan', 'black'], fstr=['$T', '$U', '$L', '$M'],
                 max_line_length=20):
        self.file = file
        self.user = user
        self.colors = colors
        self.fstr = fstr
        self.max_line_length = max_line_length

    def _get_str(self, message, level, colors):
        mll = len(message) if self.max_line_length is None else self.max_line_length
        for m in [message[i:i+mll] for i in range(0, len(message), mll)]:
            f = [MACROS.get(macro, f"'{macro}'") for macro in self.fstr]
            yield from itertools.starmap(_write, itertools.zip_longest(map(eval, f), colors, fillvalue='black'))
            yield None
            
    def debug(self, message):
        with open(self.file, 'a') as file:
            for colored_str in self._get_str(message, "DEBUG", ["none"] * 4):
                if colored_str is None:
                    print(file=file)
                else:
                    print(colored_str, end=' ', file=file)

    def info(self, message):
        for colored_str in self._get_str(message, 'INFO', self.colors):
            if colored_str is None:
                print()
            else:
                print(colored_str, end=' ')

    def config(self, **config):
        attrs = ['file', 'user', 'colors', 'fstr', 'max_line_length']
        for name, value in config.items():
            if name in attrs:
                setattr(self, name, value)
                
_logger = Logger()

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
