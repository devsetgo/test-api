# -*- coding: utf-8 -*-

import pyjokes
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from com_lib.db_setup import create_db, database
from com_lib.demo_data import create_data
from com_lib.default_data import add_default_group
from com_lib.logging_config import config_logging
from endpoints.email_service import views as email_service
from endpoints.groups import views as groups
from endpoints.health import views as health
from endpoints.sillyusers import views as silly_users
from endpoints.textblob import views as textblob
from endpoints.todo import views as todo
from endpoints.tools import views as tools
from endpoints.users import views as users
from settings import (
    ADD_DEFAULT_GROUP,
    APP_VERSION,
    CREATE_SAMPLE_DATA,
    HOST_DOMAIN,
    HTTPS_ON,
    LICENSE_LINK,
    LICENSE_TYPE,
    OWNER,
    RELEASE_ENV,
    WEBSITE,
)

# config logging start
config_logging()
logger.info("API Logging initiated")
# database start
create_db()
logger.info("API database initiated")
# fastapi start
app = FastAPI(
    title="Test API",
    description="Checklist APIs",
    version=APP_VERSION,
    openapi_url="/openapi.json",
)
logger.info("API App initiated")
# Add general middelware
# Add prometheus
app.add_middleware(PrometheusMiddleware)
# Add GZip
app.add_middleware(GZipMiddleware, minimum_size=500)
# 404
four_zero_four = {404: {"description": "Not found"}}
# Endpoint routers
# Group router
app.include_router(
    groups.router, prefix="/api/v1/groups", tags=["groups"], responses=four_zero_four,
)
# Text router
app.include_router(
    textblob.router,
    prefix="/api/v1/textblob",
    tags=["textblob"],
    responses=four_zero_four,
)
# ToDo router
app.include_router(
    todo.router, prefix="/api/v1/todo", tags=["todo"], responses=four_zero_four,
)
# User router
app.include_router(
    users.router, prefix="/api/v1/users", tags=["users"], responses=four_zero_four,
)

# email_service
# app.include_router(
#     email_service.router,
#     prefix="/api/v1/email",
#     tags=["email"],
#     responses=four_zero_four,
# )
# Silly router
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses=four_zero_four,
)
# Tools router
app.include_router(
    tools.router, prefix="/api/v1/tools", tags=["tools"], responses=four_zero_four,
)
# Health router
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["system-health"],
    responses=four_zero_four,
)

"""
for future use
app.include_router(socket.router,prefix="/api/v1/websocket",
tags=["websocket"],responses=four_zero_four,)
"""


@app.on_event("startup")
async def startup_event():
    """
    Startup events for application
    """
    try:
        await database.connect()
        logger.info("Connecting to database")

    except Exception as e:
        logger.info(f"Error: {e}")
        logger.trace(f"tracing: {e}")

    # initiate log with statement
    if RELEASE_ENV.lower() == "dev":
        logger.debug("Initiating logging for API")
        logger.info(f"API initiated Release_ENV: {RELEASE_ENV}")

        if CREATE_SAMPLE_DATA == "True":
            create_data()
            logger.info("Create Data")
    else:
        logger.info(f"API initiated Release_ENV: {RELEASE_ENV}")

    if CREATE_SAMPLE_DATA == "True":
        create_data()

    if HTTPS_ON == "True":
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.warning(
            f"HTTPS is set to {HTTPS_ON} and will required HTTPS connections"
        )
    if ADD_DEFAULT_GROUP == "True":
        logger.warning(f"Adding Default group")
        await add_default_group(add_default=ADD_DEFAULT_GROUP)

    app.add_route("/api/health/metrics", handle_metrics)


@app.on_event("shutdown")
async def shutdown_event():

    try:
        await database.disconnect()
        logger.info("Disconnecting from database")
    except Exception as e:
        logger.info("Error: {error}", error=e)
        logger.trace("tracing: {exception} - {e}", error=e)

    logger.info("API shutting down")


@app.get("/")
async def root():
    """
    Root endpoint of API

    Returns:
        Redrects to openapi document
    """
    response = RedirectResponse(url="/docs")
    return response


@app.get("/joke")
async def joke(
    qty: int = Query(
        None,
        title="Pyjokes",
        description="Quantity of PyJokes (max 10)",
        ge=1,
        le=10,
        alias="qty",
        deprecated=False,
    ),
    delay: int = Query(
        None,
        title="Delay",
        description="Delay seconds (Max 121)",
        ge=1,
        le=121,
        alias="delay",
    ),
):
    """
    GET a Joke endpoint

    Keyword Arguments:
        qty {int} -- [description] max of 10 random jokes can be returened
        delay {int} -- [description] delay in API response (sleep) and
        can be 121 seconds

    Returns:
        [json] -- [description] a list of jokes
    """
    if qty is None:
        qty = 1
    jokes_result = []
    for j in range(qty):
        j = pyjokes.get_joke()
        joke = {"Joke": j}
        jokes_result.append(joke)

    results = {"PyJokes": jokes_result, "Credit": "https://pyjok.es/"}
    return results


@app.get("/information")
async def info():
    """
    API information endpoint

    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    if RELEASE_ENV.lower() == "dev":
        main_url = "http://localhost:5000"
    else:
        main_url = HOST_DOMAIN

    openapi_url = f"{main_url}/docs"
    redoc_url = f"{main_url}/redoc"
    result = {
        "App Version": APP_VERSION,
        "Environment": RELEASE_ENV,
        "Docs": {"OpenAPI": openapi_url, "ReDoc": redoc_url},
        "License": {"Type": LICENSE_TYPE, "License Link": LICENSE_LINK},
        "Application_Information": {"Owner": OWNER, "Support Site": WEBSITE},
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
