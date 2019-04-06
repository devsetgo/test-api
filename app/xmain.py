from fastapi import FastAPI, Path, Query, HTTPException
from rand_word import r_w
from gen_data import create_list, create_item
import time
import uuid
import random
import asyncio
# import uvicorn


app = FastAPI(title="Test API",
    description="API's to be used for testing and creating sample data. Parameters to include delays, random generation of data, and other useful things to help mock an application.",
    version="2019.4.5")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/sample")
async def sample_list(
    *
    ,qty: int = Query(..., title='The number of items in the list to return (min of 1 and max 1000)', ge=1, le=1000)
    ,delay: int = None
    ):
    
    if delay is None:
        response_list = create_list(qty)
        return response_list

    elif delay in range(0, 11):
        await asyncio.sleep(delay)
        response_list = create_list(qty)
        return response_list

    elif delay not in range(0, 10):
        raise HTTPException(status_code=404, detail="Delay parameter must be between an int 0 and 10 seconds")
        # return response_list

    


@app.get("/sample/{id}")
async def sample_item(
    id: str
    ,delay: int = None):
    
    await asyncio.sleep(delay)
    
    rand_str = r_w(random.randrange(1,10))
    # id = uuid.uuid1()
    j_response = create_item(id)
    

    return j_response

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info", reload=True)
