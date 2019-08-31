# -*- coding: utf-8 -*-
from fastapi import FastAPI, Path, Query, HTTPException, APIRouter, Header
import time
import datetime
import asyncio
from loguru import logger
from health.checks import check_platform, check_app_information

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_main() -> dict:
    try:
        result: dict = {"status": "up"}
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


@router.get("/details", tags=["health"])
async def health_details() -> dict:
    system_info = check_platform()
    app_modules = check_app_modules()
    try:
        result: dict = {
            "current_datetime": str(datetime.datetime.now()),
            "platform": system_info,
        }
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


@router.get("/modules", tags=["health"])
async def health_modules() -> dict:
    system_info = check_platform()
    app_info = check_app_information()
    try:
        result: dict = {
            "current_datetime": str(datetime.datetime.now()),
            "applicaton_information": app_info,
        }
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
