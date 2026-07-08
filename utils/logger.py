"""Central logging configuration.

Sets up three handlers writing into logs/: info, warning and error level
files, plus a stream handler for console output during development.
"""
from __future__ import annotations

import logging
import os


def setup_logging(log_dir: str = "logs") -> None:
    os.makedirs(log_dir, exist_ok=True)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.setLevel(logging.INFO)
    root.addHandler(console)

    info_handler = logging.FileHandler(os.path.join(log_dir, "info.log"), encoding="utf-8")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(fmt)
    root.addHandler(info_handler)

    warning_handler = logging.FileHandler(os.path.join(log_dir, "warning.log"), encoding="utf-8")
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(fmt)
    root.addHandler(warning_handler)

    error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"), encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(fmt)
    root.addHandler(error_handler)
