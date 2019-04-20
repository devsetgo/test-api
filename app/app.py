import uvicorn
from fastapi import FastAPI
from main import app


if __name__ == "__main__":
    uvicorn.run(app, port=5000, debug=True, access_log=True)