#! /usr/bin/env python3

import logging
from functools import wraps
from typing import Callable
from pathlib import Path
import inspect

logging.captureWarnings(True)

wlogger = logging.getLogger("py.warnings")
wlogger.setLevel(logging.WARNING)


def log_to_file(level=logging.INFO) -> Callable:
    def decorator(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()

            log_path = bound.arguments.get("log_file_path")
            logger = logging.getLogger()  # root logger
            logger.setLevel(level)

            if not logger.handlers:

                formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

                if log_path is not None:

                    handler = logging.FileHandler(log_path, encoding="utf-8")

                else:

                    handler = logging.StreamHandler()

                handler.setFormatter(formatter)
                logger.addHandler(handler)

            try:
                logger.info(
                    "download completed successfully",
                )

                result = func(*args, **kwargs)

                logger.info(
                    "download completed successfully",
                )
                return result

            except Exception:
                logger.exception('Exception in "%s"', bound.arguments.get("url"))
                raise

            finally:
                if handler:
                    handler.close()
                    logger.removeHandler(handler)

        return wrapper

    return decorator
