# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""

from starlette.config import Config
import os
from loguru import logger

# get environment variables
config = Config(".env")
USE_ENV = config("USE_ENV", default="docker")

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
    NUMBER_TASKS = config("NUMBER_TASKS", default=100)
    NUMBER_USERS = config("NUMBER_USERS", default=100)

    # Application Configurations
    HOST_DOMAIN = config("HOST_DOMAIN", default="https://devsetgo.com")
    RELEASE_ENV = config("RELEASE_ENV", default="prd")
    SQLALCHEMY_DATABASE_URI = config(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///sqlite_db/api.db"
    )

    # Loguru settings
    LOGURU_RETENTION = config("LOGURU_RETENTION", default="10 days")
    LOGURU_ROTATION = config("LOGURU_ROTATION", default="10 MB")
    LOGURU_LOGGING_LEVEL = config("LOGURU_LOGGING_LEVEL", default="WARNING")
    # Access Token Settings
    SECRET_KEY = config("SECRET_KEY", default="secret-key-1234567890")
    ALGORITHM = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=10080)
    
else:
    logger.info(
        f"USE_ENV set to {USE_ENV}. Using os environmental settings for\
             external configuration"
    )
    # Application information
    APP_VERSION = os.environ["APP_VERSION"]
    OWNER = os.environ["OWNER"]
    WEBSITE = os.environ["WEBSITE"]
    LICENSE_TYPE = os.environ["LICENSE_TYPE"]
    LICENSE_LINK = os.environ["LICENSE_LINK"]

    # Demo Data
    CREATE_SAMPLE_DATA = os.environ["CREATE_SAMPLE_DATA"]
    NUMBER_TASKS = os.environ["NUMBER_TASKS"]
    NUMBER_USERS = os.environ["NUMBER_USERS"]

    # Application Configurations
    HOST_DOMAIN = os.environ["HOST_DOMAIN"]
    RELEASE_ENV = os.environ["RELEASE_ENV"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    # Loguru settings
    LOGURU_RETENTION = os.environ["LOGURU_RETENTION"]
    LOGURU_ROTATION = os.environ["LOGURU_ROTATION"]
    LOGURU_LOGGING_LEVEL = os.environ["LOGURU_LOGGING_LEVEL"]
    # Access Token Settings
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
