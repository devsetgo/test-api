# -*- coding: utf-8 -*-
"""
ToDo api endpoints
"""
import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter, Path, Query, HTTPException
from loguru import logger

from core.db_setup import database, todos
from models.todo_models import TodoCreate

router = APIRouter()
# time variables
currentTime = datetime.now()


@router.get("/list", tags=["todo"])
async def todo_list(
    is_complete: bool = Query(None, title="by completion status", alias="complete"),
) -> dict:

    # Fetch multiple rows
    if is_complete is not None:
        query = todos.select().where(todos.c.is_complete == is_complete)
        result = await database.fetch_all(query)
    else:
        query = todos.select()
        result = await database.fetch_all(query)

    logger.info("todo list accessed")
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
    is_complete: bool = Query(None, title="by completion status", alias="complete"),
) -> dict:

    # Fetch multiple rows
    if is_complete is not None:
        query = todos.select().where(todos.c.is_complete == is_complete)
        db_result = await database.fetch_all(query)
    else:
        query = todos.select()
        db_result = await database.fetch_all(query)

    result = {"count": len(db_result)}
    return result


@router.get("/{todo_id}", tags=["todo"], response_description="Get todo information")
async def get_todo_id(
    todo_id: str = Path(..., title="The ToDo id to be searched for", alias="todo_id"),
) -> dict:

    # Fetch single row
    query = todos.select().where(todos.c.todo_id == todo_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{todo_id} not found")

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
) -> dict:

    todo_information = {"is_complete": True, "date_complete": currentTime}

    # Fetch single row
    query = todos.update().where(todos.c.todo_id == todo_id)
    logger.debug(query)
    values = todo_information
    logger.debug(values)
    await database.execute(query, values)
    # Fetch single row
    query = todos.select().where(todos.c.todo_id == todo_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{todo_id} does not exist")
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
    *,
    todo_id: str = Path(..., title="The todo id to be searched for", alias="todo_id"),
) -> dict:
    query = todos.select().where(todos.c.todo_id == todo_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{todo_id} does not exist")

    # delete id
    query = todos.delete().where(todos.c.todo_id == todo_id)
    await database.execute(query)
    query = todos.select().where(todos.c.todo_id == todo_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{todo_id} does not exist")

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

    query = todos.insert()
    values = todo_information
    await database.execute(query, values)
    result = {"todo_id": todo_information["todo_id"]}
    return result
