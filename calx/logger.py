import logging


def create_logger(name: str = "calx", level=logging.INFO) -> logging.Logger:
    formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.setLevel(level)

    return logger


default_logger = create_logger()
