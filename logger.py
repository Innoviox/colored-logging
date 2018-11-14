import logging as _logging
import time
import enum
import itertools
__all__ = ['debug', 'info', 'set_file', 'set_colors']

class Colors(enum.Enum):
    BLACK   = '\u001b[30m'
    RED     = '\u001b[31m'
    GREEN   = '\u001b[32m'
    YELLOW  = '\u001b[33m'
    BLUE    = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN    = '\u001b[36m'
    WHITE   = '\u001b[37m'
    RESET   = '\u001b[0m'

MACROS = {
    "$T": "time.ctime()",
    "$U": "self.user",
    "$L": "level",
    "$M": "message"
}

def _write(m, color):
    c = color.upper()
    if c in Colors.__members__:
        return f"{Colors[c].value}{m}{Colors['RESET'].value}"
    return m

class Logger:
    def __init__(self, file=f'LOGS_{time.ctime()}.txt', user='root',
                 colors=['blue', 'magenta', 'cyan', 'black'], fstr=['$T', '$U', '$L', '$M']):
        self.file = file
        self.user = user
        self.colors = colors
        self.fstr = fstr

    def _get_str(self, message, level, colors):
        f = [MACROS[macro] for macro in self.fstr]
        yield from itertools.starmap(_write, zip(map(eval, f), colors))
        yield "\n"
            
    def debug(self, message):
        with open(self.file, 'a') as file:
            for colored_str in self._get_str(message, "DEBUG", ["none"] * 4):
                print(colored_str, end=' ', file=file)

    def info(self, message):
        for colored_str in self._get_str(message, 'INFO', self.colors):
            print(colored_str, end=' ')

    def config(self, config):
        attrs = ['file', 'user', 'colors', 'fstr']
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

def config(config):
    _logger.config(config)

def debug(m):
    _logger.debug(m)

def info(m):
    _logger.info(m)
