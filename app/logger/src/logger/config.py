import logging
import sys
from pathlib import Path


_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_CONFIGURED: set[str] = set()


def get_logger(
    name: str,
    *,
    level: int = logging.INFO,
    log_dir: Path | None = None,
) -> logging.Logger:
    if name in _CONFIGURED:
        return logging.getLogger(name)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / f"{name}.log")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    _CONFIGURED.add(name)
    return logger
