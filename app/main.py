import pyjokes
import uvicorn
from fastapi import APIRouter, FastAPI, Header, HTTPException, Path, Query
from loguru import logger
from starlette.responses import PlainTextResponse, RedirectResponse

from com_lib.logging_config import config_logging
from settings import (
    APP_VERSION,
    HOST_DOMAIN,
    LICENSE_LINK,
    LICENSE_TYPE,
    OWNER,
    RELEASE_ENV,
    WEBSITE,
)

# from endpoints.todo import views as todo
from endpoints.sillyusers import views as silly_users

# from endpoints.users import views as users


config_logging()
logger.info("API Logging inititated")
app = FastAPI(
    title="Test API",
    description="Checklist APIs",
    version=APP_VERSION,
    openapi_url="/openapi.json",
)
logger.info("API App inititated")


# Endpoint routers
# app.include_router(
#     todo.router,
#     prefix="/api/v1/todo",
#     tags=["todo"],
#     responses={404: {"description": "Not found"}},
# )
# app.include_router(
#     users.router,
#     prefix="/api/v1/users",
#     tags=["users"],
#     responses={404: {"description": "Not found"}},
# )
app.include_router(
    silly_users.router,
    prefix="/api/v1/silly-users",
    tags=["Silly Users"],
    responses={404: {"description": "Not found"}},
)
# app.include_router(socket.router,prefix="/api/v1/websocket",tags=["websocket"],responses={404: {"description": "Not found"}},)


@app.get("/")
async def root():
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
    if qty == None:
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

    if RELEASE_ENV.lower() == "dev":
        main_url = "http://localhost:5000"
    else:
        main_url = HOST_DOMAIN

    openApi_ulr = f"{main_url}/docs"
    reDoc_ulr = f"{main_url}/redoc"
    joke = pyjokes.get_joke()
    result = {
        "App Version": APP_VERSION,
        "Environment": RELEASE_ENV,
        "Docs": {"OpenAPI": openApi_ulr, "ReDoc": reDoc_ulr},
        "License": {"Type": LICENSE_TYPE, "License Link": LICENSE_LINK},
        "Application_Information": {"Owner": OWNER, "Support Site": WEBSITE},
        "PyJoke": joke,
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")