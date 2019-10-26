# -*- coding: utf-8 -*-
import asyncio
import time
import json

from fastapi import (
    APIRouter,
    FastAPI,
    Header,
    HTTPException,
    Path,
    Query,
    File,
    Form,
    UploadFile,
    
)
from starlette.responses import Response
from loguru import logger

from xmltodict import parse as xml_parse, unparse as xml_unparse

router = APIRouter()


@router.post("/xml-json")
async def convert_xml(
    # file: bytes = File(...),
    myfile: UploadFile = File(...),
):
    if myfile.content_type != "text/xml":
        error_exception = f"API requires text/xml, but file {myfile.filename} is {myfile.content_type}"
        raise HTTPException(status_code=400, detail=error_exception)

    try:
        
        contents = await myfile.read()      
        result = xml_parse(contents, encoding="utf-8", process_namespaces=True)
        logger.info(f"file {myfile.filename} converted to JSON")
        return result

    except Exception as e:
        logger.critical(f'error: {e}')
    #


@router.post("/json-xml")
async def convert_json(
    # myfile: bytes = File(...),
    myfile: UploadFile = File(...),
):
    if myfile.content_type != "application/json":
        error_exception = f"API requires application/json, but file {myfile.filename} is {myfile.content_type}"
        raise HTTPException(status_code=400, detail=error_exception)
        
    try:
        content = await myfile.read()
        new_dict = json.loads(content.decode('utf8'))
        result = xml_unparse(new_dict, pretty = True)
        logger.info(f"file {myfile.filename} converted to xml")
        return Response(content=result, media_type="application/xml")

    except Exception as e:
        logger.critical(f"error: {e}")
