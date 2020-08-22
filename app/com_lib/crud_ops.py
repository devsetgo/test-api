# -*- coding: utf-8 -*-
"""
database simple functions. Pass query and where needed values and get result back
"""


from loguru import logger

from com_lib.db_setup import database


async def fetch_one_db(query):
    try:
        result = await database.fetch_one(query)
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def fetch_all_db(query):
    try:
        result = await database.fetch_all(query)
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        return e


async def execute_one_db(query, values: dict = None):

    try:
        await database.execute(query, values)
        result = "complete"
        logger.debug(str(result))
        return result
    except Exception as e:
        logger.critical(f"error: {e}")
        logger.debug(query)
        logger.debug(values)
        return e


async def execute_many_db(query, values: dict):
    try:
        result = await database.execute_many(query, values)
        logger.debug(str(result))

    except Exception as e:
        logger.critical(f"error: {e}")
        logger.debug(query)
        logger.debug(values)
        return e
