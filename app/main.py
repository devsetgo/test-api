# -*- coding: utf-8 -*-
import pyjokes
import uvicorn
from fastapi import FastAPI
from fastapi import Query
from loguru import logger
from starlette.responses import RedirectResponse

from com_lib.logging_config import config_logging
from db_setup import create_db
from db_setup import database
from endpoints.sillyusers import views as silly_users
from endpoints.todo import views as todo
from endpoints.tools import views as tools
from endpoints.users import views as users
from health import views as health
from settings import APP_VERSION
from settings import HOST_DOMAIN
from settings import LICENSE_LINK
from settings import LICENSE_TYPE
from settings import OWNER
from settings import RELEASE_ENV
from settings import WEBSITE

# config logging start
config_logging()
logger.info("API Logging inititated")
# database start
create_db()
logger.info("API database inititated")
# fastapi start
app = FastAPI(
    title="Test API",
    description="Checklist APIs",
    version=APP_VERSION,
    openapi_url="/openapi.json",
)
logger.info("API App inititated")

four_zero_four = {404: {"description": "Not found"}}
# Endpoint routers
# ToDo router
app.include_router(
    todo.router, prefix="/api/v1/todo", tags=["todo"], responses=four_zero_four,
)
# User router
app.include_router(
    users.router, prefix="/api/v1/users", tags=["users"], responses=four_zero_four,
)
# Converter router
app.include_router(
    tools.router, prefix="/api/v1/tools", tags=["tools"], responses=four_zero_four,
)

# Silly router
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses=four_zero_four,
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

# startup events
@app.on_event("startup")
async def startup_event():

    # initiate log with statement
    if RELEASE_ENV.lower() == "dev":
        logger.debug("Inititating logging for API")
        logger.info("API inititated in Development environment")
    else:
        logger.info("API inititated in Production environment")

    try:
        await database.connect()
        logger.info("Connecting to database")

    except Exception as e:
        logger.info(f"Error: {e}")
        logger.trace(f"tracing: {e}")


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
        delay {int} -- [description] delay in API response (sleep) and can be 121 seconds

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
