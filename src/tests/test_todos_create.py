# -*- coding: utf-8 -*-
import datetime
import unittest

from starlette.testclient import TestClient

from app.main import app
from core.file_functions import save_json

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
            "title": "Test",
            "user_id": "123",
            "description": "test",
            "date_due": "2019-08-22T23:51:28.873Z",
        }
        url = f"/api/v1/todo/create/?delay=1"

        response = client.post(url, json=test_data)

        state = response.status_code
        data = response.json()
        save_json(file_name, data)
        assert state == 200
