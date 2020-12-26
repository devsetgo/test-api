# -*- coding: utf-8 -*-
import datetime

from cpuinfo import get_cpu_info
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette_exporter import handle_metrics

from endpoints.health.checks import get_processes

router = APIRouter()

# TODO: detmine method to shutdown/restart python application
# TODO: Determine method to get application uptime

router.add_route("/metrics", handle_metrics)


@router.get("/status", tags=["system-health"], response_class=ORJSONResponse)
async def health_main() -> dict:
    """
    GET status, uptime, and current datetime

    Returns:
        dict -- [status: UP, uptime: seconds current_datetime: datetime.now]
    """
    result: dict = {"status": "UP"}
    return result


@router.get("/system-info", tags=["system-health"])
async def health_status() -> dict:
    """
    GET Request for CPU and process data

    Returns:
        dict -- [current_datetime: datetime.now, system information:
        Python and System Information]
    """

    try:
        system_info = get_cpu_info()
        result: dict = {
            "current_datetime": str(datetime.datetime.now()),
            "system_info": system_info,
        }
        logger.info("GET system info")
        return result
        # TODO: make more specific Exception
        # BODY: Exception is generic and should be more specific or removed.
    except Exception as e:
        logger.error(f"Error: {e}")


@router.get("/processes", tags=["system-health"])
async def health_processes() -> dict:
    """
    GET running processes and filter by python processes

    Returns:
        dict -- [pid, name, username]
    """
    try:
        system_info = get_processes()
        result: dict = {
            "current_datetime": str(datetime.datetime.now()),
            # "note": "this is filter to only return, python, gunicorn,
            # uvicorn, hypercorn, and daphne pids for security",
            "running_processes": system_info,
        }
        logger.info("GET processes")
        return result
    except Exception as e:
        logger.error(f"Error: {e}")


# from functools import lru_cache
from settings import Settings

# @lru_cache()
# def get_settings():
#     return settings.Settings()


@router.get("/configuration")
async def info():
    """
    API information endpoint

    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    # if config.release_env.lower() == "dev":
    #     main_url = "http://localhost:5000"
    # else:
    #     main_url = config.host_domain

    # openapi_url = f"{main_url}/docs"
    # redoc_url = f"{main_url}/redoc"
    result = {
        # "docs": {"OpenAPI": openapi_url, "ReDoc": redoc_url},
        "configuraton": Settings(),
        # "app version": settings.app_version,
        # "environment": settings.release_env,
        # "license": {"type": settings.license_type, "license link": settings.license_link},
        # "application_information": {"owner": settings.owner, "support site": settings.website},
    }
    return result
