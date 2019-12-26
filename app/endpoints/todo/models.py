# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ToDoBase(BaseModel):
    # todo_id: Optional[str]
    title: str
    description: Optional[str] = None
    isComplete: Optional[bool] = False
    dateDue: Optional[datetime] = None
    date_create: Optional[str] = None
    date_update: datetime
    date_complete: Optional[datetime] = None
    user_id: str


# Properties to receive via API on creation
# Additional properties to return via API
class ToDoInDB(ToDoBase):
    todo_id: str


# Create a ToDo
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date_due: Optional[datetime] = None
    user_id: Optional[str]


# # Create a ToDo
# class TodoGetId(ToDoBase):
#     todo_id: str

# # Update a ToDo
# class TodoUpdate(ToDoBase):
#     todo_id: str
#     title: str
#     description: str
#     isComplete: Optional[bool] = False
#     dateDue: Optional[str]

# # complete a ToDo
# class TodoUpdateComplete(ToDoBase):
#     todo_id: str
#     isComplete: bool = True

# # Delete a ToDo
# class TodoDelete(ToDoBase):
#     todo_id: str
