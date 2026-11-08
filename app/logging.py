import logging

LEVELS = {"fatal": 50, "error": 40, "warn": 30, "info": 20, "debug": 10, "trace": 5}

class _Trace(logging.DEBUG.__class__):
    level = 5

logging.addLevelName(5, "TRACE")

def get_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
