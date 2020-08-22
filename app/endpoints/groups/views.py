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

from fastapi import APIRouter
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from loguru import logger

from com_lib.crud_ops import execute_one_db
from com_lib.crud_ops import fetch_all_db
from com_lib.db_setup import database
from com_lib.db_setup import groups
from com_lib.db_setup import groups_item
from endpoints.groups.models import GroupCreate
from endpoints.groups.models import GroupDeactivate
from endpoints.groups.models import GroupItemDelete
from endpoints.groups.models import GroupTypeEnum
from endpoints.groups.models import GroupUser
from endpoints.groups.validation import check_id_exists
from endpoints.groups.validation import check_unique_name
from endpoints.groups.validation import check_user_exists
from endpoints.groups.validation import check_user_id_exists

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
        None, title="groupType", description="Type of group", alias="groupType"
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
    count_query = groups.select()

    for crit in criteria:
        col, val = crit
        query = query.where(col == val)
        count_query = count_query.where(col == val)

    db_result = await database.fetch_all(query)
    total_count = await database.fetch_all(count_query)

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


@router.put(
    "/deactivate",
    tags=["groups"],
    response_description="The created item",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        # 302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Not Found"},
        # 405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def deactivate_group(
    *,
    group: GroupDeactivate,
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

    id_exists = await check_id_exists(group.id)

    if id_exists == False:
        error: dict = {"error": f"Group ID: '{group.id}' not found"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)
    try:

        group_data = {
            # "id": group.id,
            "is_active": group.is_active,
            "date_update": datetime.now(),
        }
        logger.debug(group_data)
        # create group
        query = groups.update().where(groups.c.id == group.id)
        group_result = await execute_one_db(query=query, values=group_data)

        if "error" in group_result:
            error: dict = group_result
            logger.critical(error)
            return JSONResponse(status_code=400, content=error)

        # data result
        full_result: dict = {"id": group.id, "status": group_result}
        logger.debug(full_result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=full_result)
    except Exception as e:
        error: dict = {"error": str(e)}
        logger.debug(e)
        logger.critical(type(e))
        logger.critical(f"Critical Error: {e}")
        return JSONResponse(status_code=400, content=error)


@router.post(
    "/create",
    tags=["groups"],
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
    group_type_check: list = ["approval", "notification"]
    if group.group_type not in group_type_check:
        error: dict = {
            "error": f"Group Type '{group.group_type}' is not 'approval' or 'notification'"
        }
        logger.warning(error)
        return JSONResponse(status_code=400, content=error)
        
    check_name = str(group.name)
    duplicate = await check_unique_name(check_name)

    try:
        if duplicate == False:
            error: dict = {"error": f"Group Name '{group.name}' is a duplicate"}
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
            error: dict = group_result
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


@router.get("/group/{group_id}", tags=["groups"])
async def group_list(
    group_id: str,
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=121,
        alias="delay",
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

    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)
    # check if ID exists
    id_exists = await check_id_exists(group_id)
    if id_exists == False:
        error: dict = {"error": f"Group ID: '{group_id}' not found"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)
    query = groups_item.select().where(groups_item.c.group_id == group_id)
    db_result = await fetch_all_db(query=query)

    users_list: list = []
    for r in db_result:
        logger.debug(r)
        user_data: dict = {"id": r["id"], "user": r["user"]}
        users_list.append(user_data)
    result = {"group_id": group_id, "count": len(users_list), "users": users_list}
    return result


@router.post(
    "/user/create",
    tags=["groups"],
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
async def create_group_user(
    *,
    group: GroupUser,
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
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

    check_id = str(group.group_id)
    group_id_exists = await check_id_exists(id=check_id)

    if group_id_exists == False:
        error: dict = {"error": f"Group ID '{check_id}' does not exist"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    check_user = str(group.user)
    exist_user = await check_user_exists(user=check_user, group_id=check_id)

    if exist_user == True:
        error: dict = {"error": f"User ID '{check_id}' already in group"}
        logger.warning(error)
        return JSONResponse(status_code=400, content=error)

    try:

        user_id = str(uuid.uuid4())
        group_data = {"id": user_id, "user": group.user, "group_id": group.group_id}
        logger.debug(group_data)
        # create group
        query = groups_item.insert()
        group_result = await execute_one_db(query=query, values=group_data)

        if "error" in group_result:
            error: dict = group_result
            logger.critical(error)
            return JSONResponse(status_code=400, content=error)

        # data result
        full_result: dict = group_data
        # full_result: dict = {"id": str(user_id), "data": group_result}
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


@router.delete(
    "/user/delete",
    tags=["groups"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Not Found"},
        # 405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_group_item_user_id(
    *,
    user: GroupItemDelete,
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
) -> dict:
    """
    Delete a user by UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [result: user UUID deleted]
    """
    # sleep if delay option is used
    if delay is not None:
        logger.info(f"adding a delay of {delay} seconds")
        await asyncio.sleep(delay)

    check_id = str(user.id)
    group_id_exists = await check_user_id_exists(id=check_id)

    if group_id_exists == False:
        error: dict = {"error": f"Group ID '{check_id}' does not exist"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    try:
        # delete id
        logger.critical(str(user.id))
        query = groups_item.delete().where(groups_item.c.id == user.id)
        await execute_one_db(query)
        result = {"status": f"{user.id} deleted"}
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        logger.error(f"Critical Error: {e}")
        error: dict = {"error": f"{e}"}
        return JSONResponse(status_code=500, content=error)
