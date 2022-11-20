# -*- coding: utf-8 -*-
"""
Crud functions to check if users, groups or ids exist for validation
"""

from loguru import logger
from sqlalchemy import and_

from core.db_setup import users
from crud.crud_ops import fetch_one_db, execute_one_db, fetch_all_db
from sqlalchemy import or_, and_

async def check_unique_contraints(email: str, user_name:str) -> bool:
    query = users.select().where(or_(users.c.email == email, users.c.user_name == user_name))
    result = await fetch_all_db(query=query)
    logger.error(result)
    if result is not None:
        logger.debug(f"existing email {email} and/or user_name{user_name}")
        return True
    else:
        logger.debug("no duplicate value")
        return False
