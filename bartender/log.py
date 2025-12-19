import logging.config

from rich.logging import RichHandler


def setup_logging(verbosity: int) -> None:
    level = None

    match verbosity:
        case 0:
            level = logging.WARN
        case 1:
            level = logging.INFO
        case _:
            level = logging.DEBUG

    L.setLevel(level)


L = logging.Logger('bartender')
L.addHandler(RichHandler())
