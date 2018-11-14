import logging as _logging
import time
import enum
import itertools
__all__ = ['debug', 'info', 'set_file']

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

def _write(m, color):
    c = color.upper()
    if c in Colors.__members__:
        return f"{Colors[c].value}{m}{Colors['RESET'].value}"
    return m

class Logger:
    def __init__(self, file=f'LOGS_{time.time()}.txt', user='root',):
                 # format_func=lambda user, level, message:[str(time.time()), self.user,level, message]):
        self.file = file
        self.user = user
        # self.format_func = format_func
        self.colors = ['blue', 'magenta', 'cyan', 'black']

    def _get_str(self, message, level):
        yield from itertools.starmap(_write, zip([time.time(), self.user, level, message], self.colors))
            
    def debug(self, message):
        print(f"DEBUG:{self.user}:{message}", file=open(self.file, 'a'))

    def info(self, message):
        for colored_str in self._get_str(message, 'INFO'):
            print(colored_str, end=' ')

logger = Logger()

def set_file(f):
    logger.file = f

def debug(m):
    logger.debug(m)

def info(m):
    logger.info(m)

info("hi!")
