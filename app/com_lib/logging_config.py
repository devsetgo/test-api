# -*- coding: utf-8 -*-
from pathlib import Path
import json
from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from settings import LOGURU_RETENTION
from settings import LOGURU_ROTATION
from settings import LOGURU_LOGGING_LEVEL
import logging, sys


def config_logging():

    log_path = Path.cwd().joinpath("logfile").joinpath("app_log.log")
    logger.add(
        log_path,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        enqueue=True,
        backtrace=False,
        rotation=LOGURU_ROTATION,
        retention=LOGURU_RETENTION,
        level=LOGURU_LOGGING_LEVEL,
        compression="zip",
        serialize=True,
    )
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=LOGURU_LOGGING_LEVEL)

def request_parser(request_data):
    client_host = request_data.client.host
    meth = request_data.method
    url_path = request_data.url.path
    head = request_data.headers["user-agent"]
    logger.info(f"{client_host} | {meth} | {url_path} | {head}")
