# -*- coding: utf-8 -*-
"""
Group Routes
List Groups
Count Groups
State of Group
Create Group
Get Group
Add User to Group
Remove User to Group
"""
import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter, Query, status, HTTPException
from fastapi.responses import JSONResponse, ORJSONResponse
from loguru import logger

from core.db_setup import database, groups, groups_item
from crud.crud_ops import execute_one_db, fetch_all_db, fetch_one_db
from crud.group_crud import (
    check_id_exists,
    check_unique_name,
    check_user_exists,
    check_user_id_exists,
    delete_user_in_group,
)
from models.group_models import (
    GroupCreate,
    GroupItemDelete,
    GroupTypeEnum,
    GroupUser,
)

router = APIRouter()


@router.get("/list", tags=["groups"], status_code=200)
async def group_list(
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
        ge=0,
        le=10000,
        alias="offset",
    ),
    is_active: bool = Query(None, title="by active status", alias="active"),
    group_type: GroupTypeEnum = Query(
        None, title="groupType", description="Type of group", alias="groupType"
    ),
    group_name: str = Query(
        None,
        title="Group Name",
        description="Get by the Group Name",
        alias="groupName",
    ),
) -> dict:
    """[summary]
    Get list of all groups and associated information

    Args:

        qty (int, optional): [description]. Defaults to Query( None, title="Quanity",
         description="Records to return (max 500)", ge=1, le=500, alias="qty", ).
        offset (int, optional): [description]. Defaults to Query( None, title="Offset",
         description="Offset increment", ge=0,le=10000, alias="offset" ).
        is_active (bool, optional): [description]. Defaults to Query(None,
         title="by active status", alias="active").
        group_type (GroupTypeEnum, optional): [description]. Defaults to Query( None,
         title="groupType", description="Type of group", alias="groupType" ).

    Returns:
        dict: [description]
        GroupId, Name, Description, active state, dates created & updated
    """
    criteria = []

    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if is_active is not None:
        criteria.append((groups.c.is_active, is_active, "equal"))

    if group_type is not None:
        criteria.append((groups.c.group_type, group_type, "equal"))

    if group_name is not None:

        if group_name.isalnum() is False:
            error_note = {
                "message": f"Group Name {group_name} is not a valud alpha numeric value"
            }
            logger.error(error_note)
            raise HTTPException(status_code=422, detail=error_note)

        criteria.append((groups.c.name, group_name, "ilike"))

    query = groups.select().order_by(groups.c.date_create).limit(qty).offset(offset)
    count_query = groups.select()

    for crit in criteria:
        col, val, compare_type = crit

        if compare_type == "ilike":
            query = query.where(col.ilike(f"%{val}%"))

        else:
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
        },
        "groups": db_result,
    }
    return result


@router.get("/list/count", tags=["groups"], status_code=200)
async def group_list_count(
    is_active: bool = Query(None, title="by active status", alias="active"),
    group_type: GroupTypeEnum = Query(
        None, title="groupType", description="Type of group", alias="groupType"
    ),
) -> dict:
    """[summary]
    Get a count of groups
    Args:
        is_active (bool, optional): [description]. Defaults to Query(None,
         title="by active status", alias="active").
        group_type (GroupTypeEnum, optional): [description]. Defaults to Query( None,
         title="groupType", description="Type of group", alias="groupType" ).

    Returns:
        dict: [description]
        count based on filters
    """
    criteria = []

    if is_active is not None:
        criteria.append((groups.c.is_active, is_active))

    if group_type is not None:
        criteria.append((groups.c.group_type, group_type))

    query = groups.select().order_by(groups.c.date_create)
    count_query = groups.select()

    for crit in criteria:
        col, val = crit
        query = query.where(col == val)
        count_query = count_query.where(col == val)

    total_count = await database.fetch_all(count_query)

    result = {
        "parameters": {
            "total_count": len(total_count),
            "filter": is_active,
        },
    }
    return result


