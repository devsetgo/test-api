from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header
from services.rand_word import r_w
from services.gen_data import create_list, create_item
import time
import uuid
import random
import asyncio

router = APIRouter()


@router.get(
    "/list", tags=["sample"], responses={404: {"description": "Operation forbidden"}, 500: {"description": "Mommy!"}}
)
async def sample_list(
    *, qty: int = Query(..., title='The number of items in the list to return (min of 1 and max 1000)', ge=1, le=1000, alias="quantity"), delay: int = Query(None, title='The number of items in the list to return (min of 1 and max 10)', ge=1, le=10, alias="delay")
):

    if delay is None:
        response_list = create_list(qty)
        return response_list

    elif delay in range(0, 11):
        await asyncio.sleep(delay)
        response_list = create_list(qty)
        return response_list

    elif delay not in range(0, 10):
        raise HTTPException(
            status_code=404, detail="Delay parameter must be between an int 0 and 10 seconds")


@router.get("/{id}", tags=["sample"], responses={404: {"description": "Operation forbidden"}, 500: {"description": "Mommy!"}})
async def sample_item(
        id: str = Path(..., title='The ID to search for'), delay: int = Query(None, title='The delay time in seconds', ge=1, le=10, alias="delay")):

    if delay is None:
        j_response = create_item(id)
        return j_response

    elif delay in range(0, 11):
        await asyncio.sleep(delay)
        j_response = create_item(id)
        return j_response

    elif delay not in range(0, 10):
        raise HTTPException(
            status_code=404, detail="Delay parameter must be between an int 0 and 10 seconds")
