# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from src.core.file_functions import open_json
from src.main import app

client = TestClient(app)

directory_to__files: str = "data"

test_data_todos = "test_data_todos.json"


class Test(unittest.TestCase):
    def test_todos_count_complete_delay(self):
        response = client.get(f"/api/v1/todo/list/count?delay=1&complete=true")
        assert response.status_code == 200

    def test_todos_count(self):
        response = client.get(f"/api/v1/todo/list/count")
        assert response.status_code == 200

    def test_todos_list(self):
        response = client.get(f"/api/v1/todo/list")
        assert response.status_code == 200

    def test_todos_list_options(self):
        response = client.get(f"/api/v1/todo/list?delay=1&complete=true")
        assert response.status_code == 200

    def test_todos_error_delay(self):
        response = client.get(f"/api/v1/todo/list?delay=122")
        assert response.status_code == 422

    def test_todos_id(self):
        todo_id = open_json(test_data_todos)
        response = client.get(f"/api/v1/todo/{todo_id['todo_id']}")
        assert response.status_code == 200

    def test_todos_id_delay(self):
        todo_id = open_json(test_data_todos)
        response = client.get(f"/api/v1/todo/{todo_id['todo_id']}?delay=1")
        assert response.status_code == 200

    def test_todos_put_complete_delay(self):
        todo_id = open_json(test_data_todos)
        response = client.put(f"/api/v1/todo/complete/{todo_id['todo_id']}?delay=1")
        assert response.status_code == 200

    def test_todos_delete_delay(self):
        todo_id = open_json(test_data_todos)
        response = client.delete(f"/api/v1/todo/{todo_id['todo_id']}?delay=1")
        assert response.status_code == 200
