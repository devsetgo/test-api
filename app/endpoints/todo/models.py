# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ToDoBase(BaseModel):
    # todoId: Optional[str]
    title: str
    description: Optional[str] = None
    isComplete: Optional[bool] = False
    dateDue: Optional[datetime] = None
    dateCreate: Optional[str] = None
    dateUpdate: datetime
    dateComplete: Optional[datetime] = None
    userId: str


# Properties to receive via API on creation
# Additional properties to return via API
class ToDoInDB(ToDoBase):
    todoId: str


# Create a ToDo
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    dateDue: Optional[datetime] = None
    userId: Optional[str]


# # Create a ToDo
# class TodoGetId(ToDoBase):
#     todoId: str

# # Update a ToDo
# class TodoUpdate(ToDoBase):
#     todoId: str
#     title: str
#     description: str
#     isComplete: Optional[bool] = False
#     dateDue: Optional[str]

# # complete a ToDo
# class TodoUpdateComplete(ToDoBase):
#     todoId: str
#     isComplete: bool = True

# # Delete a ToDo
# class TodoDelete(ToDoBase):
#     todoId: str
