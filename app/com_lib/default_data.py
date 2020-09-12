# -*- coding: utf-8 -*-
"""
Default data for api
"""
import time
import uuid
from datetime import datetime

from fastapi import APIRouter
from loguru import logger

from com_lib.crud_ops import execute_one_db
from com_lib.db_setup import groups, groups_item
from endpoints.groups.validation import check_unique_name

router = APIRouter()

title = "Delay in Seconds"


async def add_default_group(add_default: str):
    # check if default is true
    if add_default == "True":
        # check if default exists
        default_exists = await check_unique_name(name="default")
        # if does not exist
        if default_exists is True:

            group_id = uuid.uuid4()
            group_data = {
                "id": str(group_id),
                "name": "default",
                "is_active": True,
                "description": "Default group",
                "group_type": "approval",
                "date_create": datetime.now(),
                "date_update": datetime.now(),
            }
            logger.warning(f"Creating default group {group_data}")
            # create group
            query = groups.insert()
            group_result = await execute_one_db(query=query, values=group_data)
            logger.debug(group_result)
            time.sleep(0.1)
            user_id = str(uuid.uuid4())
            user_data = {"id": user_id, "user": "admin", "group_id": str(group_id)}
            logger.warning(f"Creating default group {user_data}")
            # create group
            query = groups_item.insert()
            group_result = await execute_one_db(query=query, values=user_data)
            logger.debug(group_result)
    return "complete"
