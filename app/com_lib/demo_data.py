# -*- coding: utf-8 -*-
import random
import time
import uuid
from datetime import datetime, timedelta

import silly
from loguru import logger
from unsync import unsync

from com_lib.db_setup import database, todos, users, groups, groups_item
from endpoints.sillyusers.gen_user import user_test_info
from settings import NUMBER_TASKS, NUMBER_USERS, NUMBER_GROUPS

number_of_tasks = NUMBER_TASKS
number_of_users = NUMBER_USERS
number_of_groups = NUMBER_GROUPS
# time variables
currentTime = datetime.now()


def create_data():

    logger.info(f"creating demo data")
    user_count = count_users().result()
    task_count = count_tasks().result()
    group_count = count_groups().result()

    if int(user_count) == 0:
        create_users(int(number_of_users))
    else:
        logger.info(f"existing data, sample users will not be created")

    if int(task_count) == 0:
        create_tasks(int(number_of_tasks))
    else:
        logger.info(f"existing data, sample tasks will not be created")

    if int(group_count) == 0:
        create_users(int(number_of_users))
    else:
        logger.info(f"existing data, sample users will not be created")


@unsync
async def count_groups():
    query = groups.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of users in DB: {result}")
    return result


@unsync
async def count_users():
    query = users.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of users in DB: {result}")
    return result


@unsync
async def count_tasks():
    query = todos.select()
    count = await database.fetch_all(query)

    result = len(count)
    logger.info(f"number of tasks in DB: {result}")
    return result


def create_users(qty: int):

    for _ in range(0, qty):
        time.sleep(0.01)
        new_user = user_test_info()
        db_user_call(new_user)


def create_groups(qty: int):

    for _ in range(0, qty):
        time.sleep(0.01)
        new_user = user_test_info()
        db_user_call(new_user)


def create_tasks(qty: int):

    for _ in range(0, qty):
        time.sleep(0.01)
        todo_information = {
            "todo_id": str(uuid.uuid1()),
            "title": silly.thing(),
            "description": silly.sentence(),
            "date_due": currentTime + timedelta(days=random.randint(1, 180)),
            "is_complete": bool(random.getrandbits(1)),
            "date_create": currentTime,
            "date_update": currentTime,
            "user_id": str(uuid.uuid4()),
            "date_complete": None,
        }

        db_todo_call(todo_information)


@unsync
async def db_user_call(new_user: dict):
    try:
        query = users.insert()
        values = new_user
        await database.execute(query, values)

        result = {
            "user_id": new_user["user_id"],
        }
        logger.info(f"db user call: {result}")
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@unsync
async def db_todo_call(todo_information: dict):
    try:
        query = todos.insert()
        values = todo_information
        await database.execute(query, values)
        result = {"todo_id": todo_information["todo_id"]}
        logger.info(f"db todo call: {result}")
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")
