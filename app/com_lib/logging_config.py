# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from loguru import logger

from settings import config_settings


def config_logging():
    # remove default logger
    logger.remove()
    # set file path
    log_path = Path.cwd().joinpath("logfile").joinpath("app_log.log")
    # add new configuration
    logger.add(
        log_path,  # log file path
        level=config_settings.loguru_logging_level.upper(),  # logging level
        format="{time:yyyy-mm-dd at hh:mm:ss} | {level} | {message}",  # format of log
        enqueue=True,  # set to true for async or multiprocessing logging
        backtrace=False,  # turn to false if in production to prevent data leaking
        rotation=config_settings.loguru_rotation,  # file size to rotate
        retention=config_settings.loguru_retention,  # how long a the logging data persists
        compression="zip",  # log rotation compression
        serialize=False,  # if you want it json style, set to true. but also change the format
    )

    # intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=config_settings.loguru_logging_level.upper(),
    )

    # logger.remove()
    # log_path = Path.cwd().joinpath("logfile").joinpath("app_log.log")
    # # logger.remove()
    # logger.add(
    #     log_path,
    #     format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    #     enqueue=True,
    #     backtrace=False,
    #     rotation=LOGURU_ROTATION,
    #     retention=LOGURU_RETENTION,
    #     level=LOGURU_LOGGING_LEVEL,
    #     compression="zip",
    #     serialize=False,
    # )

    # class InterceptHandler(logging.Handler):
    #     def emit(self, record):
    #         # Retrieve context where the logging call occurred, this happens to be in
    #         #  the 6th frame upward
    #         logger_opt = logger.opt(depth=6, exception=record.exc_info)
    #         logger_opt.log(record.levelno, record.getMessage())

    # logging.basicConfig(handlers=[InterceptHandler()], level=LOGURU_LOGGING_LEVEL)


def request_parser(request_data):
    client_host = request_data.client.host
    meth = request_data.method
    url_path = request_data.url.path
    head = request_data.headers["user-agent"]
    logger.info(f"{client_host} | {meth} | {url_path} | {head}")
