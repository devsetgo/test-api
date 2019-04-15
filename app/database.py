import logging
import os
from loguru import logger
from dotenv import load_dotenv
from sqlalchemy import create_engine
from endpoints.todo import model

load_dotenv()

release_env = os.getenv('RELEASE_ENV')
sqlachemy_database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

def create_database():
    engine = create_engine(sqlachemy_database_uri, echo=True)