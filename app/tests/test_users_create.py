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
from app.com_lib.file_functions import open_json, save_json
from app.endpoints.sillyusers.gen_user import user_test_info
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"


class TestUsersCreate(unittest.TestCase):
    def test_users_post_error(self):
        test_password = "testpassword"
        user_name = f"test-user-fail"

        test_data = {
            "user_name": user_name,
            # "firstName": "string",
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

        url = f"/api/v1/users/create/"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_users_post(self):
        test_user = user_test_info()
        save_json("test_data_test_user.json", test_user)
        url = f"/api/v1/users/create/?delay=1"

        response = client.post(url, json=test_user)
        assert response.status_code == 200
        data = response.json()

        user_data = {
            "userId": data["userId"],
            "user_name": data["user_name"],
            "password": test_user["password"],
        }

        save_json("test_data_users.json", user_data)

    def test_users_post_two(self):
        test_user = user_test_info()
        url = f"/api/v1/users/create/?delay=1"

        response = client.post(url, json=test_user)
        assert response.status_code == 200
