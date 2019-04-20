import asyncio
import random
import uuid
import os
import json
import pickle
from datetime import datetime, timedelta
import time
from services.gen_data import create_list, create_item
from services.rand_word import r_w
from services.rand_name import randName
from endpoints.todo.services import list_count, get_todo
from typing import List, Set
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header
from .model import ToDoBase, TodoCreate, TodoGetId, TodoUpdate, TodoDelete
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Schema, json
from loguru import logger

file_path = (os.path.abspath("logfile/file_1.log"))
# logger.debug("That's it, beautiful and simple logging!")
logger.add(file_path, backtrace=True, retention="10 days", rotation="1 MB")

router = APIRouter()

currentTime = datetime.now()
days30Plus = currentTime + timedelta(days=30)
todo_full_list = []


@router.get("/list", tags=["todo"], responses={404: {"description": "Operation forbidden"}, 500: {"description": "Mommy!"}})
async def todo_list(delay: int = Query(None, title='The number of items in the list to return (min of 1 and max 10)', ge=1, le=10, alias="delay")
                    ,user: str = Query(None, title='filter by userid', alias="userid")):
    if delay is None:
        result = todo_full_list
        # print(result)

        return result

    else:
        await asyncio.sleep(delay)
        result = todo_full_list
        return result


@router.get("/list/count", tags=["todo"], responses={404: {"description": "Operation forbidden"}, 500: {"description": "Mommy!"}})
async def todo_list_count(delay: int = Query(None, title='The number of items in the list to return (min of 1 and max 10)', ge=1, le=10, alias="delay")):

    if delay is not None:
        await asyncio.sleep(delay)

    result = list_count(todo_full_list)
    return result

# create a function to search for id


def find_id(id: str):
    # print(todo_full_list)
    for i in todo_full_list:
        # print(i['id'])
        if i['id'] == id:
            result = i
            description = 'Found'
    
    logger.info('ID: {id} searched and {description}',id=id,description=description,)
    return result


@router.get("/id/{id}", tags=["todo"]            # , response_model=TodoGetId
            , responses={404: {"description": "Operation forbidden"}, 500: {"description": "Mommy!"}})
async def get_todo_id(id: str = Path(..., title='The ID to search for'), delay: int = Query(None, title='The delay time in seconds', ge=1, le=10, alias="delay")):
    # print(f'id:{id},delay:{delay}')
    # print(todo_full_list)
    # cid = f"UUID('{id}')"
    logger.info('{description} with ID: {id} and a delay={delay}',id=id,description='ToDo Created',delay=delay)
    if delay is None:
        result = find_id(id)
        return result
    else:
        await asyncio.sleep(delay)
        result = 'bob'
        # result = get_todo(id, todo_full_list)
        return result



@router.post("/create/", tags=["todo"], response_model=TodoCreate, response_description="The created item"
             , responses={302: {"description": "Incorect URL, redirecting"}, 404: {"description": "Operation forbidden"}, 405: {"description": "Method not allowed"}, 500: {"description": "Mommy!"}})
async def create_todo(*,todo: TodoCreate
                    , delay: int = Query(None, title='The number of items in the list to return (min of 1 and max 10)', ge=1, le=10, alias="delay")):
    #  = Body(..., example={"title": "A thing", "description": "A description of a thing", "dateDue": '2019-04-14 15:15:34.832031','userId': 'Bob'}, embed=True)
    value = todo.dict()
    
    # dictionary to append to todo_full_list
    result = {'id': str(uuid.uuid1())
            ,'title': value['title']
            ,'description': value['description']
            ,'dueDate': value['dateDue']
            ,'isComplete': False
            ,'dateCreate': currentTime
            ,'dateUpdate': currentTime
            ,'userId': value['userId']
            ,'checklist': []
            ,'dateCompleted': None
            }
    # print(len(todo_full_list))
    logger.info('{description} with ID: {id} and a delay={delay}',id=result['id'],description='ToDo Created',delay=delay)
    if delay is None:
        todo_full_list.append(result)
        return result
    else:
        await asyncio.sleep(delay)
        todo_full_list.append(result)
        
        return result
