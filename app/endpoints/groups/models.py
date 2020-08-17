# -*- coding: utf-8 -*-
from enum import Enum, IntEnum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, SecretStr


# Shared properties
class GroupTypeEnum(str, Enum):
    approval = "approval"
    notification = "notification"

class GroupsBase(BaseModel):
    name: str = Field(
        ...,
        alias="name",
        title="The unique name for the group",
        min_length=1,
        max_length=50,
        regex="^\w+$",
        example="AlphaNumericOnly",
    )
    description: str = Field(
        None,
        alias="description",
        title="A helpful description of the group",
        min_length=1,
        max_length=250,
        example="A helpful description of the group",
    )
    group_type: str = Field(
        ...,
        alias="group_type",
        title="approval or notification",
        min_length=1,
        max_length=50,
        example="approval",
    )

class GroupItemBase(BaseModel):
    user: str = Field(
        None,
        alias="user",
        title="a user",
        min_length=6,
        max_length=6,
        example="abc123",
    )

class GroupCreate(GroupsBase):
    # id: UUID = Field(default_factory=uuid4)
    # users: List[GroupItemBase]
    is_active: bool = Field(default=False)

class GroupDeactivate(BaseModel):
    id: str = Field(
        ...,
        alias="id",
        title="The ID of the Group",
        example="UUID-OF-THE-GROUP-TO-DEACTIVATE",
    )
    is_active: bool = Field(default=False)

class GroupItemDelete(BaseModel):
    id: str = Field(
        ...,
        alias="id",
        title="The ID of the User",
        example="UUID-OF-THE-USER-TO-DELETE",
    )

class GroupsOut(BaseModel):
    GroupsBase
    GroupItemBase

class GroupUser(BaseModel):
    # {'id':'id','user':'user','group_Id':'group_Id'}
    group_id: str = Field(
        None,
        alias="group_id",
        title="UUID of the group associated",
        example="203b7773-543f-4e2b-9f5b-dcd17c18b50f",
    )
    user: str = Field(
        None,
        alias="user",
        title="a user",
        min_length=6,
        max_length=6,
        example="abc123",
    )
