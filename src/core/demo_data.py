# -*- coding: utf-8 -*-
import random
import secrets
import time
import uuid
from datetime import datetime, timedelta

import silly
from loguru import logger
from unsync import unsync

from core.db_setup import database, groups, groups_item, todos, users
from core.gen_user import user_test_info
from settings import config_settings

# time variables
currentTime = datetime.now()


def create_data():
    logger.warning("DEMO Data Initialization is TRUE")
    logger.info("Starting process demo data")
    user_count = count_users().result()
    task_count = count_tasks().result()
    group_count = count_groups().result()

    if int(user_count) == 0:
        create_users(config_settings.number_users)
        time.sleep(1)
    else:
        logger.info("existing data, sample users will not be created")

    if int(task_count) == 0:
        create_tasks(int(config_settings.number_tasks))
        time.sleep(1)
    else:
        logger.info("existing data, sample tasks will not be created")

    if int(group_count) == 0:
        create_groups(int(config_settings.number_groups))
        time.sleep(1)
        create_standard_groups()
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
        time.sleep(0.05)
        new_user = user_test_info()
        db_user_call(new_user)


def create_groups(qty: int):

    for _ in range(0, qty):
        time.sleep(0.05)
        id: str = str(uuid.uuid4())
        group_information = {
            "id": id,
            "name": f"test{secrets.token_hex(2)}",
            "is_active": random.choice([True, False]),
            "description": "This is a test",
            "group_type": random.choice(["approval", "notification"]),
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        }
        db_group_call(group_information)
        time.sleep(0.01)

        for _ in range(random.randint(2, 10)):
            time.sleep(0.05)
            group_user_creator(group_id=id)


def group_user_creator(group_id: str):
    group_information = {
        "id": str(uuid.uuid4()),
        "group_id": group_id,
        "user": f"test{secrets.token_hex(4)}",
        "date_create": datetime.now(),
    }
    db_group_user_call(group_information)


_GROUP_DESCRIPTION: str = "This is an example group"


def create_standard_groups():
    groups: list = [
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup1",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup2",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup3",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup4",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup5",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
        {
            "id": str(uuid.uuid4()),
            "name": "approvalgroup6",
            "is_active": True,
            "description": _GROUP_DESCRIPTION,
            "group_type": "approval",
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        },
    ]
    users: list = [
        "Jerry",
        "Sarah",
        "Juan",
        "Jack",
        "Angela",
        "Jesse",
        "Beverly",
        "Linda",
        "Jason",
        "Jordan",
        "Ethan",
        "Karen",
        "Jennifer",
        "Sean",
        "Joseph",
        "Kimberly",
        "Samuel",
        "Dorothy",
        "Raymond",
        "Olivia",
        "Carolyn",
        "Cheryl",
        "Jeffrey",
        "Rachel",
        "Judy",
        "Larry",
        "Zachary",
        "Pamela",
        "Walter",
        "Deborah",
        "Billy",
        "Kevin",
        "Katherine",
        "Kenneth",
        "Janice",
        "Roy",
        "Kathleen",
        "Nancy",
        "Eugene",
        "Daniel",
        "Marie",
        "Gabriel",
        "Diana",
        "Jonathan",
        "Dennis",
        "Emma",
        "Laura",
        "Rose",
        "Patrick",
        "Scott",
        "Sandra",
        "Gregory",
        "Thomas",
        "Roger",
        "Helen",
        "Debra",
        "Jessica",
        "Bobby",
        "Lawrence",
        "Joshua",
        "Natalie",
        "Matthew",
        "George",
        "Austin",
        "Ryan",
        "Julie",
        "Barbara",
        "Benjamin",
        "Theresa",
        "Harold",
        "Richard",
        "Alexander",
        "Joyce",
        "Danielle",
        "Anthony",
        "Ashley",
        "Ronald",
        "Stephen",
        "Mary",
        "Adam",
        "Johnny",
        "Lisa",
        "Nicholas",
        "Dylan",
        "Nathan",
        "William",
        "Steven",
        "Brandon",
        "Charlotte",
        "Jean",
        "Heather",
        "Brittany",
        "Gloria",
        "Amanda",
        "Teresa",
        "Judith",
        "Logan",
        "Shirley",
        "Philip",
        "Jose",
        "Nicole",
        "Noah",
        "Randy",
        "Vincent",
        "Amber",
        "Sara",
        "Michelle",
        "Gary",
        "Cynthia",
        "Arthur",
        "Paul",
        "James",
        "Tyler",
        "Henry",
        "Bruce",
        "Denise",
        "Doris",
        "Christina",
        "Julia",
        "Amy",
        "Joan",
        "Madison",
        "David",
        "Melissa",
        "Albert",
        "Brenda",
        "Eric",
        "Robert",
        "Russell",
        "Alan",
        "Timothy",
        "Isabella",
        "Charles",
        "Victoria",
        "Maria",
        "Willie",
        "Stephanie",
        "John",
        "Louis",
        "Mark",
        "Donna",
        "Gerald",
        "Catherine",
        "Anna",
        "Peter",
        "Marilyn",
        "Sophia",
        "Kayla",
        "Martha",
        "Justin",
        "Joe",
        "Abigail",
        "Alice",
        "Frank",
        "Rebecca",
        "Betty",
        "Andrea",
        "Aaron",
        "Virginia",
        "Wayne",
        "Ralph",
        "Ruth",
        "Alexis",
        "Douglas",
        "Jacqueline",
        "Christopher",
        "Carl",
        "Lauren",
        "Bryan",
        "Christine",
        "Ann",
        "Elizabeth",
        "Frances",
        "Evelyn",
        "Bradley",
        "Brian",
        "Jeremy",
        "Sharon",
        "Diane",
        "Margaret",
        "Hannah",
        "Keith",
        "Carol",
        "Jacob",
        "Kyle",
        "Christian",
        "Emily",
        "Kathryn",
        "Edward",
        "Terry",
        "Michael",
        "Megan",
        "Kelly",
        "Patricia",
        "Samantha",
        "Janet",
        "Grace",
        "Andrew",
        "Susan",
        "Donald",
    ]
    for g in groups:
        time.sleep(0.01)
        db_group_call(g)
        time.sleep(0.01)
        for _ in range(random.randint(1, 5)):
            create_standard_group_user(
                group_id=g["id"], name=users[random.randint(0, len(users) - 1)]
            )


def create_standard_group_user(group_id: str, name: str):
    group_information = {
        "id": str(uuid.uuid4()),
        "group_id": group_id,
        "user": name,
        "date_create": datetime.now(),
    }
    db_group_user_call(group_information)


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