@router.put(
    "/state",
    tags=["groups"],
    response_description="ID Modified",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Not Found"},
        405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def group_state(
    *,
    id: str = Query(
        ...,
        title="group id",
        description="Group UUID",
        alias="id",
    ),
    is_active: bool = Query(
        None,
        title="active status",
        description="true or false of status",
        alias="isActive",
    ),
) -> dict:
    """[summary]
        Active or Deactivate a Group ID
    Args:
        id (str, optional): [description]. Defaults to
         Query(..., title="group id", description="Group UUID", alias="id",).
        state (bool, optional): [description]. Defaults to
         Query( ..., title="active state", description="true or false of state",\
              alias="state", ).

    Returns:
        dict: [id, state]
    """

    if is_active is None:
        error: dict = {
            "error": "isActive must be true or false and \
            cannot be empty"
        }
        logger.warning(error)
        return JSONResponse(status_code=422, content=error)

    id_exists = await check_id_exists(id)

    if id_exists is False:
        error: dict = {"error": f"Group ID: '{id}' not found"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    try:

        group_data = {
            "is_active": is_active,
            "date_update": datetime.now(),
        }
        logger.debug(group_data)
        # create group
        query = groups.update().where(groups.c.id == id)
        group_result = await execute_one_db(query=query, values=group_data)
        logger.debug(str(group_result))

        full_result: dict = {"id": id, "status": is_active}
        logger.debug(full_result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=full_result)
    except Exception as e:
        error: dict = {"error": str(e)}
        logger.debug(e)
        logger.error(error)
        return JSONResponse(status_code=400, content=error)


@router.post(
    "/create",
    tags=["groups"],
    response_description="The created item",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def create_group(
    *,
    group: GroupCreate,
) -> dict:
    """[summary]
    Create a new group
    Args:
        group (GroupCreate): [description]

    Returns:
        dict: [description]
        Group data
    """
    # approval or notification
    group_type_check: list = ["approval", "notification"]
    if group.group_type not in group_type_check:
        error: dict = {
            "error": f"Group Type '{group.group_type}'\
                 is not 'approval' or 'notification'"
        }
        logger.warning(error)
        return JSONResponse(status_code=400, content=error)

    check_name = str(group.name)
    duplicate = await check_unique_name(check_name)

    try:
        if duplicate is False:
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

        full_result: dict = {"id": str(group_id), "data": group_result}
        logger.debug(full_result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=full_result)
    except Exception as e:
        error: dict = {"error": str(e)}
        logger.error(error)
        return JSONResponse(status_code=400, content=error)


@router.get("/group", tags=["groups"], status_code=200)
async def group_id(
    group_id: str = Query(
        None,
        title="Group ID",
        description="Get by the Group UUID",
        alias="groupId",
    ),
    group_name: str = Query(
        None,
        title="Group Name",
        description="Get by the Group Name",
        alias="groupName",
    ),
) -> dict:
    """[summary]
    Get individual group data, including users
    Args:
        group_id (str, optional): [description]. Defaults to Query( None,
         title="Group ID", description="Get by the Group UUID", alias="groupId", ).
        group_name (str, optional): [description]. Defaults to Query( None,
         title="Group Name", description="Get by the Group Name", alias="groupName", ).


    Returns:
        dict: [description]
        Group data and associated users
    """

    # if search by ID
    if group_id is not None:

        id_exists = await check_id_exists(group_id)
        if id_exists is False:
            error: dict = {"error": f"Group ID: '{group_id}' not found"}
            logger.warning(error)
            return JSONResponse(status_code=404, content=error)

    # elif search by name
    elif group_name is not None:

        name_exists = await check_unique_name(group_name)
        if name_exists is True:
            error: dict = {"error": f"Group Name: '{group_name}' not found"}
            logger.warning(error)
            return JSONResponse(status_code=404, content=error)

        query = groups.select().where(groups.c.name == group_name)
        name_result = await fetch_one_db(query=query)
        group_id = name_result["id"]
    # else at least one needs to be selected
    else:
        error: dict = {"error": "groupId or groupName must be used"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    query = groups_item.select().where(groups_item.c.group_id == group_id)
    db_result = await fetch_all_db(query=query)

    users_list: list = []
    user_dict: list = []
    for r in db_result:
        logger.debug(r)
        user_data: dict = {
            "id": r["id"],
            "user": r["user"],
            "date_created": str(r["date_create"]),
        }
        user_dict.append(user_data)
        users_list.append(r["user"])
    result = {
        "group_id": group_id,
        "count": len(users_list),
        "users": users_list,
        "user_info": user_dict,
    }
    return JSONResponse(status_code=200, content=result)


@router.post(
    "/user/create",
    tags=["groups"],
    response_description="The created item",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def create_group_user(
    *,
    group: GroupUser,
) -> dict:
    """[summary]
    Add a user to a group
    Args:
        group (GroupUser): [description]


    Returns:
        dict: [description]
        Confirmation of user being added
    """

    check_id = str(group.group_id)
    group_id_exists = await check_id_exists(id=check_id)

    if group_id_exists is False:
        error: dict = {"error": f"Group ID '{check_id}' does not exist"}
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    check_user = str(group.user)
    exist_user = await check_user_exists(user=check_user, group_id=check_id)

    if exist_user is True:
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
        logger.debug(str(group_result))

        full_result: dict = group_data
        logger.debug(full_result)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=full_result)
    except Exception as e:
        error: dict = {"error": str(e)}
        logger.debug(e)
        logger.error(f"Error: {e}")
        return JSONResponse(status_code=400, content=error)


@router.delete(
    "/user/delete",
    tags=["groups"],
    response_description="The deleted item",
    status_code=200,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Not Found"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_group_item_user_id(
    *,
    user: GroupItemDelete,
) -> dict:
    """[summary]
    Remove User from Group
    Args:
        user (GroupItemDelete): [description]

    Returns:
        dict: [description]
        Confirmation of removal
    """

    user_id = str(user.user)
    group_id = str(user.group_id)
    group_id_exists = await check_user_id_exists(id=user_id, group_id=group_id)
    # print(group_id_exists)
    if group_id_exists is False:
        error: dict = {
            "message": f"Group ID: {group_id} and/or User ID: {user_id} does not exist in Group"
        }
        logger.warning(error)
        return JSONResponse(status_code=404, content=error)

    result = await delete_user_in_group(id=user_id, group_id=group_id)
    return result
