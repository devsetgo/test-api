# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Set, Union

from pydantic import UUID1, BaseModel, Json, Schema, SecretStr


# Shared properties
class UserBase(BaseModel):
    user_name: str
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


class UserBaseInDB(UserBase):
    user_id: str = None
    user_name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str
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


class UserPwd(UserBase):
    user_name: str
    password: SecretStr


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    firstName: str
    lastName: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None


class UserList(UserBaseInDB):
    firstName: str
    lastName: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    isActive: bool = True
