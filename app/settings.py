# -*- coding: utf-8 -*-
"""Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""
import os
from dotenv import load_dotenv


load_dotenv()

# Environment settings
HOST_DOMAIN = os.getenv("HOST_DOMAIN")
RELEASE_ENV = os.getenv("RELEASE_ENV")
SECRET_KEY = os.getenv("SECRET_KEY")
# Database
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
# LOGURU settings
LOGURU_BACKTRACE = True
LOGURU_RETENTION = "10 days"
LOGURU_ROTATION = "100 MB"


# env settings from cookiecutter flask for ideas
# ENV = os.getenv('RELEASE_ENV')
# DEBUG = ENV == 'development'
# SQLALCHEMY_DATABASE_URI = os.getenv('RELEASE_ENV')
# SECRET_KEY = os.getenv('RELEASE_ENV')
# BCRYPT_LOG_ROUNDS = os.getenv('RELEASE_ENV')
# DEBUG_TB_ENABLED = DEBUG
# DEBUG_TB_INTERCEPT_REDIRECTS = False
# CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'
