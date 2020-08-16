# -*- coding: utf-8 -*-
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, SecretStr, Field
from enum import Enum, IntEnum

# "groups"
# "id"
# "name"
# "description"
# date_created
# date_updated
#
# "groups_item"
# "id"
# "user"
# 'group_Id'

# Shared properties
class GroupTypeEnum(str,Enum):
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


class GroupsOut(BaseModel):
    GroupsBase
    GroupItemBase
