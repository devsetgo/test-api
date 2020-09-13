# -*- coding: utf-8 -*-
import random
import secrets
import time
import uuid
from datetime import datetime, timedelta

import silly
from loguru import logger
from unsync import unsync

from com_lib.db_setup import database, groups, groups_item, todos, users
from endpoints.sillyusers.gen_user import user_test_info
from settings import NUMBER_GROUPS, NUMBER_TASKS, NUMBER_USERS

number_of_tasks = NUMBER_TASKS
number_of_users = NUMBER_USERS
number_of_groups = NUMBER_GROUPS
# time variables
currentTime = datetime.now()


def create_data():
    logger.warning("DEMO Data Initialization is TRUE")
    logger.info("Starting process demo data")
    user_count = count_users().result()
    task_count = count_tasks().result()
    group_count = count_groups().result()

    if int(user_count) == 0:
        create_users(int(number_of_users))
        time.sleep(1)
    else:
        logger.info("existing data, sample users will not be created")

    if int(task_count) == 0:
        create_tasks(int(number_of_tasks))
        time.sleep(1)
    else:
        logger.info("existing data, sample tasks will not be created")

    if int(group_count) == 0:
        create_groups(int(number_of_groups))
        time.sleep(1)
    else:
        logger.info("existing data, sample groups will not be created")
        logger.warning("DEMO DATA INITIALIZATION IS TRUE")


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

    g_count = 0
    for _ in range(0, qty):
        group_information = {
            "id": str(uuid.uuid4()),
            "name": f"test{g_count}",
            "is_active": random.choice([True, False]),
            "description": "This is a test",
            "group_type": random.choice(["approval", "notification"]),
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        }
        db_group_call(group_information)
        g_count += 1


def group_user_creator():
    group_information = {
        "id": str(uuid.uuid4()),
        "user": f"test{secrets.token_hex(4)}",
    }
    db_group_user_call(group_information)


def group_creator():
    group_information = {
        "id": str(uuid.uuid4()),
        "name": f"test{secrets.token_hex(4)}",
        "is_active": random.choice([True, False]),
        "description": "This is a test",
        "group_type": random.choice(["approval", "notification"]),
        "date_create": datetime.now(),
        "date_update": datetime.now(),
    }
    db_group_call(group_information)


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
        logger.critical(f"Critical Error: {e}")


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


@unsync
async def db_group_call(group_information: dict):
    try:
        query = groups.insert()
        values = group_information
        await database.execute(query, values)
        result = {"id": group_information["id"]}
        logger.info(f"db group call: {result}")
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")


@unsync
async def db_group_user_call(group_user_information: dict):
    try:
        query = groups_item.insert()
        values = group_user_information
        await database.execute(query, values)
        result = {"todo_id": group_user_information["id"]}
        logger.info(f"db group user call: {result}")
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")
