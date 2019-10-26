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
from app.endpoints.tools import views
from app.main import app

client = TestClient(app)

directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_xml_error(self):
        file_directory = f"{directory_to__files}/json"
        directory_path = Path.cwd().joinpath(file_directory)
        file_path = f"{directory_path}/sample.json"


        url = f"/api/v1/tools/xml-json"
        files={'files': open(file_path,'rb')}
        response = client.post(url, files=files)
        assert response.status_code == 500

    # def test_users_post(self):
    #     test_user = user_test_info()
    #     save_json("test_data_test_user.json", test_user)
    #     url = f"/api/v1/users/create/?delay=1"

    #     response = client.post(url, json=test_user)
    #     assert response.status_code == 200
    #     data = response.json()

    #     user_data = {
    #         "userId": data["userId"],
    #         "user_name": data["user_name"],
    #         "password": test_user["password"],
    #     }

    #     save_json("test_data_users.json", user_data)

    # def test_users_post_two(self):
    #     test_user = user_test_info()
    #     url = f"/api/v1/users/create/?delay=1"

    #     response = client.post(url, json=test_user)
    #     assert response.status_code == 200


# files = {'upload_file': open('file.txt','rb')}
# values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

# r = requests.post(url, files=files, data=values)