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

from fastapi import APIRouter, Form, Path, Query, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from core.db_setup import database, users
from core.pass_lib import encrypt_pass, verify_pass
from core.simple_functions import get_current_datetime
from models.user_models import UserCreate, UserDeactiveModel, UserPwd
from crud import user_crud
from crud.crud_ops import fetch_one_db, execute_one_db, fetch_all_db


router = APIRouter()


@router.get("/list", tags=["users"])
async def user_list(
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
    first_name: str = Query(None, title="first name", alias="firstname"),
    last_name: str = Query(None, title="last name", alias="lastname"),
    title: str = Query(None, title="title", alias="title"),
    company: str = Query(None, title="company", alias="company"),
    city: str = Query(None, title="city", alias="city"),
    country: str = Query(None, title="country", alias="country"),
    postal: str = Query(None, title="postal code", alias="postal"),
) -> dict:

    """
    list of users

    Keyword Arguments:
        qty {int} -- [description] 100 returned results is default,
        maximum is 500
        offset {int} -- [description] 0 seconds default
        Active {bool} -- [description] no default as not required,
        must be Active=true or false if used

    Returns:
        dict -- [description]

    """
    criteria = []
    if qty is None:
        qty: int = 100

    if offset is None:
        offset: int = 0

    if first_name is not None:
        criteria.append((users.c.first_name, first_name))

    if last_name is not None:
        criteria.append((users.c.last_name, last_name))

    if title is not None:
        criteria.append((users.c.title, title))

    if company is not None:
        criteria.append((users.c.company, company))

    if city is not None:
        criteria.append((users.c.city, city))

    if country is not None:
        criteria.append((users.c.country, country))

    if postal is not None:
        criteria.append((users.c.postal, postal))

    if is_active is not None:
        criteria.append((users.c.is_active, is_active))

    query = users.select().order_by(users.c.date_create).limit(qty).offset(offset)
    count_query = users.select().order_by(users.c.date_create)

    for crit in criteria:
        col, val = crit
        query = query.where(col == val)
        count_query = count_query.where(col == val)

    db_result = await database.fetch_all(query)
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
            "city": r["city"],
            "country": r["country"],
            "postal": r["postal"],
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
    is_active: bool = Query(None, title="by active status", alias="active"),
) -> dict:
    """
    Count of users in the database

    Keyword Arguments:
        Active {bool} -- [description] no default as not required,
        must be Active=true or false if used

    Returns:
        dict -- [description]
    """

    try:
        # Fetch multiple rows
        if is_active is not None:
            query = users.select().where(users.c.is_active == is_active)
            x = await database.fetch_all(query)
        else:
            query = users.select()
            x = await database.fetch_all(query)

        result = {"count": len(x)}
        return result
    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.get("/{user_id}", tags=["users"], response_description="Get user information")
async def get_user_id(
    user_id: str = Path(..., title="The user id to be searched for", alias="user_id"),
) -> dict:
    """
    User information for requested UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required


    Returns:
        dict -- [description]
    """

    try:
        # Fetch single row
        query = users.select().where(users.c.user_id == user_id)
        db_result = await database.fetch_one(query)
        print(db_result)
        if db_result is None:
            error_note = {"message": f"user id {user_id} not found"}
            logger.error(error_note)
            # raise HTTPException(status_code=404, detail=error_note)
            return JSONResponse(status_code=404, content=error_note)
        user_data = {
            "user_id": db_result["user_id"],
            "user_name": db_result["user_name"],
            "first_name": db_result["first_name"],
            "last_name": db_result["last_name"],
            "company": db_result["company"],
            "title": db_result["title"],
            "address": db_result["address"],
            "city": db_result["city"],
            "country": db_result["country"],
            "postal": db_result["postal"],
            "email": db_result["email"],
            "website": db_result["website"],
            "description": db_result["description"],
            "date_create": db_result["date_create"],
            "date_updated": db_result["date_updated"],
            "is_active": db_result["is_active"],
        }
        return user_data

    except Exception as e:
        logger.error(f"Critical Error: {e}")


