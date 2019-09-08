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
from com_lib.pass_lib import encrypt_pass, verify_pass


class test_pass_lib(unittest.TestCase):
    def test_encrypt_password(self):
        password = "toast"
        hashed_pwd = encrypt_pass(password)

        assert type(hashed_pwd) is str

    def test_verify_password(self):
        pwd = "toast"
        crypt_pwd = encrypt_pass(pwd)

        result = verify_pass(pwd, crypt_pwd)
        assert result == True

    def test_verify_password_incorrect(self):
        pwd = "toast"
        crypt_pwd = encrypt_pass(pwd)

        pwd_fail = "toasT"
        result = verify_pass(pwd_fail, crypt_pwd)
        assert result == False

        # user_id = open_json("test_data_users.json")
        # test_data = {"user_name": user_id["user_name"], "password": user_id["password"]}
        # url = f"/api/v1/users/check-pwd/"
        # client = TestClient(app)
        # response = client.post(url, data=test_data)
        # result = response.json()
        # assert response.status_code == 200
        # assert result["result"] == True
