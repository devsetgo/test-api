from starlette.responses import PlainTextResponse, RedirectResponse
from fastapi import FastAPI

from database import create_database
from routers import items, sillyUsers, sample
from endpoints.todo import todo
import logging
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

file_path = (os.path.abspath("logfile/file_1.log"))
logger.debug("That's it, beautiful and simple logging!")
logger.add(file_path, backtrace=True, retention="10 days",rotation="1 MB")
# logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG,filename=file_path)
# logging.info('Logging app started')
# logging.warning('An example logging message.')
# logging.warning('Another log message')

create_database()

app = FastAPI(title="Test API",
              description="API's to be used for testing and creating sample data. Parameters to include delays, random generation of data, and other useful things to help mock an application.",
              version="19.1", openapi_url="/api/v1/openapi.json")

# app.mount('/static', StaticFiles(directory='statics'), name='static')


app.include_router(
    todo.router,
    prefix="/api/v1/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    sillyUsers.router, prefix="/api/v1/silly-users", tags=["silly users"], responses={404: {"description": "Not found"}},
)
app.include_router(
    sample.router, prefix="/api/v1/sample", tags=["sample"], responses={404: {"description": "Not found"}},
)
app.include_router(
    items.router,
    prefix="/api/v1/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


# Redirect to OpenAPI doc /docs
@app.get("/")
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

# About page API 
@app.get("/about")
async def read_about():
    release_env = os.getenv('RELEASE_ENV')
    print(release_env)
    host_domain = os.getenv("HOST_DOMAIN")
    
    if release_env.lower() == 'dev':
        main_url = 'http://localhost:5000'
    else:
        main_url = host_domain

    openApi_ulr = f'{main_url}/docs'
    reDoc_ulr = f'{main_url}/redoc'
    print(openApi_ulr)

    return {'urls':
                {'OpenAPI_URL': openApi_ulr
                , 'ReDoc_URL': reDoc_ulr
                }
            ,'environment': release_env
            ,'created_by': 'Mike Ryan'
            , 'website': 'https://devsetgo.com/projects/test-api/'
            ,'licensing':
                        {'type': 'MIT'
                        , 'link': 'https://github.com/devsetgo/test-api/blob/master/LICENSE'
                        }
            }