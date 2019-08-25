# -*- coding: utf-8 -*-
"""
doc string
"""
import asyncio
import os
import random
import uuid
from datetime import date, datetime, time, timedelta

import databases
from pydantic import BaseModel, Schema, Json, UUID1, SecretStr
from fastapi import APIRouter, FastAPI, Header, HTTPException, Path, Query, Form
from loguru import logger

from db_setup import database, users
from endpoints.users.models import (
    UserCreate,  # , UserUpdate,User, UserInDB
    UserDeactivate,
    UserList,
    UserPwd,
    UserUpdate,
)
from endpoints.users.pass_lib import encrypt_pass, verify_pass
from settings import SQLALCHEMY_DATABASE_URI

router = APIRouter()
# time variables
currentTime = datetime.now()


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
        None,
        title="Offset",
        description="Offset increment",
        ge=1,
        le=500,
        alias="offset",
    ),
    isActive: bool = Query(None, title="by active status", alias="active"),
):
    """
    docstring
    """
    # sleep if delay option is used
    if delay is None:
        delay == 0

    asyncio.sleep(delay)

    if qty is None:
        qty: int = 100
    if offset is None:
        offset: int = 0

    try:
        # await database.connect()
        # Fetch multiple rows
        if isActive is not None:
            query = (
                users.select()
                .where(users.c.isActive == isActive)
                .order_by(users.c.dateCreate)
                .limit(qty)
            )
            # values = {'isActive': isActive}
            db_result = await database.fetch_all(query)
        else:
            query = users.select().order_by(users.c.dateCreate).limit(qty)
            db_result = await database.fetch_all(query)

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
                "quantity": qty,
                "filter": isActive,
                "delay": delay,
            },
            "users": result_set,
        }
        # await database.disconnect()
        return result
    except Exception as e:
        # print(e)
        logger.error(f"Error: {e}")
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
        # print(e)
        logger.error(f"Error: {e}")
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
        le=121,
        alias="delay",
    ),
):

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
        # print(e)
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
        logger.error(f"Error: {e}")

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
        logger.error(f"Error: {e}")

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
    hash_pwd = encrypt_pass(value["password"])
    # print(value)
    # dictionary to append to todo_full_list
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
        result = {"userId": userInformation["userId"], "user_name": value["user_name"]}
    except Exception as e:
        print(e)
        logger.error(f"Error: {e}")
        result = {"error": e}

    return result


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
async def check_pwd(user_name: str = Form(...), password: str = Form(...)):
    try:
        # Fetch single row
        query = users.select().where(users.c.user_name == user_name)
        db_result = await database.fetch_one(query)
        # print(user_data)
        result = verify_pass(password, db_result["password"])
        # print(db_result['user_name'],db_result['password'])
        return {"result": result}

    except Exception as e:
        # print(e)
        logger.error(f"Error: {e}")
