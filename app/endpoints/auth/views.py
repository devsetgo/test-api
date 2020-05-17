# -*- coding: utf-8 -*-
"""
Auth routes to perform actions
auth users


"""
import asyncio
import uuid

from fastapi import APIRouter, Form, Path, Query
from loguru import logger

from com_lib.pass_lib import encrypt_pass, verify_pass
from com_lib.simple_functions import get_current_datetime
from db_setup import database, users

router = APIRouter()


@router.get("/list", tags=["users"])
async def user_list(
    delay: int = Query(
        None,
        title=title,
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
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:

    """
    list of users

    Keyword Arguments:
        delay {int} -- [description] 0 seconds default, maximum is 122
        qty {int} -- [description] 100 returned results is default,
        maximum is 500
        offset {int} -- [description] 0 seconds default
        Active {bool} -- [description] no default as not required,
        must be Active=true or false if used

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
    if is_active is not None:
        query = (
            users.select()
            .where(users.c.is_active == is_active)
            .order_by(users.c.date_create)
            .limit(qty)
            .offset(offset)
        )
        db_result = await database.fetch_all(query)

        count_query = (
            users.select()
            .where(users.c.is_active == is_active)
            .order_by(users.c.date_create)
        )
        total_count = await database.fetch_all(count_query)

    else:

        query = users.select().order_by(users.c.date_create).limit(qty).offset(offset)
        db_result = await database.fetch_all(query)
        count_query = users.select().order_by(users.c.date_create)
        total_count = await database.fetch_all(count_query)

    result_set = []
    for r in db_result:
        # iterate through data and return simplified data set
        user_data = {
            "user_id": r["user_id"],
            "user_name": r["user_name"],
            "first_name": r["first_name"],
            "last_name": r["last_name"],
            "company": r["company"],
            "title": r["title"],
            "is_active": r["is_active"],
        }
        result_set.append(user_data)

    result = {
        "parameters": {
            "returned_results": len(result_set),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter": is_active,
            "delay": delay,
        },
        "users": result_set,
    }
    return result
