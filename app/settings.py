# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
import os
from starlette.config import Config

# get environment variables
config = Config(".env")

# Application information
APP_VERSION = config("APP_VERSION")
OWNER = config("OWNER")
WEBSITE = config("WEBSITE")
LICENSE_TYPE = config("LICENSE_TYPE")
LICENSE_LINK = config("LICENSE_LINK")

# Application Configurations
HOST_DOMAIN = config("HOST_DOMAIN")
RELEASE_ENV = config("RELEASE_ENV")
SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")

# Loguru settings
LOGURU_RETENTION = config("LOGURU_RETENTION")
LOGURU_ROTATION = config("LOGURU_ROTATION")

# Access Token Settings
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")
