# -*- coding: utf-8 -*-
import datetime
import unittest
import secrets
from fastapi.testclient import TestClient

from dsg_lib.file_functions import save_json
from src.main import app

client = TestClient(app)

directory_to__files: str = "data"
time_str = datetime.datetime.now()


class Test(unittest.TestCase):
    def test_todos_post_exception(self):
        test_data = {
            # "title": "Test",
            "user_id": "123",
            "description": "test",
            "date_due": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_todos_post(self):
        file_name = "test_data_todos.json"
        test_data = {
            "userId": "123",
            "description": "test",
            "dateDue": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/"

        response = client.post(url, json=test_data)

        state = response.status_code
        data = response.json()
        save_json(file_name, data)
        assert state == 200

    def test_todos_post(self):
        # file_name = "test_data_todos.json"
        for _ in range(10):
            test_data = {
                "userId": "123",
                "description": f"test{secrets.token_hex(2)}",
                "dateDue": "2019-08-22T23:51:28.873Z",
            }
            url = f"/api/v1/todo/create/"
            response = client.post(url, json=test_data)
            state = response.status_code
            assert state == 200
