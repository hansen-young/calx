import logging


def create_logger(name: str = "calx", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.setLevel(level)

    return logger


default_logger = create_logger()
