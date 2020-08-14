# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from loguru import logger

from endpoints.email_service.models import (
    NewEmail,
    PostMessageError,
    ReplyEmail,
)

router = APIRouter()

four_zero_eight: dict = {
    "email_id": str(uuid.uuid4()),
    "status": 408,
    "message": "email id not found",
}


@router.post(
    "/new",
    status_code=201,
    responses={
        408: {
            "model": PostMessageError,
            "description": "The message failed to connect to SMTP Server",
            "content": {"application/json": {"example": four_zero_eight}},
        },
        201: {
            "description": "Message accepted and processed",
            "content": {"application/json": {"example": four_zero_eight}},
        },
    },
)
async def email_new(new_email: NewEmail):

    logger.debug(new_email)
    json_data = jsonable_encoder(new_email)
    return ORJSONResponse(content=json_data, status_code=status.HTTP_201_CREATED)


@router.post(
    "/reply",
    status_code=201,
    responses={
        408: {
            "model": PostMessageError,
            "description": "The message failed to connect to SMTP Server",
            "content": {"application/json": {"example": four_zero_eight}},
        },
        201: {
            "description": "Message accepted and processed",
            "content": {"application/json": {"example": four_zero_eight}},
        },
    },
)
async def email_reply(reply_email: ReplyEmail):

    logger.debug(reply_email)

    json_data = {
        "email_id": str(uuid.uuid4()),
        "status": "queued for delivery",
        "date_created": str(datetime.now()),
    }
    return ORJSONResponse(content=json_data, status_code=status.HTTP_201_CREATED)


@router.get("/{email_id}", status_code=200)
async def email_by_id(
    email_id: str = Path(
        ..., title="The email id to be searched for", alias="email_id"
    ),
):

    logger.debug(email_id)
    json_data = jsonable_encoder(email_id)
    return ORJSONResponse(content=json_data, status_code=200)
