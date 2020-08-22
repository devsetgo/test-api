# -*- coding: utf-8 -*-
import json
import asyncio

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from loguru import logger
from xmltodict import parse as xml_parse
from xmltodict import unparse as xml_unparse
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse

router = APIRouter()


@router.post(
    "/spellcheck",
    tags=["textblob"],
    response_description="Spell Check",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        # 302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Not Found"},
        # 405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def convert_xml(
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
) -> dict:
    """
    convert xml document to json

    Returns:
        json object
    """
    # sleep if delay option is used
    if delay is not None:
        await asyncio.sleep(delay)

    data: dict = {"this": "that"}
    return ORJSONResponse(status_code=201, content=data)
