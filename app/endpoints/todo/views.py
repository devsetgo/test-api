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

from com_lib.db_setup import database
from com_lib.db_setup import todos
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
    is_complete: bool = Query(None, title="by completion status", alias="complete"),
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    # Fetch multiple rows
    if is_complete is not None:
        query = todos.select().where(todos.c.is_complete == is_complete)
        x = await database.fetch_all(query)
    else:
        query = todos.select()
        x = await database.fetch_all(query)

    logger.info("todo list accessed")
    result = x
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
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
    is_complete: bool = Query(None, title="by completion status", alias="complete"),
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)
    # Fetch multiple rows
    if is_complete is not None:
        query = todos.select().where(todos.c.is_complete == is_complete)
        x = await database.fetch_all(query)
    else:
        query = todos.select()
        x = await database.fetch_all(query)

    result = {"count": len(x)}
    return result


@router.get("/{todo_id}", tags=["todo"], response_description="Get todo information")
async def get_todo_id(
    todo_id: str = Path(..., title="The ToDo id to be searched for", alias="todo_id"),
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)
    # Fetch single row
    query = todos.select().where(todos.c.todo_id == todo_id)
    result = await database.fetch_one(query)
    return result


@router.put(
    "/complete/{todo_id}",
    tags=["todo"],
    response_description="The created item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def deactivate_todo_id(
    *,
    todo_id: str = Path(..., title="The ToDo id to be searched for", alias="todo_id"),
    delay: int = Query(None, title=title, ge=1, le=10, alias="delay",),
) -> dict:

    todo_information = {"is_complete": True, "date_complete": currentTime}
    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    # Fetch single row
    query = todos.update().where(todos.c.todo_id == todo_id)
    values = todo_information
    await database.execute(query, values)
    result = await get_todo_id(todo_id)
    return result


@router.delete(
    "/{todo_id}",
    tags=["todo"],
    response_description="The deleted item",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        404: {"description": "Operation forbidden"},
        405: {"description": "Method not allowed"},
        500: {"description": "Mommy!"},
    },
)
async def delete_todo_id(
    *, todo_id: str = Path(..., title="The todo id to be searched for", alias="todo_id")
) -> dict:

    # delete id
    query = todos.delete().where(todos.c.todo_id == todo_id)
    await database.execute(query)
    result = {"status": f"{todo_id} deleted"}
    return result


@router.post(
    "/create/",
    tags=["todo"],
    response_description="The created ToDo",
    responses={
        302: {"description": "Incorrect URL, redirecting"},
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
    todo_information = {
        "todo_id": str(uuid.uuid1()),
        "title": value["title"],
        "description": value["description"],
        "date_due": value["date_due"],
        "is_complete": False,
        "date_create": currentTime,
        "date_update": currentTime,
        "user_id": value["user_id"],
        # ,'checklist': []
        "date_complete": None,
    }

    # sleep if delay option is used
    if delay is not None:
        asyncio.sleep(delay)

    query = todos.insert()
    values = todo_information
    await database.execute(query, values)
    result = {"todo_id": todo_information["todo_id"]}
    return result
