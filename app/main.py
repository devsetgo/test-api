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
from com_lib.default_data import add_default_group
from com_lib.demo_data import create_data
from com_lib.logging_config import config_logging
from endpoints.groups import views as groups
from endpoints.health import views as health
from endpoints.sillyusers import views as silly_users
from endpoints.textblob import views as textblob
from endpoints.todo import views as todo
from endpoints.tools import views as tools
from endpoints.users import views as users
from settings import config_settings

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
    version=config_settings.app_version,
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
    groups.router,
    prefix="/api/v1/groups",
    tags=["groups"],
    responses=four_zero_four,
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
    todo.router,
    prefix="/api/v1/todo",
    tags=["todo"],
    responses=four_zero_four,
)
# User router
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
    responses=four_zero_four,
)

# Silly router
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses=four_zero_four,
)
# Tools router
app.include_router(
    tools.router,
    prefix="/api/v1/tools",
    tags=["tools"],
    responses=four_zero_four,
)
# Health router
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["system-health"],
    responses=four_zero_four,
)


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
    if config_settings.release_env.lower() == "dev":
        logger.debug("initiating logging for api")
        logger.info(f"api initiated release_env: {config_settings.release_env}")

        if config_settings.create_sample_data == True:
            create_data()
            logger.info("create data")
    else:
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    if config_settings.create_sample_data == True:
        create_data()

    if config_settings.https_on == True:
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.warning(
            f"https is set to {config_settings.https_on} and will required https connections"
        )
    if config_settings.add_default_group == True:
        logger.warning("adding default group")
        await add_default_group(add_default=config_settings.add_default_group)

    if config_settings.prometheus_on == True:
        app.add_route("/api/health/metrics", handle_metrics)
        logger.info("prometheus route added")


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


@app.get("/info")
async def information():
    """
    API information endpoint

    Returns:
        [json] -- [description] app version, environment running in (dev/prd),
        Doc/Redoc link, Lincense information, and support information
    """
    if config_settings.release_env.lower() == "dev":
        main_url = "http://localhost:5000"
    else:
        main_url = config_settings.host_domain

    openapi_url = f"{main_url}/docs"
    redoc_url = f"{main_url}/redoc"
    result = {
        "docs": {"OpenAPI": openapi_url, "ReDoc": redoc_url},
        "app version": config_settings.app_version,
        "environment": config_settings.release_env,
        "license": {
            "type": config_settings.license_type,
            "license link": config_settings.license_link,
        },
        "application_information": {
            "owner": config_settings.owner,
            "support site": config_settings.website,
        },
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
