# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""

import os
import secrets

from loguru import logger
from starlette.config import Config

# get environment variables
config = Config(".env")
USE_ENV = config("USE_ENV", default="docker")

SECRET_KEY = secrets.token_urlsafe(64)


if USE_ENV.lower() == "dotenv":
    logger.info(f"USE_ENV set to {USE_ENV}. Using .env file for external configuration")
    # Application information
    APP_VERSION = config("APP_VERSION", default="1.0.0")
    OWNER = config("OWNER", default="Mike Ryan")
    WEBSITE = config("WEBSITE", default="https://devsetgo.com")
    LICENSE_TYPE = config("LICENSE_TYPE", default="MIT")
    LICENSE_LINK = config(
        "LICENSE_LINK", default="https://github.com/devsetgo/starlette-SRTDashboard"
    )

    # Demo Data
    CREATE_SAMPLE_DATA = config("CREATE_SAMPLE_DATA", default=False)
    NUMBER_TASKS = config("NUMBER_TASKS", default=0)
    NUMBER_USERS = config("NUMBER_USERS", default=0)
    NUMBER_GROUPS = config("NUMBER_GROUPS", default=0)

    # Application Configurations
    HOST_DOMAIN = config("HOST_DOMAIN", default="https://devsetgo.com")
    RELEASE_ENV = config("RELEASE_ENV", default="prd")
    HTTPS_ON = config("HTTPS_ON", default="True")
    PROMETHEUS_ON=config("PROMETHEUS_ON",default="False")
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///sqlite_db/api.db"
    )

    # Loguru settings
    LOGURU_RETENTION = config("LOGURU_RETENTION", default="10 days")
    LOGURU_ROTATION = config("LOGURU_ROTATION", default="10 MB")
    LOGURU_LOGGING_LEVEL = config("LOGURU_LOGGING_LEVEL", default="WARNING")
    ADD_DEFAULT_GROUP = config("ADD_DEFAULT_GROUP", default="True")
    WORKERS = int(config("WORKERS", default=0))
else:
    logger.info(
        f"USE_ENV set to {USE_ENV}. Using os environmental settings for\
             external configuration"
    )
    # Application information
    APP_VERSION = os.environ["APP_VERSION"]
    logger.critical(APP_VERSION)
    if APP_VERSION is None:
        APP_VERSION = "0.0.1"

    OWNER = os.environ["OWNER"]
    if OWNER is None:
        OWNER = "example"

    WEBSITE = os.environ["WEBSITE"]
    if WEBSITE is None:
        WEBSITE = "http://www.example.com"

    LICENSE_TYPE = os.environ["LICENSE_TYPE"]
    if LICENSE_TYPE is None:
        LICENSE_TYPE = "MIT"

    LICENSE_LINK = os.environ["LICENSE_LINK"]
    if LICENSE_LINK is None:
        LICENSE_LINK = "http://www.example.com"

    # Demo Data
    CREATE_SAMPLE_DATA = os.environ["CREATE_SAMPLE_DATA"]
    if CREATE_SAMPLE_DATA is None:
        CREATE_SAMPLE_DATA = "False"

    NUMBER_TASKS = os.environ["NUMBER_TASKS"]
    if NUMBER_TASKS is None:
        NUMBER_TASKS = 10
    NUMBER_USERS = os.environ["NUMBER_USERS"]
    if NUMBER_USERS is None:
        NUMBER_USERS = 10

    NUMBER_GROUPS = os.environ["NUMBER_USERS"]
    if NUMBER_GROUPS is None:
        NUMBER_GROUPS = 10

    # Application Configurations
    HOST_DOMAIN = os.environ["HOST_DOMAIN"]
    if HOST_DOMAIN is None:
        HOST_DOMAIN = "https://example.com"

    RELEASE_ENV = os.environ["RELEASE_ENV"]
    if RELEASE_ENV is None:
        RELEASE_ENV = "prd"

    HTTPS_ON = os.environ["HTTPS_ON"]
    if HTTPS_ON is None:
        HTTPS_ON = True

    PROMETHEUS_ON=os.environ["PROMETHEUS_ON"]
    if PROMETHEUS_ON is None:
        PROMETHEUS_ON = False
        
    ADD_DEFAULT_GROUP = os.environ["ADD_DEFAULT_GROUP"]
    if ADD_DEFAULT_GROUP is None:
        ADD_DEFAULT_GROUP = "False"

    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    if SQLALCHEMY_DATABASE_URI is None:
        SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite_db/api.db"

    # Loguru settings
    LOGURU_RETENTION = os.environ["LOGURU_RETENTION"]
    if LOGURU_RETENTION is None:
        LOGURU_RETENTION = "10 days"

    LOGURU_ROTATION = os.environ["LOGURU_ROTATION"]
    if LOGURU_ROTATION is None:
        LOGURU_ROTATION = "100 MB"

    LOGURU_LOGGING_LEVEL = os.environ["LOGURU_LOGGING_LEVEL"]
    if LOGURU_LOGGING_LEVEL is None:
        LOGURU_LOGGING_LEVEL = "INFO"
    WORKERS = int(os.environ["WORKERS"])

    if WORKERS is None or WORKERS == 0:
        WORKERS = 0
