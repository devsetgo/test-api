# -*- coding: utf-8 -*-


import pyjokes
import uvicorn
from dsg_lib import logging_config
from fastapi import FastAPI, Query, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from api import group_routes as groups
from api import health_routes as health
from api import silly_routes as silly_users
from api import textblob_routes as textblob
from api import todo_routes as todo
from api import tool_routes as tools
from api import user_routes as users
from core.db_setup import create_db, database
from core.default_data import add_default_group
from core.demo_data import create_data
from core.middleware import AccessLoggerMiddleware
from settings import config_settings

# config logging start
logging_config.config_log(
    logging_directory="log",
    # or None and defaults to logging
    log_name="log.log",
    # or None and defaults to "log.log"
    logging_level=config_settings.loguru_logging_level,
    # or "info" or "debug" or "warning" or "error" or "critical" or None and defaults to "info"
    log_rotation=config_settings.loguru_retention,
    # or None and default is 10 MB
    log_retention=config_settings.loguru_retention,
    # or None and defaults to "14 Days"
    log_backtrace=config_settings.loguru_backtrace,
    # or None and defaults to False
)
logger.debug(f"config settings {dict(config_settings)}")
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
app.add_middleware(
    SessionMiddleware,
    secret_key=config_settings.secret_key,
    max_age=7200,
    same_site="lax",
    session_cookie="session_set",
    https_only=False,
)
app.add_middleware(AccessLoggerMiddleware, user_identifier="id")

# Endpoint routers
router_responses: dict = {
    302: {"description": "The item was moved"},
    400: {"description": "Bad request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Insufficient privileges"},
    404: {"description": "Not found"},
    418: {
        "I_am-a_teapot": "The server refuses the attempt to \
                brew coffee with a teapot."
    },
    429: {"description": "Rate limit exceeded"},
}
# Group router
app.include_router(
    groups.router,
    prefix="/api/v1/groups",
    tags=["groups"],
    responses=router_responses,
)

# Text router
app.include_router(
    textblob.router,
    prefix="/api/v1/textblob",
    tags=["textblob"],
    responses=router_responses,
)
# To Do router
app.include_router(
    todo.router,
    prefix="/api/v1/todo",
    tags=["todo"],
    responses=router_responses,
)
# User router
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
    responses=router_responses,
)

# Silly router
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses=router_responses,
)
# Tools router
app.include_router(
    tools.router,
    prefix="/api/v1/tools",
    tags=["tools"],
    responses=router_responses,
)
# Health router
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["system-health"],
    responses=router_responses,
)


@app.on_event("startup")
async def startup_event():
    """
    Startup events for application
    """
    try:
        # connect to database
        await database.connect()
        logger.info("Connecting to database")

    except Exception as ex:
        # log error
        logger.info(f"Error: {ex}")
        logger.trace(f"tracing: {ex}")

    # initiate log with statement
    if config_settings.release_env.lower() == "dev":
        logger.debug("initiating logging for api")
        logger.info(f"api initiated release_env: {config_settings.release_env}")

        # create sample data
        if config_settings.create_sample_data is True:
            create_data()
            logger.info("create data")
    else:
        logger.info(f"api initiated release_env: {config_settings.release_env}")

    # require HTTPS
    if config_settings.https_on is True:
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.warning(
            f"https is set to {config_settings.https_on} and will required https\
                 connections"
        )
    # add default group
    if config_settings.add_default_group is True:
        logger.warning("adding default group")
        await add_default_group(add_default=config_settings.add_default_group)

    if config_settings.prometheus_on is True:
        app.add_route("/api/health/metrics", handle_metrics)
        logger.info("prometheus route added")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shut down events
    """
    try:
        # discount database
        await database.disconnect()
        logger.info("Disconnecting from database")
    except Exception as e:
        # log exception
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
    # redirect to openapi docs
    response = RedirectResponse(url="/docs")
    return response


@app.get("/robots.txt")
async def robots():
    """
    Robots.txt endpoint

    Returns:
        Disallow all robots
    """
    data = """
    User-agent: *
    Disallow: /
    """
    return Response(content=data, media_type="application/text")


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
        le=20,
        alias="delay",
    ),
) -> dict:
    """
    GET a Joke endpoint

    Keyword Arguments:
        qty {int} -- [description] max of 10 random jokes can be returened
        delay {int} -- [description] delay in API response (sleep) and
        can be 121 seconds

    Returns:
        [json] -- [description] a list of jokes
    """
    # set to one if not set
    if qty is None:
        qty = 1
    # list to return
    jokes_result: list = []
    # create quantity of jokes
    for j in range(qty):

        j = pyjokes.get_joke()
        joke = {"Joke": j}
        jokes_result.append(joke)

    # returned dictionary of jokes and credit
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
