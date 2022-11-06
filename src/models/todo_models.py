# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field, SecretStr, ValidationError, validator


sample_id: str = str(uuid.uuid4())


class ToDoBase(BaseModel):
    # todo_id: Optional[str]
    title: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="title",
        title="Title",
        example="Something To Do",
    )
    description: str = Field(
        None,
        min_length=1,
        max_length=500,
        alias="description",
        title="description",
        example="I am a thing",
    )
    isComplete: bool = Field(default=False)

    date_due: datetime = Field(
        None,
        alias="dateDue",
        title="Date Due",
        example=str(datetime.utcnow()),
    )
    date_create: Optional[str] = Field(
        None,
        alias="date_create",
        title="date_create",
        example=str(datetime.utcnow()),
    )
    date_update: datetime
    date_complete: datetime = Field(
        None,
        alias="date_complete",
        title="date_complete",
        example=str(datetime.utcnow()),
    )
    user_id: str = Field(
        ...,
        alias="userId",
        title="Users ID",
        example=sample_id,
    )


# Properties to receive via API on creation
# Additional properties to return via API
class ToDoInDB(ToDoBase):
    todo_id: str = Field(
        ...,
        alias="todoId",
        title="ToDo ID",
        example=sample_id,
    )


# Create a ToDo
class TodoCreate(BaseModel):
    title: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="title",
        title="Title",
        example="Something To Do",
    )
    description: str = Field(
        None,
        min_length=1,
        max_length=500,
        alias="description",
        title="description",
        example="I am a thing",
    )
    date_due: datetime = Field(
        None,
        alias="dateDue",
        title="Date Due",
        example=str(datetime.utcnow()),
    )
    user_id: str = Field(
        ...,
        alias="userId",
        title="Users ID",
        example=sample_id,
    )


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
