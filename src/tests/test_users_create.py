# -*- coding: utf-8 -*-
import unittest

from fastapi.testclient import TestClient

from dsg_lib.file_functions import save_json
from src.core.gen_user import user_test_info
from src.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_users_post_error(self):
        test_password = "testpassword"
        user_name = f"test-user-fail"

        test_data = {
            "user_name": user_name,
            # "firstName": "string",
            "last_name": "string",
            "password": test_password,
            "title": "string",
            "company": "string",
            "address": "string",
            "city": "string",
            "country": "string",
            "phone": "string",
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
        del test_user["user_id"]
        save_json("test_data_test_user.json", test_user)
        url = f"/api/v1/users/create/"

        response = client.request(method="POST", url=url, json=test_user)
        # response = client.post(url, json=test_user)
        data = response.json()
        # error_request: dict = {"test_user": test_user, "response": data}
        # save_json("test_error.json", data=error_request)
        assert response.status_code == 201

        user_data = {
            "user_id": data["user_id"],
            "user_name": data["user_name"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"],
            "password": test_user["password"],
            "email": test_user["email"],
        }

        save_json("test_data_users.json", data=user_data)

    def test_users_post_twenty(self):
        for _ in range(20):
            test_user = user_test_info()
            url = f"/api/v1/users/create/"

            response = client.post(url, json=test_user)
            assert response.status_code != 500
