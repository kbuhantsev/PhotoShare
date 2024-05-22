import logging
from logging.handlers import RotatingFileHandler

# ANSI escape codes for colors
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
GREEN = '\033[92m'


class ColorFormatter(logging.Formatter):
    """ Custom formatter to add color to log levels """

    def format(self, record):
        color = ''
        if hasattr(record, 'custom_color') and record.custom_color:
            if record.levelno == logging.INFO:
                color = GREEN
        elif record.levelno == logging.WARNING:
            color = YELLOW
        elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            color = RED

        record.msg = f'{color}{record.msg}{RESET}'
        return super().format(record)


_format = "%(asctime)s [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"

_file = 'app.log'

file_handler = RotatingFileHandler(
                filename=_file,
                mode="a",
                maxBytes=1000000,  # 1mb
                backupCount=5,
                encoding="utf-8",
                delay=False,
            )
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(ColorFormatter(_format))


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
