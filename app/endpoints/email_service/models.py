# -*- coding: utf-8 -*-
from typing import List, Optional

from pydantic import BaseModel, ByteSize, EmailStr, Field


class PostMessageError(BaseModel):
    email_id: str
    status: int
    message: str


list_email_description: str = "Each item in list must be a valid email address format."


class ReferenceDataBase(BaseModel):
    """
    Reference Data Structure
    """

    reference_id: List[str] = Field(
        None,
        alias="reference_id",
        title="Reference List",
        description="List of IDs to reference with email in database.",
    )


class NewCommBase(BaseModel):
    """
    Communication Required
    """

    sender: EmailStr = Field(
        ..., alias="Sender", title="Sender", description=list_email_description,
    )
    to: List[EmailStr] = Field(
        ..., title="To List", description=list_email_description,
    )


class ReplyCommBase(BaseModel):
    """
    Communication Required
    """

    sender: EmailStr = Field(
        ..., alias="Sender", title="Sender", description=list_email_description,
    )
    reply_to: List[EmailStr] = Field(
        ..., title="Reply To List", description=list_email_description,
    )


class CommOptionsBase(BaseModel):
    """
    Communication Options
    """

    cc: List[EmailStr] = Field(
        None, alias="cc", title="Carbon Copy List", description=list_email_description,
    )
    bcc: List[EmailStr] = Field(
        None,
        alias="bcc",
        title="Blind Carbon Copy List",
        description=list_email_description,
    )


class EmailContent(BaseModel):
    """
    Subject and Body of Email
    """

    subject: bytes = Field(..., alias="Subject", min_length=1, max_length=255)
    body: bytes = Field(..., alias="Body", min_length=1, max_length=20000)


class NewEmail(BaseModel):
    """
    Schema for sending a new email
    """

    required_communication: NewCommBase
    optional_communciation: CommOptionsBase
    email_content: EmailContent
    reference_data: ReferenceDataBase


class ReplyEmail(BaseModel):
    """
    Schema for sending a reply email
    """

    required_communication: ReplyCommBase
    optional_communciation: CommOptionsBase
    email_content: EmailContent
    reference_data: ReferenceDataBase
