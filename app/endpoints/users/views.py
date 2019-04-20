# FastAPI and Starlette libraries
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header

# from starlette.responses import response_description

# application libraries
from endpoints.users.models import (
    UserCreate,
    UserUpdate,
    UserDeactivate,
)  # , UserUpdate,User, UserInDB
from db_setup import users, database
from settings import SQLALCHEMY_DATABASE_URI

# Python libraries
import asyncio
import random
import uuid
import os
from datetime import datetime, date, timedelta, time

# External Library imports
import databases

# from databases import Database
from loguru import logger


# database = databases.Database(SQLALCHEMY_DATABASE_URI)
# database = databases.Database(SQLALCHEMY_DATABASE_URI)

router = APIRouter()
# time variables
currentTime = datetime.now()


@router.get("/list", tags=["users"])
async def user_list(
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
    isActive: bool = Query(None, title="by active status", alias="active"),
):

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # await database.connect()
        # Fetch multiple rows
        if isActive is not None:
            query = users.select().where(users.c.isActive == isActive)
            # values = {'isActive': isActive}
            x = await database.fetch_all(query)
        else:
            query = users.select()
            x = await database.fetch_all(query)

        result = x
        # await database.disconnect()
    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}
    return result


@router.get(
    "/list/count",
    tags=["users"],
    response_description="Get count of users",
    responses={
        404: {"description": "Operation forbidden"},
        500: {"description": "Mommy!"},
    },
)
async def users_list_count(
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
    isActive: bool = Query(None, title="by active status", alias="active"),
):

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)
    try:
        # Fetch multiple rows
        if isActive is not None:
            query = users.select().where(users.c.isActive == isActive)
            x = await database.fetch_all(query)
        else:
            query = users.select()
            x = await database.fetch_all(query)

        result = {"count": len(x)}
    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}

    # print(result)
    return result


@router.get("/{userId}", tags=["users"], response_description="Get user information")
async def get_user_id(
    userId: str = Path(..., title="The user id to be searched for", alias="userId"),
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
):

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # Fetch single row
        query = users.select().where(users.c.userId == userId)
        result = await database.fetch_one(query)
    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)

    return result


@router.put(
    "/deactivate/{userId}",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivatee_user_id(
    *,
    userId: str = Path(..., title="The user id to be searched for", alias="userId"),
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
):

    userInformation = {"isActive": False}
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # Fetch single row
        query = users.update().where(users.c.userId == userId)
        values = userInformation
        result = await database.execute(query, values)

    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)

    return result


@router.delete(
    "/{userId}",
    tags=["users"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_user_id(
    *, userId: str = Path(..., title="The user id to be searched for", alias="userId")
):

    try:
        # delete id
        query = users.delete().where(users.c.userId == userId)
        await database.execute(query)
        result = {"status": f"{userId} deleted"}
    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)

    return result


@router.post(
    "/create/",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def create_user(
    *,
    user: UserCreate,
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
):
    value = user.dict()
    # print(value)
    # dictionary to append to todo_full_list
    userInformation = {
        "userId": str(uuid.uuid1()),
        "firstName": value["firstName"],
        "lastName": value["lastName"],
        "password": value["password"],
        "title": value["title"],
        "company": value["company"],
        "address": value["address"],
        "city": value["city"],
        "country": value["country"],
        "postal": value["postal"],
        "email": value["email"],
        "website": value["website"],
        "description": value["description"],
        "dateCreate": currentTime,
        "isActive": True,
        "isSuperuser": False,
    }

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        query = users.insert()
        values = userInformation
        await database.execute(query, values)
        result = {"userId": userInformation["userId"]}
    except Exception as e:
        print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}

    return result
