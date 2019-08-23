# -*- coding: utf-8 -*-
import datetime
import os
import json
from pathlib import Path
import sys
import time
import unittest
from unittest import mock
import requests
from requests.exceptions import Timeout
import requests_mock
from loguru import logger
import pytest
from app.main import app
from app.com_lib.file_functions import open_json, save_json

# from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

# from starlette.exceptions import HTTPException

client = TestClient(app)

directory_to__files: str = "data"


class test_default_endpoints(unittest.TestCase):
    def test_users_post(self):
        test_password = "testpassword"
        name = f"test-user"
        test_data = {
            "user_name": name,
            "firstName": "string",
            "lastName": "string",
            "password": test_password,
            "title": "string",
            "company": "string",
            "address": "string",
            "city": "string",
            "country": "string",
            "postal": "string",
            "email": "string",
            "website": "string",
            "description": "string",
        }

        url = f"/api/v1/users/create/?delay=1"
        client = TestClient(app)
        response = client.post(url, json=test_data)
        assert response.status_code == 200
        data = response.json()
        save_json("test_data_users.json", data)

    def test_user_password(self):
        name = f"test-user"
        test_password = "testpassword"
        test_data = {"user_name": name, "password": test_password}

        url = f"/api/v1/users/check-pwd/"
        client = TestClient(app)
        response = client.post(url, data=test_data)
        result = response.json()
        assert response.status_code == 200
        assert result["result"] == True

    def test_users_count(self):
        client = TestClient(app)
        response = client.get(f"api/v1/todo/list/count")
        assert response.status_code == 200

    def test_users_count_complete_delay(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list/count?delay=1&complete=true")
        assert response.status_code == 200

    def test_users_list(self):
        client = TestClient(app)
        response = client.get(f"/api/v1/users/list?delay=1&qty=2")
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
        client = TestClient(app)
        response = client.get(f"/api/v1/users/{user_id['userId']}")
        assert response.status_code == 200

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

    def test_users_delete_delay(self):
        user_id = open_json("test_data_users.json")
        client = TestClient(app)
        response = client.delete(f"/api/v1/users/{user_id['userId']}?delay=1")
        assert response.status_code == 200
