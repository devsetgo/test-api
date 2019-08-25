# -*- coding: utf-8 -*-
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header
from endpoints.sillyusers.gen_user import user_info
import time
import asyncio
from loguru import logger

router = APIRouter()


@router.get("/make-one", tags=["silly users"])
async def make_user(
    delay: int = Query(
        None,
        title="silly users",
        description="Seconds (max 121)",
        ge=1,
        le=121,
        alias="delay",
    )
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    response_list = user_info()
    return response_list


@router.get("/list", tags=["silly users"])
async def user_list(
    qty: int = Query(
        ..., title="silly list", description="(max 1000)", ge=1, le=1000, alias="qty"
    ),
    delay: int = Query(
        None,
        title="Delay",
        description="Delay seconds (Max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
) -> dict:

    result = []

    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    for i in range(qty):
        x = user_info()
        result.append(x)
    return result
