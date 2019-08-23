# -*- coding: utf-8 -*-
# FastAPI and Starlette libraries
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header

# application libraries
from endpoints.todo.models import TodoCreate

#  from endpoints.todo.models import TodoCreate,TodoUpdate #,TodoDeactivate #, UserUpdate,User, UserInDB
from db_setup import todos, database
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


@router.get("/list", tags=["todo"])
async def todo_list(
    delay: int = Query(
        None,
        title="The number of todos in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
    isComplete: bool = Query(None, title="by completion status", alias="complete"),
):

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # await database.connect()
        # Fetch multiple rows
        if isComplete is not None:
            query = todos.select().where(todos.c.isComplete == isComplete)
            x = await database.fetch_all(query)
        else:
            query = todos.select()
            x = await database.fetch_all(query)

        result = x
        # await database.disconnect()
    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}
    return result


@router.get(
    "/list/count",
    tags=["todo"],
    response_description="Get count of todos",
    responses={
        404: {"description": "Operation forbidden"},
        500: {"description": "Mommy!"},
    },
)
async def todos_list_count(
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
    isComplete: bool = Query(None, title="by completion status", alias="complete"),
):

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)
    try:
        # Fetch multiple rows
        if isComplete is not None:
            query = todos.select().where(todos.c.isComplete == isComplete)
            x = await database.fetch_all(query)
        else:
            query = todos.select()
            x = await database.fetch_all(query)

        result = {"count": len(x)}
    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}

    # print(result)
    return result


@router.get("/{todoId}", tags=["todo"], response_description="Get todo information")
async def get_todo_id(
    todoId: str = Path(..., title="The ToDo id to be searched for", alias="todoId"),
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
        query = todos.select().where(todos.c.todoId == todoId)
        result = await database.fetch_one(query)

    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        # retry db call
        await database.fetch_one(query)
        result = {"status": f"{todoId} retrieved"}
        logger.info("Retry Result: {result}", result=result)
    return result


@router.put(
    "/complete/{todoId}",
    tags=["todo"],
    response_description="The created item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivatee_todo_id(
    *,
    todoId: str = Path(..., title="The ToDo id to be searched for", alias="todoId"),
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
):

    todoInformation = {"isComplete": True, "dateComplete": currentTime}
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        # Fetch single row
        query = todos.update().where(todos.c.todoId == todoId)
        values = todoInformation
        await database.execute(query, values)
        result = await get_todo_id(todoId)
    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        # retry db call
        await database.execute(query, values)
        result = await get_todo_id(todoId)
        logger.info("Retry Result: {result}", result=result)
    return result


@router.delete(
    "/{todoId}",
    tags=["todo"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_todo_id(
    *, todoId: str = Path(..., title="The todo id to be searched for", alias="todoId")
):

    try:
        # delete id
        query = todos.delete().where(todos.c.todoId == todoId)
        await database.execute(query)
        result = {"status": f"{todoId} deleted"}
    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        # retry db call
        await database.execute(query)
        result = {"status": f"{todoId} deleted"}
        logger.info("Retry Result: {result}", result=result)
    return result


@router.post(
    "/create/",
    tags=["todo"],
    response_description="The created ToDo",
    responses={
        302: {"description": "Incorect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def create_todo(
    *,
    todo: TodoCreate,
    delay: int = Query(
        None,
        title="The number of items in the list to return (min of 1 and max 10)",
        ge=1,
        le=10,
        alias="delay",
    ),
):
    #  = Body(..., example={"title": "A thing", "description": "A description of a thing", "dateDue": '2019-04-14 15:15:34.832031','userId': 'Bob'}, embed=True)
    value = todo.dict()
    # print(value)
    # dictionary to append to todo_full_list
    todoInformation = {
        "todoId": str(uuid.uuid1()),
        "title": value["title"],
        "description": value["description"],
        "dateDue": value["dateDue"],
        "isComplete": False,
        "dateCreate": currentTime,
        "dateUpdate": currentTime,
        "userId": value["userId"],
        # ,'checklist': []
        "dateComplete": None,
    }
    # print(len(todo_full_list))
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        query = todos.insert()
        values = todoInformation
        await database.execute(query, values)
        result = {"todoId": todoInformation["todoId"]}
    except Exception as e:
        # print(e)
        logger.info("Error: {error}", error=e)
        result = {"error": e}
        # retry db call
        await database.execute(query, values)
        result = {"todoId": todoInformation["todoId"]}
        logger.info("Retry Result: {result}", result=result)
    return result
