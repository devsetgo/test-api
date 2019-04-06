from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Schema

router = APIRouter()


class Item(BaseModel):
    name: str
    description: str = Schema(
        None, title="The description of the item", max_length=300)
    price: float = Schema(..., gt=0,
                          description="The price must be greater than zero")
    tax: float = None


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.get("/{item_id}")
async def read_item(item_id: str):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(*, item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
