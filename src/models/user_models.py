# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import EmailStr, AnyHttpUrl
import uuid
from pydantic import BaseModel, Field, SecretStr, ValidationError, validator

sample_id: str = str(uuid.uuid4())
# Shared properties

# Optional Fields
class UserOptional(BaseModel):
    title: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="title",
        title="Title",
        example="Captain",
    )
    company: str = Field(
        None,
        min_length=1,
        max_length=50,
        alias="company",
        title="Company",
        example="Something Co.",
    )
    address: str = Field(
        None,
        min_length=3,
        max_length=50,
        alias="address",
        title="Address",
        example="123 Maple Lane",
    )
    city: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="city",
        title="City",
        example="Somewhere",
    )
    country: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="country",
        title="Country",
        example="USA",
    )
    postal: str = Field(
        None,
        min_length=1,
        max_length=20,
        alias="postal",
        title="Postal",
        example="90210",
    )
    email: EmailStr = Field(
        None,
        alias="email",
        title="email",
        example="me@example.com",
    )
    website: AnyHttpUrl = Field(
        None,
        alias="website",
        title="Website",
        example="http://example.com",
    )
    description: str = Field(
        None,
        min_length=1,
        max_length=500,
        alias="description",
        title="description",
        example="I am a thing",
    )


class UserBase(BaseModel):
    user_name: str = Field(
        ...,
        max_length=20,
        min_length=2,
        alias="user_name",
        title="Users Name",
        example="bob",
    )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="first_name",
        title="First or Given Name",
        example="Bob",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="last_name",
        title="Surname Name",
        example="Smith",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        alias="password",
        title="Password",
        example="NotLetMeIn",
    )
    optionalFields: UserOptional

    @validator("password")
    def null_byte_check(cls, v):
        if b"\x00" in v:
            raise ValueError("passwords do not match")
        return v


class UserBaseInDB(UserBase):

    user_name: str = Field(
        ...,
        alias="user_name",
        title="Users Name",
        example="bob",
    )


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_name: str = Field(
        ...,
        alias="user_name",
        title="Users Name",
        example="bob",
    )
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="first_name",
        title="First or Given Name",
        example="Bob",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="last_name",
        title="Surname Name",
        example="Smith",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        alias="password",
        title="Password",
        example="NotLetMeIn",
    )
    optionalFields: UserOptional

    @validator("password")
    def null_byte_check(cls, v):
        if b"\x00" in v:
            raise ValueError("passwords do not match")
        return v


class UserPwd(UserBase):
    user_name: str = Field(
        ...,
        alias="user_name",
        title="Users Name",
        example="bob",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        alias="password",
        title="Password",
        example="NotLetMeIn",
    )

    @validator("password")
    def null_byte_check(cls, v):
        if b"\x00" in v:
            raise ValueError("passwords do not match")
        return v


# Properties to receive via API on update
class UserDeactivate(UserBaseInDB):
    is_active: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="first_name",
        title="First or Given Name",
        example="Bob",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="last_name",
        title="Surname Name",
        example="Smith",
    )
    optionalFields: UserOptional


class UserList(UserBaseInDB):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="first_name",
        title="First or Given Name",
        example="Bob",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        alias="last_name",
        title="Surname Name",
        example="Smith",
    )
    optionalFields: UserOptional
    is_active: bool = True


class UserDeactiveModel(BaseModel):
    id: str = Field(
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
