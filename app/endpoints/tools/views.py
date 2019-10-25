# -*- coding: utf-8 -*-
import asyncio
import time

from fastapi import APIRouter, FastAPI, Header, HTTPException, Path, Query,File, Form, UploadFile
from loguru import logger

from xmltodict import parse as xml_parse, unparse as xml_unparse

router = APIRouter()


@router.post("/convert-to/xml")
async def convert_xml(
    file: bytes = File(...), 
    # file: UploadFile = File(...),
):

    result = xml_parse(file)
    return result

@router.post("/convert-to/json")
async def convert_json(
    file: bytes = File(...), 
    # file: UploadFile = File(...),
):

    result = xml_unparse(file)
    return result
