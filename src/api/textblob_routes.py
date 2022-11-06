# -*- coding: utf-8 -*-
import asyncio

from fastapi import APIRouter, File, Query, UploadFile, HTTPException
from fastapi.responses import ORJSONResponse
from loguru import logger
from textblob import TextBlob

router = APIRouter()
title = "Delay in Seconds"


@router.post(
    "/spellcheck",
    tags=["textblob"],
    response_description="Spell Check",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Not Found"},
        405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def spell_check(
    myfile: UploadFile = File(..., description="File to spell check"),
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=20,
        alias="delay",
    ),
) -> dict:

    # sleep if delay option is used
    if delay is not None:
        logger.info(f"Delay of {delay} seconds invoked")
        await asyncio.sleep(delay)
        logger.info(f"Delay of {delay} seconds completed")

    try:
        file_text = await myfile.read()
        text_decoded = file_text.decode("utf-8")
    except Exception as e:
        error_note = {"message": f"File Read Error: {e}"}
        logger.error(error_note)
        raise HTTPException(status_code=422, detail=error_note)

    tb = TextBlob(text_decoded)
    original_text = text_decoded
    logger.debug(f"file text size {len(original_text)}")

    if len(original_text) == 0:
        error: dict = {"error": "The file is empty or unreadable"}
        logger.warning(error)
        return ORJSONResponse(status_code=400, content=error)

    data: dict = {
        "original": original_text,
        "corrected": {
            "raw": tb.correct().raw,
            "string": tb.correct().string,
            "stripped": tb.correct().stripped,
        },
    }
    return ORJSONResponse(status_code=201, content=data)


@router.post(
    "/sentiment",
    tags=["textblob"],
    response_description="Spell Check",
    response_class=ORJSONResponse,
    status_code=201,
    responses={
        302: {"description": "Incorrect URL, redirecting"},
        400: {"description": "Bad Request"},
        422: {"description": "Validation Error"},
        404: {"description": "Not Found"},
        405: {"description": "Method not allowed"},
        500: {"description": "All lines are busy, try again later."},
    },
)
async def sentiment_check(
    myfile: UploadFile = File(..., description="File to get sentiment"),
    delay: int = Query(
        None,
        title=title,
        description="Seconds to delay (max 121)",
        ge=1,
        le=20,
        alias="delay",
    ),
) -> dict:
    # sleep if delay option is used
    if delay is not None:
        logger.info(f"Delay of {delay} seconds invoked")
        await asyncio.sleep(delay)
        logger.info(f"Delay of {delay} seconds completed")

    try:
        file_text = await myfile.read()
        text_decoded = file_text.decode("utf-8")
    except Exception as e:
        error_note = {"message": f"File Read Error: {e}"}
        logger.error(error_note)
        raise HTTPException(status_code=422, detail=error_note)

    tb = TextBlob(text_decoded)
    original_text = text_decoded

    if len(original_text) == 0:
        error: dict = {"error": "The file is empty or unreadable"}
        logger.warning(error)
        return ORJSONResponse(status_code=400, content=error)

    data: dict = {
        "original": original_text,
        "sentiment": {
            "polarity": tb.sentiment.polarity,
            "subjectivity": tb.sentiment.subjectivity,
        },
    }
    return ORJSONResponse(status_code=201, content=data)
