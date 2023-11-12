from loguru import logger
import sys

class Logger:
    def __init__(self, log_file=None, log_level="INFO") -> None:
        if log_file is None:
            log_file = sys.stdout
        


