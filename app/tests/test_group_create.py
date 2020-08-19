# -*- coding: utf-8 -*-
import unittest
import secrets
from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"

# api/v1/groups/list?delay=1&qty=10&offset=1&active=true&groupType=approval
class Test(unittest.TestCase):
    def test_groups_post_error(self):

        test_data = {
            "name": "test 1",
            "description": "test group",
            "group_type": "approval",
            "is_active": True,
        }

        url = f"/api/v1/groups/create"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_groups_post(self):
        test_data = {
            "name": f"test{secrets.token_hex(4)}",
            "description": "test group",
            "group_type": "approval",
            "is_active": True,
        }
        save_json("test_data_test_user.json", test_data)
        url = f"/api/v1/groups/create?delay=1"

        response = client.post(url, json=test_data)
        assert response.status_code == 201
        data = response.json()

        save_json("test_data_group.json", data)
        # duplicate
        response = client.post(url, json=test_data)
        assert response.status_code == 400

    def test_groups_post_two(self):
        count = 10
        for _ in range(2):
            test_data = {
                "name": f"test{secrets.token_hex(4)}",
                "description": "test group",
                "group_type": "notification",
                "is_active": False,
            }
            url = f"/api/v1/groups/create"
            count += 10
            response = client.post(url, json=test_data)
            assert response.status_code == 201

    def test_groups_post_two_error(self):

        test_data = {
            "name": f"test{secrets.token_hex(4)}",
            "description": "test group",
            "group_type": "notification",
            "is_active": False,
        }
        url = f"/api/v1/groups/create"
        response = client.post(url, json=test_data)
        response = client.post(url, json=test_data)
        assert response.status_code == 400

    def test_groups_post(self):
        test_data = {
            "name": f"test{secrets.token_hex(4)}",
            "description": "test group",
            "group_type": "test",
            "is_active": True,
        }
        save_json("test_data_test_user.json", test_data)
        url = f"/api/v1/groups/create?delay=1"

        response = client.post(url, json=test_data)
        assert response.status_code == 400
