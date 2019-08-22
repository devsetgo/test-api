# -*- coding: utf-8 -*-
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header
from endpoints.sillyusers.gen_user import user_info
import time
import asyncio

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
):
    if delay is None:
        response_list = user_info()
        return response_list

    elif delay in range(0, 11):
        await asyncio.sleep(delay)
        response_list = user_info()
        return response_list

    elif delay not in range(0, 10):
        raise HTTPException(
            status_code=406,
            detail="Not Acceptable: Delay parameter must be between an int 0 and 10 seconds",
        )

    result = user_info()
    return result


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
):

    t0 = time.time()
    id = None
    user = None
    result = []
    # sleep if delay option is used
    if delay is None:
        for i in range(qty):
            x = user_info(user, id)
            result.append(x)
        t1 = time.time() - t0
        return result

    elif delay in range(0, 122):
        await asyncio.sleep(delay)

        for i in range(qty):
            x = user_info(user, id)
            result.append(x)
        t1 = time.time() - t0
        return result

    elif delay not in range(0, 122):
        raise HTTPException(
            status_code=406,
            detail="Not Acceptable: Delay parameter must be between an int 0 and 10 seconds",
        )


# @router.get("/me", tags=["silly users"])
# async def user_me(
#     delay: int = Query(
#         None,
#         title="The number of items in the list to return (min of 1 and max 10)",
#         ge=1,
#         le=10,
#         alias="delay",
#     )
# ):
#     # sleep if delay option is used
#     if delay is not None:
#         asyncio.sleep(delay)

#     id = None
#     user = "Fake Me"
#     result = user_info(user, id)
#     return result


# @router.get("/{id}", tags=["silly users"])
# async def user_id(
#     id: str = Path(..., title="The user id to be searched for", alias="id"),
#     delay: int = Query(
#         None,
#         title="The number of items in the list to return (min of 1 and max 10)",
#         ge=1,
#         le=10,
#         alias="delay",
#     ),
# ):
#     # sleep if delay option is used
#     if delay is not None:
#         asyncio.sleep(delay)

#     user = None
#     result = user_info(user, id)
#     return result
