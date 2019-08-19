import logging
import os
from pathlib import Path

from loguru import logger

from settings import LOGURU_RETENTION, LOGURU_ROTATION, RELEASE_ENV


def config_logging():
    """
    Set logging configuration and if in development, allow backtrace to be True.
    """
    LOGURU_BACKTRACE = False
    LOGGING_HANDLER_LEVEL = 20
    if RELEASE_ENV.lower() == "dev":
        LOGURU_BACKTRACE = True
        LOGGING_HANDLER_LEVEL = 10

    log_path = Path.cwd().joinpath("logfile").joinpath("app_log.log")
    logger.add(
        log_path,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        enqueue=True,
        backtrace=LOGURU_BACKTRACE,
        rotation=LOGURU_ROTATION,
        retention=LOGURU_RETENTION,
        compression="zip",
    )

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=LOGGING_HANDLER_LEVEL)
