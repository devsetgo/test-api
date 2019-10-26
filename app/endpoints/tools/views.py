# -*- coding: utf-8 -*-
import asyncio
import json
import time

from fastapi import (
    APIRouter,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    UploadFile,
)
from loguru import logger
from starlette.responses import Response
from xmltodict import parse as xml_parse
from xmltodict import unparse as xml_unparse

router = APIRouter()


@router.post("/xml-json")
async def convert_xml(
    # myfile: bytes = File(...),
    myfile: UploadFile = File(...),
):

    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    if file_named.endswith(".xml", 4) is not True:
        error_exception = (
            f"API requires a XML docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    try:

        contents = await myfile.read()
        # contents = myfile
        result = xml_parse(
            contents, encoding="utf-8", process_namespaces=True, xml_attribs=True
        )
        logger.info(f"file converted to JSON")
        return result

    except Exception as e:
        logger.critical(f"error: {e}")
        err = str(e)
        if err.startswith("syntax error") == True:
            error_exception = f"The syntax of the object is not valid"
            raise HTTPException(status_code=400, detail=error_exception)


@router.post("/json-xml")
async def convert_json(
    # myfile: bytes = File(...),
    myfile: UploadFile = File(...),
):
    # if myfile.content_type != "application/json":
    #     error_exception = f"API requires application/json, but file {myfile.filename} is {myfile.content_type}"
    #     raise HTTPException(status_code=400, detail=error_exception)

    # try:
    #     content = await myfile.read()
    #     new_dict = json.loads(content.decode("utf8"))
    #     result = xml_unparse(new_dict, pretty=True)
    #     logger.info(f"file {myfile.filename} converted to xml")
    #     return Response(content=result, media_type="application/xml")

    # except Exception as e:
    #     logger.critical(f"error: {e}")
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    if file_named.endswith(".json", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    try:

        content = await myfile.read()
        new_dict = json.loads(content.decode("utf8"))
        result = xml_unparse(new_dict, pretty=True)
        logger.info(f"file converted to JSON")
        return result

    except Exception as e:
        logger.critical(f"error: {e}")
        err = str(e)
        # or e is not None:
        if err.startswith("Extra data") == True or e is not None:
            error_exception = f"The syntax of the object is not valid. Error: {e}"
            raise HTTPException(status_code=400, detail=error_exception)
