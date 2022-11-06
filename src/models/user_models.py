# -*- coding: utf-8 -*-
from typing import Optional
import uuid
from pydantic import BaseModel, Field, SecretStr,ValidationError, validator

sample_id:str = str(uuid.uuid4())
# Shared properties
class UserBase(BaseModel):
    user_name: str
    first_name: str
    last_name: str
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
    
    @validator('password')
    def null_byte_check(cls, v):
        if b'\x00' in v:
            raise ValueError('passwords do not match')
        return v

class UserBaseInDB(UserBase):
    # user_id: str = None
    user_name: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str
    first_name: str
    last_name: str
    password: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    
    @validator('password')
    def null_byte_check(cls, v):
        if b'\x00' in v:
            raise ValueError('passwords do not match')
        return v


class UserPwd(UserBase):
    user_name: str
    password: SecretStr
    
    @validator('password')
    def null_byte_check(cls, v):
        if b'\x00' in v:
            raise ValueError('passwords do not match')
        return v

# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    first_name: str
    last_name: str
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
    first_name: str
    last_name: str
    title: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class UserDeactiveModel(BaseModel):
    id: str=Field(
        ...,
        alias="id",
        title="Users ID",
        example=sample_id,
    )
    is_active: bool = Field(
        False,
        alias="isActive",
        title="Status of user",
        example="false",
    )
