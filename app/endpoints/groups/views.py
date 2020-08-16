# -*- coding: utf-8 -*-
"""
User routes to perform actions
list users
list user count
user create
user profile
user update profile
user password verify
user update password
user delete
user deactivate
user unlock

"""
import asyncio
import uuid
from datetime import datetime
from fastapi import APIRouter, Form, Path, Query, status
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import run_endpoint_function
from loguru import logger
from sqlalchemy.sql.expression import false

from com_lib.crud_ops import fetch_one_db, fetch_all_db, execute_one_db, execute_many_db
from com_lib.db_setup import database, groups, groups_item
from com_lib.pass_lib import encrypt_pass, verify_pass
from com_lib.simple_functions import get_current_datetime
from endpoints.groups.models import GroupCreate, GroupsBase, GroupItemBase, GroupsOut,GroupTypeEnum

router = APIRouter()

title = "Delay in Seconds"


@router.get("/list", tags=["groups"])
async def group_list(
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
    group_type: GroupTypeEnum = Query(
        None, title="groupType", description="Type of group",alias="groupType"
    ),
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
    criteria = []
    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if is_active is not None:
        criteria.append((groups.c.is_active, is_active))

    query = groups.select().order_by(groups.c.date_create).limit(qty).offset(offset)
    count_query = groups.select().order_by(groups.c.date_create)

    for crit in criteria:
        col, val = crit
        query = query.where(col == val)
        count_query = count_query.where(col == val)

    db_result = await database.fetch_all(query)
    total_count = await database.fetch_all(count_query)

    # result_set = []
    # for r in db_result:
    #     # iterate through data and return simplified data set
    #     user_data = {
    #         "user_id": r["user_id"],
    #         "user_name": r["user_name"],
    #         "first_name": r["first_name"],
    #         "last_name": r["last_name"],
    #         "company": r["company"],
    #         "title": r["title"],
    #         "city": r["city"],
    #         "country": r["country"],
    #         "postal": r["postal"],
    #         "is_active": r["is_active"],
    #     }
    #     result_set.append(user_data)

    result = {
        "parameters": {
            "returned_results": len(db_result),
            "qty": qty,
            "total_count": len(total_count),
            "offset": offset,
            "filter": is_active,
            "delay": delay,
        },
        "groups": db_result,
    }
    return result


@router.post(
    "/create/",
    tags=["users"],
    response_description="The created item",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        # 302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        # 404: {"description": "Operation forbidden"},
        # 405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def create_group(
    *,
    group: GroupCreate,
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:
    """
    POST/Create a new User. user_name (unique), firstName, lastName,
    and password are required. All other fields are optional.

    Arguments:
        user {UserCreate} -- [description]

    Keyword Arguments:
        delay {int} -- [description] 0 seconds default, maximum is 122

    Returns:
        dict -- [user_id: uuid, user_name: user_name]
    """

    # sleep if delay option is used
    if delay is not None:
        logger.info(f"adding a delay of {delay} seconds")
        await asyncio.sleep(delay)

    # approval or notification
    if group.group_type != "approval" or group.group_type != "notification":
        error: dict = {"error":f"Group Type '{group.name}' is not 'approval' or 'notification'"}
        logger.warning(error)
        return JSONResponse(status_code=400, content=error)
        b
    check_name = str(group.name)
    duplicate = await check_unique(check_name)

    try:
        if duplicate == False:
            error: dict = {"error":f"Group Name '{group.name}' is a duplicate"}
            logger.warning(error)
            return JSONResponse(status_code=400, content=error)
            

        group_id = uuid.uuid4()
        group_data = {
            "id": str(group_id),
            "name": group.name,
            "is_active": group.is_active,
            "description": group.description,
            "group_type": group.group_type,
            "date_create": datetime.now(),
            "date_update": datetime.now(),
        }
        logger.debug(group_data)
        # create group
        query = groups.insert()
        group_result = await execute_one_db(query=query, values=group_data)

        if "error" in group_result:
            error:dict = group_result
            logger.critical(error)
            return JSONResponse(status_code=400, content=error)

        # data result
        full_result: dict = {"id": str(group_id), "data": group_result}
        logger.debug(full_result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=full_result)
    except Exception as e:
        error: dict = {"error": str(e)}
        logger.debug(e)
        logger.critical(type(e))
        logger.critical(f"Critical Error: {e}")
        return JSONResponse(status_code=400, content=error)
    except ValueError as e:
        error: dict = {"error": e}
        logger.debug(e)
        logger.critical(type(e))
        logger.critical(f"Critical Error: {e}")
        return JSONResponse(status_code=400, content=error)


async def check_unique(name: str) -> bool:
    query = groups.select().where(groups.c.name == name)
    result = await fetch_one_db(query=query)
    logger.debug(result)
    if result is not None:
        logger.debug("duplicate value")
        return False
    else:
        logger.debug("no duplicate value")
        return True
    # return False
