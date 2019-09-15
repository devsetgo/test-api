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
from starlette.testclient import TestClient

from app.main import app
from com_lib.file_functions import (
    create_sample_files,
    get_data_directory_list,
    open_csv,
    open_json,
    save_csv,
    save_json,
)

client = TestClient(app)

directory_to__files: str = "data"
time_str = datetime.datetime.now()


class Test(unittest.TestCase):
    def test_todos_post_exception(self):
        test_data = {
            # "title": "Test",
            "userId": "123",
            "description": "test",
            "dateDue": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_todos_post(self):
        file_name = "test_data_todos.json"
        test_data = {
            "title": "Test",
            "userId": "123",
            "description": "test",
            "dateDue": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/?delay=1"

        response = client.post(url, json=test_data)
        data = response.json()
        state = response.status_code
        data = response.json()
        save_json(file_name, data)
        save_json("test_data_todos.json", data)
        assert state == 200
