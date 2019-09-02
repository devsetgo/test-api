# -*- coding: utf-8 -*-
import datetime
import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest import mock

import pytest
import requests
import requests_mock
from loguru import logger
from requests.exceptions import Timeout

# from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json, save_json
from app.main import app

# from starlette.exceptions import HTTPException

client = TestClient(app)

directory_to__files: str = "data"


class test_todos_endpoints(unittest.TestCase):
    def test_todos_post_exception(self):
        test_data = {
            # "title": "Test",
            "userId": "123",
            "description": "test",
            "dateDue": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/"
        client = TestClient(app)
        response = client.post(url, json=test_data)
        # result = response.json()
        assert response.status_code == 422
        # data = response.json()
        # save_json("test_data_todos.json", data)

    def test_todos_post(self):
        test_data = {
            "title": "Test",
            "userId": "123",
            "description": "test",
            "dateDue": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/?delay=1"
        client = TestClient(app)
        response = client.post(url, json=test_data)
        assert response.status_code == 200
        data = response.json()
        save_json("test_data_todos.json", data)
