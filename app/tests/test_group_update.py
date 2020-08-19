# -*- coding: utf-8 -*-
import unittest
import secrets
from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json, open_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"

base_url = '/api/v1/groups/deactivate?delay=1'
class Test(unittest.TestCase):
    # test delay
    def test_groups_put_error_delay(self):
        url = f"{base_url}?delay=122"
        test_data = {
            "id": "123",
            "is_active": True,
        }
        response = client.put(url, json=test_data)
        assert response.status_code == 422

    # test 404
    def test_groups_put_error_not_found(self):
        url = f"{base_url}"
        test_data = {
            "id": "123",
            "is_active": True,
        }
        response = client.put(url, json=test_data)
        assert response.status_code == 404

    # test bad data
    def test_groups_put_error(self):
        url = f"{base_url}"
        test_data = {
            "id": "123",
            "is_active": "bob",
        }
        response = client.put(url, json=test_data)
        assert response.status_code == 422
    # test deactivate
    def test_groups_put_valid(self):
        group_id = open_json("test_data_group.json")
        url = f"{base_url}"
        test_data = {
            "id": group_id['id'],
            "is_active": False,
        }
        response = client.put(url, json=test_data)
        assert response.status_code == 201
    