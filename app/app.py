# -*- coding: utf-8 -*-
from starlette.responses import PlainTextResponse, RedirectResponse
from fastapi import FastAPI

# database
from db_setup import createDB, disconnectDB, connectDB, database

# List of ENDPOINTS for routers
from endpoints.todo import views as todo
from endpoints.sillyusers import views as silly_users
from endpoints.users import views as users

# from endpoints.websocket import views as socket
# Internal Library imports
import os

# External Library imports
from loguru import logger
from dotenv import load_dotenv
import databases


load_dotenv()
App_Ver = os.getenv("APP_VERSION")
# Set the environment configuration
app_env = os.getenv("RELEASE_ENV")
backtrace = os.getenv("LOGURU_BACKTRACE")
retention = os.getenv("LOGURU_RETENTION")
rotatation = os.getenv("LOGURU_ROTATION")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


createDB()
# database = databases.Database(SQLALCHEMY_DATABASE_URI)

app = FastAPI(
    title="Test API",
    description="Checklist APIs",
    version=App_Ver,
    openapi_url="/api/v1/openapi.json",
)

# Endpoint routers
app.include_router(
    todo.router,
    prefix="/api/v1/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["silly users"],
    responses={404: {"description": "Not found"}},
)
# app.include_router(socket.router,prefix="/api/v1/websocket",tags=["websocket"],responses={404: {"description": "Not found"}},)


@app.on_event("startup")
async def startup_event():

    # loguru settings
    file_path = os.path.abspath("logfile/file_1.log")  # File path
    # loguru configuration
    logger.add(file_path, backtrace=backtrace, retention=retention, rotation=rotatation)
    # initiate log with statement
    if app_env.lower() == "dev":
        logger.debug("Inititating logging for API")
        logger.info("API inititated in Development environment")
    else:
        logger.info("API inititated in Production environment")

    try:
        await database.connect()
        logger.info("Connecting to database")

    except Exception as e:
        logger.info("Error: {error}", error=e)
        logger.trace("tracing: {exception} - {e}", error=e)


@app.on_event("shutdown")
async def shutdown_event():

    try:
        await database.disconnect()
        logger.info("Disconnecting from database")
    except Exception as e:
        logger.info("Error: {error}", error=e)
        logger.trace("tracing: {exception} - {e}", error=e)

    logger.info("API shutting down")


# Redirect to OpenAPI doc /docs


@app.get("/")
async def read_root():
    response = RedirectResponse(url="/docs")
    return response


# About page API


@app.get("/information")
async def read_about():
    release_env = os.getenv("RELEASE_ENV")
    print(release_env)
    host_domain = os.getenv("HOST_DOMAIN")
    owner = os.getenv("OWNER")
    website = os.getenv("WEBSITE")
    license_type = os.getenv("LICENSE_TYPE")
    license_link = os.getenv("LICENSE_LINK")
    if release_env.lower() == "dev":
        main_url = "http://localhost:5000"
    else:
        main_url = host_domain

    openApi_ulr = f"{main_url}/docs"
    reDoc_ulr = f"{main_url}/redoc"
    print(openApi_ulr)

    return {
        "urls": {"OpenAPI_URL": openApi_ulr, "ReDoc_URL": reDoc_ulr},
        "environment": release_env,
        "created_by": owner,
        "website": website,
        "licensing": {"type": license_type, "link": license_link},
    }
