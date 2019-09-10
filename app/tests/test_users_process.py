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
from app.endpoints.sillyusers.gen_user import user_test_info
from app.main import app

# from starlette.exceptions import HTTPException

client = TestClient(app)

directory_to__files: str = "data"


class test_users_endpoints(unittest.TestCase):
    def test_user_password(self):
        user_id = open_json("test_data_users.json")
        test_data = {"user_name": user_id["user_name"], "password": user_id["password"]}
        url = f"/api/v1/users/check-pwd/"
        client = TestClient(app)
        response = client.post(url, data=test_data)
        result = response.json()
        assert response.status_code == 200
        assert result["result"] == True

    def test_users_count(self):
        client = TestClient(app)
        response = client.get(f"api/v1/users/list/count")
        assert response.status_code == 200

    def test_users_count_complete_delay(self):
        client = TestClient(app)
        response = client.get(f"api/v1/users/list/count?delay=1&active=true")
        assert response.status_code == 200

    def test_users_list(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list?delay=1&qty=2")
        assert response.status_code == 200

    def test_users_list_param_none(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list")
        assert response.status_code == 200

    def test_users_list_options(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list?delay=1&qty=2&active=true")
        assert response.status_code == 200

    def test_users_error_delay(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list?delay=122")
        assert response.status_code == 422

    def test_users_id(self):
        user_id = open_json("test_data_users.json")
        uid = user_id["userId"]
        client = TestClient(app)
        response = client.get(f"/api/v1/users/{uid}")
        state = response.status_code
        assert state is 200
        assert response.json() is not None

    def test_users_id_delay(self):
        user_id = open_json("test_data_users.json")
        client = TestClient(app)
        response = client.get(f"/api/v1/users/{user_id['userId']}?delay=1")
        assert response.status_code == 200

    def test_users_put_deactivate(self):
        user_id = open_json("test_data_users.json")
        client = TestClient(app)
        response = client.put(f"/api/v1/users/deactivate/{user_id['userId']}?delay=1")
        assert response.status_code == 200
