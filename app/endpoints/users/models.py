from typing import List, Optional, Union, Set
from pydantic import BaseModel, Schema, Json, UUID1
import uuid
from datetime import datetime, timedelta
import json

# Shared properties
class UserBase(BaseModel):
    # userId: str
    firstName: str
    lastName: str
    password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    # dateCreate: datetime = None
    # isActive: Optional[bool] = True
    # isSuperuser: Optional[bool] = False


class UserBaseInDB(UserBase):
    userId: str = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    # userId: str
    firstName: str
    lastName: str
    password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    # dateCreate: datetime = None
    # isActive: bool = True


class UserBaseInDB(UserBase):
    userId: str = None


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    isActive: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    firstName: str
    lastName: str
    # password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    # dateCreate: datetime = None
    # isActive: bool = True

class UserList(UserBaseInDB):
    firstName: str
    lastName: str
    # password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    # dateCreate: datetime = None
    isActive: bool = True

