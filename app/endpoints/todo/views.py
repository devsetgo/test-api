# -*- coding: utf-8 -*-
"""
ToDo api endpoints
"""
import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter
from fastapi import Path
from fastapi import Query
from loguru import logger

from db_setup import database
from db_setup import todos
from endpoints.todo.models import TodoCreate

router = APIRouter()
# time variables
currentTime = datetime.now()

title = "Delay in Seconds"


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
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    try:
        # await database.connect()
        # Fetch multiple rows
        if isComplete is not None:
            query = todos.select().where(todos.c.isComplete == isComplete)
            x = await database.fetch_all(query)
        else:
            query = todos.select()
            x = await database.fetch_all(query)

        logger.info(f"todo list accessed")
        result = x
        return result

    except Exception as e:
        logger.error(f"List Error: {e}")


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
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
    isComplete: bool = Query(None, title="by completion status", alias="complete"),
) -> dict:

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
        return result
    except Exception as e:
        logger.info("Count Error: {error}", error=e)


@router.get("/{todoId}", tags=["todo"], response_description="Get todo information")
async def get_todo_id(
    todoId: str = Path(..., title="The ToDo id to be searched for", alias="todoId"),
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)
    try:
        # Fetch single row
        query = todos.select().where(todos.c.todoId == todoId)
        result = await database.fetch_one(query)
        return result
    except Exception as e:
        logger.critical("ID Error: {error}", error=e)


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
async def deactivate_todo_id(
    *,
    todoId: str = Path(..., title="The ToDo id to be searched for", alias="todoId"),
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:

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
        return result
    except Exception as e:
        logger.critical("Deactivate Error: {error}", error=e)


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
) -> dict:

    try:
        # delete id
        query = todos.delete().where(todos.c.todoId == todoId)
        await database.execute(query)
        result = {"status": f"{todoId} deleted"}
        return result
    except Exception as e:
        logger.critical("Delete Error: {error}", error=e)


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
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:

    value = todo.dict()
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

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    try:
        query = todos.insert()
        values = todoInformation
        await database.execute(query, values)
        result = {"todoId": todoInformation["todoId"]}
        return result
    except Exception as e:
        logger.critical(f"Create Error: {e}")
