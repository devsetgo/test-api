# -*- coding: utf-8 -*-
"""
Crud functions to check if users, groups or ids exist for validation
"""

from loguru import logger
from sqlalchemy import and_

from core.db_setup import groups, groups_item
from crud.crud_ops import fetch_one_db, execute_one_db


async def check_unique_name(name: str) -> bool:
    query = groups.select().where(groups.c.name == name)
    result = await fetch_one_db(query=query)
    logger.debug(result)
    if result is not None:
        logger.debug(f"existing name {name}")
        return False
    else:
        logger.debug("no duplicate value")
        return True


async def check_id_exists(id: str) -> bool:
    query = groups.select().where(groups.c.id == id)
    result = await fetch_one_db(query=query)
    logger.debug(result)
    if result is None:
        logger.warning(f"Group ID: {id} does not exists")
        return False
    else:
        logger.info(f"Group ID: {id} found")
        return True


async def check_user_exists(group_id: str, user: str) -> bool:
    query = groups_item.select().where(
        and_(groups_item.c.user == user, groups_item.c.group_id == group_id)
    )
    result = await fetch_one_db(query=query)
    logger.debug(result)
    if result is not None:
        logger.warning(f"User: {user} exist in group")
        return True
    else:
        logger.debug(f"ID: {user} not in group")
        return False


async def check_user_id_exists(group_id: str, id: str) -> bool:
    query = groups_item.select().where(
        groups_item.c.id == id, groups_item.c.group_id == group_id
    )
    result = await fetch_one_db(query=query)
    logger.warning(result)
    if result is None:
        logger.warning(f"Group ID: {group_id} and/or User ID: {id} does not exists")
        return False
    else:
        logger.info(f"Group ID: {group_id} and/or User ID: {id} exists")
        return True


async def delete_user_in_group(group_id: str, id: str) -> bool:
    query = groups_item.delete().where(
        groups_item.c.id == id, groups_item.c.group_id == group_id
    )
    await execute_one_db(query)
    result = await check_user_id_exists(group_id=group_id, id=id)

    if result == False:
        return {
            "message": f"User ID: {id} in Group ID: {group_id} has NOT been removed",
            "status": False,
        }
    elif result == True:
        return {
            "message": f"User ID: {id} in Group ID: {group_id} has been removed",
            "status": False,
        }
    else:
        return {
            "message": f"User ID: {id} in Group ID: {group_id} has resulted in an Error",
            "status": None,
        }
