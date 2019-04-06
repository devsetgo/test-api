from fastapi import FastAPI
from routers import items, users, sample


app = FastAPI(title="Test API",
              description="API's to be used for testing and creating sample data. Parameters to include delays, random generation of data, and other useful things to help mock an application.",
              version="19.1", openapi_url="/api/v1/openapi.json")

app.include_router(
    users.router, prefix="/api/v1/users", tags=["users"], responses={404: {"description": "Not found"}},
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


@app.get("/")
async def read_root():

    oa = f'https://test-api.devsetgo.com/docs'
    rd = f'https://test-api.devsetgo.com/redoc'
    loa = f'http://localhost:5000/docs'
    lrd = f'http://localhost:5000/redoc'
    return {'production':
                {'OpenAPI_URL': oa, 'ReDoc_URL': rd}
            ,
            'test': 
                {'OpenAPI_URL': loa, 'ReDoc_URL': lrd}
            }

@app.get("/about")
async def read_root():

    oa = f'https://test-api.devsetgo.com/docs'
    rd = f'https://test-api.devsetgo.com/redoc'
    loa = f'http://localhost:5000/docs'
    lrd = f'http://localhost:5000/redoc'
    return {'production':
                {'OpenAPI_URL': oa, 'ReDoc_URL': rd}
            ,
            'test': 
                {'OpenAPI_URL': loa, 'ReDoc_URL': lrd}
            }