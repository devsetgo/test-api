# -*- coding: utf-8 -*-
"""
doc string
"""
import asyncio
import os
import random
import uuid
from datetime import date, datetime, time, timedelta
from typing import Dict

import databases
from fastapi import APIRouter, FastAPI, Form, Header, HTTPException, Path, Query
from loguru import logger
from pydantic import UUID1, BaseModel, Json, Schema, SecretStr

from com_lib.pass_lib import encrypt_pass, verify_pass
from com_lib.simple_functions import get_current_datetime
from db_setup import database, users
from endpoints.users.models import UserCreate  # , UserUpdate,User, UserInDB
from endpoints.users.models import UserDeactivate, UserList, UserPwd, UserUpdate

router = APIRouter()


@router.get("/list", tags=["users"])
async def user_list(
    delay: int = Query(
        None,
        title="Delay",
        description="Seconds to delay (max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
    qty: int = Query(
        None,
        title="Quanity",
        description="Records to return (max 500)",
        ge=1,
        le=500,
        alias="qty",
    ),
    offset: int = Query(
        None, title="Offset", description="Offset increment", ge=0, alias="offset"
    ),
    isActive: bool = Query(None, title="by active status", alias="active"),
) -> dict:

    """
    list of users

    Keyword Arguments:
        delay {int} -- [description] 0 seconds default, maximum is 122
        qty {int} -- [description] 100 returned results is default, maximum is 500
        offset {int} -- [description] 0 seconds default
        isActive {bool} -- [description] no default as not required, must be isActive=true or false if used

    Returns:
        dict -- [description]
    """
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    # Fetch multiple rows
    if isActive is not None:
        query = (
            users.select()
            .where(users.c.isActive == isActive)
            .order_by(users.c.dateCreate)
            .limit(qty)
            .offset(offset)
        )
        # values = {'isActive': isActive}
        db_result = await database.fetch_all(query)

        count_query = (
            users.select()
            .where(users.c.isActive == isActive)
            .order_by(users.c.dateCreate)
        )
        total_count = await database.fetch_all(count_query)

    else:

        query = users.select().order_by(users.c.dateCreate).limit(qty).offset(offset)
        db_result = await database.fetch_all(query)
        count_query = users.select().order_by(users.c.dateCreate)
        total_count = await database.fetch_all(count_query)

    result_set = []
    for r in db_result:
        # iterate through data and return simplified data set
        user_data = {
            "userId": r["userId"],
            "user_name": r["user_name"],
            "firstName": r["firstName"],
            "lastName": r["lastName"],
            "company": r["company"],
            "title": r["title"],
            "isActive": r["isActive"],
        }
        result_set.append(user_data)

    result = {
        "parameters": {
            "returned_results": len(result_set),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter": isActive,
            "delay": delay,
        },
        "users": result_set,
    }
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
) -> dict:
    """
    Count of users in the database

    Keyword Arguments:
        delay {int} -- [description] 0 seconds default, maximum is 122
        isActive {bool} -- [description] no default as not required, must be isActive=true or false if used

    Returns:
        dict -- [description]
    """
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
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


@router.get("/{userId}", tags=["users"], response_description="Get user information")
async def get_user_id(
    userId: str = Path(..., title="The user id to be searched for", alias="userId"),
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=121,
        alias="delay",
    ),
) -> dict:
    """
    User information for requested UUID

    Keyword Arguments:
        userId {str} -- [description] UUID of userId property required
        delay {int} -- [description] 0 seconds default, maximum is 122


    Returns:
        dict -- [description]
    """
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # Fetch single row
        query = users.select().where(users.c.userId == userId)
        db_result = await database.fetch_one(query)

        user_data = {
            "userId": db_result["userId"],
            "user_name": db_result["user_name"],
            "firstName": db_result["firstName"],
            "lastName": db_result["lastName"],
            "company": db_result["company"],
            "title": db_result["title"],
            "address": db_result["address"],
            "city": db_result["city"],
            "country": db_result["country"],
            "postal": db_result["postal"],
            "email": db_result["email"],
            "website": db_result["website"],
            "description": db_result["description"],
            "dateCreate": db_result["dateCreate"],
            "isActive": db_result["isActive"],
        }
        return user_data

    except Exception as e:
        logger.error(f"Error: {e}")


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
) -> dict:
    """
    Deactivate a specific user UUID

    Keyword Arguments:
        userId {str} -- [description] UUID of userId property required
        delay {int} -- [description] 0 seconds default, maximum is 122

    Returns:
        dict -- [description]
    """
    userInformation = {"isActive": False}
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # Fetch single row
        query = users.update().where(users.c.userId == userId)
        values = userInformation
        result = await database.execute(query, values)
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


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
) -> dict:
    """
    Delete a user by UUID

    Keyword Arguments:
        userId {str} -- [description] UUID of userId property required

    Returns:
        dict -- [result: user UUID deleted]
    """
    try:
        # delete id
        query = users.delete().where(users.c.userId == userId)
        await database.execute(query)
        result = {"status": f"{userId} deleted"}
        return result

    except Exception as e:
        logger.error(f"Error: {e}")


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
) -> dict:
    """
    POST/Create a new User. user_name (unique), firstName, lastName, and password are required. All other fields are optional.

    Arguments:
        user {UserCreate} -- [description]

    Keyword Arguments:
        delay {int} -- [description] 0 seconds default, maximum is 122

    Returns:
        dict -- [userId: uuid, user_name: user_name]
    """
    value = user.dict()
    hash_pwd = encrypt_pass(value["password"])

    userInformation = {
        "userId": str(uuid.uuid1()),
        "user_name": value["user_name"].lower(),
        "firstName": value["firstName"],
        "lastName": value["lastName"],
        "password": hash_pwd,
        "title": value["title"],
        "company": value["company"],
        "address": value["address"],
        "city": value["city"],
        "country": value["country"],
        "postal": value["postal"],
        "email": value["email"],
        "website": value["website"],
        "description": value["description"],
        "dateCreate": get_current_datetime(),
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

        result = {"userId": userInformation["userId"], "user_name": value["user_name"]}
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


@router.post(
    "/check-pwd/",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def check_pwd(user_name: str = Form(...), password: str = Form(...)) -> dict:
    """
        Check password function

        Keyword Arguments:
            user_name {str} -- [description] existing user_name required
            password {str} -- [description] password required

        Returns:
            [Dict] -- [result: bool]
    """
    try:
        # Fetch single row
        query = users.select().where(users.c.user_name == user_name.lower())
        db_result = await database.fetch_one(query)
        result = verify_pass(password, db_result["password"])
        logger.info(f"password validation: user: {user_name.lower()} as {result}")
        return {"result": result}

    except Exception as e:
        logger.error(f"Error: {e}")