@router.put(
    "/status",
    tags=["users"],
    response_description="The created item",
    status_code=200,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def set_status_user_id(
    *,
    user_data: UserDeactiveModel,
) -> dict:
    """
    Set status of a specific user UUID

    Args:
        user_data (UserDeactiveModel): [id = UUID of user, isActive = True or False]

    Returns:
        dict: [description]
    """
    """
    Set status of a specific user UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required


    Returns:
        dict -- [description]
    """

    values = user_data.dict()
    values["date_updated"] = get_current_datetime()

    data = {"user_id": values["id"], "is_active": values["is_active"]}
    user_id = values["id"]
    status = values["is_active"]

    try:
        # Fetch single row
        query = users.select().where(users.c.user_id == user_id)
        db_result = await database.fetch_one(query)
        logger.debug(db_result)
        if db_result is None:
            error_note = {"message": f"user id {user_id} not found"}
            logger.error(f"LOOK AT THIS: {error_note}")
            # raise HTTPException(status_code=404, detail=error_note)
            return JSONResponse(status_code=404, content=error_note)

    except Exception as e:
        logger.error(f"Critical Error: {e}")

    try:
        # Fetch single row
        query = users.update().where(users.c.user_id == user_id)
        result = await database.execute(query=query, values=data)

    except Exception as e:
        error_note = {"message": e}
        logger.error(error_note)
        # raise HTTPException(status_code=400, detail=error_note)
        return JSONResponse(status_code=400, content=error_note)

    return {"message": f"{user_id} status set to {status}"}


@router.delete(
    "/{user_id}",
    tags=["users"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_user_id(
    *, user_id: str = Path(..., title="The user id to be deleted", alias="user_id")
) -> dict:
    """
    Delete a user by UUID

    Keyword Arguments:
        user_id {str} -- [description] UUID of user_id property required

    Returns:
        dict -- [result: user UUID deleted]
    """

    try:
        # Fetch single row
        query = users.select().where(users.c.user_id == user_id)
        db_result = await database.fetch_one(query)
        # print(db_result)
        if db_result is None:

            error_note = {"message": f"user id {user_id} not found"}
            logger.error(error_note)
            # raise HTTPException(status_code=404, detail=error_note)
            return JSONResponse(status_code=404, content=error_note)

    except Exception as ex:
        error_note = {"message": ex}
        logger.error(error_note)
        # raise HTTPException(status_code=400, detail=error_note)
        return JSONResponse(status_code=400, content=error_note)

    try:
        # delete id
        query = users.delete().where(users.c.user_id == user_id)
        await database.execute(query)
        result = {"status": f"{user_id} deleted"}
        return result

    except Exception as ex:
        error_note = {"message": ex}
        logger.error(error_note)
        # raise HTTPException(status_code=400, detail=error_note)
        return JSONResponse(status_code=400, content=error_note)


@router.post(
    "/create/",
    tags=["users"],
    response_description="The created item",
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        422: {"description": "Validation Error"},
        500: {"description": "Mommy!"},
    },
)
async def create_user(
    *,
    user: UserCreate,
) -> dict:
    """
    POST/Create a new User. user_name (unique), firstName, lastName, email,
    and password are required. All other fields are optional.

    Arguments:
        user {UserCreate} -- [description]

    Keyword Arguments:


    Returns:
        dict -- [user_id: uuid, user_name: user_name]
    """
    value = user.dict()
    logger.debug(f"input values {value}")
    email = value["email"]
    user_name = value["user_name"].lower()

    if (
        email is None
        or user_name is None
        or value["first_name"] is None
        or value["last_name"] is None
    ):
        error_note = {"message": f"Required fields are missing"}
        logger.error(error_note)
        raise HTTPException(status_code=400, detail=error_note)

    unique_check: bool = await user_crud.check_unique_contraints(
        email=email, user_name=user_name
    )
    logger.debug(f"LOOK AT THIS RESULT {unique_check}")
    if unique_check == True:
        error_note = {
            "message": f"The email '{email}' and/or user_name '{user_name}' is not unique and maybe in use"
        }
        logger.error(error_note)
        raise HTTPException(status_code=400, detail=error_note)

    hash_pwd = encrypt_pass(value["password"])

    user_information = {
        "user_id": str(uuid.uuid1()),
        "user_name": value["user_name"].lower(),
        "first_name": value["first_name"],
        "last_name": value["last_name"],
        "password": hash_pwd,
        "email": value["email"],
        "title": value["title"],
        "company": value["company"],
        "address": value["address"],
        "city": value["city"],
        "country": value["country"],
        "postal": value["postal"],
        "website": value["website"],
        "description": value["description"],
        "date_create": get_current_datetime(),
        "date_updated": get_current_datetime(),
        "is_active": True,
        "is_superuser": False,
    }

    try:
        query = users.insert()
        values = user_information
        await database.execute(query, values)

        result = {
            "user_id": user_information["user_id"],
            "user_name": value["user_name"],
        }
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


@router.post(
    "/check-pwd/",
    tags=["users"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def check_pwd(
    userPwd: UserPwd,
    # user_name: str = Form(...), password: str = Form(...)
) -> dict:
    """
    Check password function

    Keyword Arguments:
        user_name {str} -- [description] existing user_name required
        password {str} -- [description] password required

    Returns:
        [Dict] -- [result: bool]
    """
    # try:
    # Fetch single row
    data = dict(userPwd)
    query = users.select().where(users.c.user_name == data["user_name"].lower())
    logger.debug(f"password check query: {query}")
    db_result = await fetch_one_db(query)
    if db_result is None:
        error: dict = {"result": False, "message": "user_name, password is invalid"}
        return JSONResponse(status_code=200, content=error)
    logger.debug(f"verify password query result: {db_result}")
    result = verify_pass(data["password"], db_result["password"])
    logger.info(f"password validation: user: {data['user_name'].lower()} as {result}")
    return {"result": result, "message": "user_name, password is valid"}

    # except Exception as e:
    #     logger.error(f"Verify Password Error: {e} = user_name: {user_name} - password: {password}")
