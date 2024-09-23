import logging
from logging import handlers

# ANSI color codes
RESET = "\033[0m"
GREEN = "\033[32m"
WHITE = "\033[37m"
PURPLE = "\033[35m"
BLUE = "\033[34m"
RED = "\033[31m"


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'INFO': WHITE,
        'DEBUG': BLUE,
        'WARNING': WHITE,
        'ERROR': RED,
        'CRITICAL': WHITE
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, RESET)

        # Apply color to the message
        record.msg = f"{log_color}{record.msg}{RESET}"
        record.asctime = f"{WHITE}{self.formatTime(record)}{RESET}"
        record.levelname = f"{WHITE}{record.levelname}{RESET}"
        record.filename = f"{PURPLE}{record.filename}{RESET}"
        record.lineno = f"{WHITE}{record.lineno}{RESET}"
        record.threadName = f"{WHITE}{record.threadName}{RESET}"
        record.processName = f"{WHITE}{record.processName}{RESET}"

        return super().format(record)


class PlainFormatter(logging.Formatter):
    def format(self, record):
        # Use default formatting without colors
        return super().format(record)


def _logging(log, f_name, backup_count, level_tag):
    level = logging.INFO if level_tag == 'INFO' else logging.DEBUG

    # Define date format and message format
    datefmt = '[%Y-%m-%d %H:%M:%S]'
    format = '%(asctime)s - [%(levelname)s] - %(filename)s [line:%(lineno)s] - %(message)s'

    # Create formatters
    colored_formatter = ColoredFormatter(format, datefmt)
    plain_formatter = PlainFormatter(format, datefmt)

    # Setup file handler with plain formatter (no colors)
    th = handlers.TimedRotatingFileHandler(filename=f_name, when='D', interval=1, backupCount=backup_count, encoding='utf-8')
    th.setFormatter(plain_formatter)
    th.setLevel(level)
    log.addHandler(th)

    # Setup console handler with colored formatter
    ch = logging.StreamHandler()
    ch.setFormatter(colored_formatter)
    ch.setLevel(level)
    log.addHandler(ch)

    log.setLevel(level)
    return log
