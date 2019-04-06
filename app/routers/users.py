from fastapi import APIRouter, Query
from services.gen_user import user_info
import time
router = APIRouter()


@router.get("/make", tags=["users"])
async def make_user():
    
    result = user_info()
    return result

@router.get("/list", tags=["users"])
async def user_list(qty: int = Query(..., title='The number of items in the list to return (min of 1 and max 1000)', ge=1, le=1000, alias="quantity")):
    t0 = time.time()
    id = None
    user = None

    result = []
    for i in range(qty):
        x = user_info(user, id)
        result.append(x)
    t1 = time.time()-t0
    return result


@router.get("/me", tags=["users"])
async def user_me():
    id = None
    user = 'Fake Me'
    result = user_info(user, id)
    return result


@router.get("/{sent_id}", tags=["users"])
async def user_id(id: str = Query(..., title='The user id to be searched for', alias="user")):
    user = None
    result = user_info(user,id)
    return result