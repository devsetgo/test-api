# -*- coding: utf-8 -*-
import random
import secrets
import unittest

from starlette.testclient import TestClient

from src.core.file_functions import save_json
from src.main import app

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

    def test_groups_post_error_type(self):

        test_data = {
            "name": f"test{secrets.token_hex(1)}",
            "description": f"test group {secrets.token_hex(2)}",
            "group_type": secrets.token_hex(1),
            "is_active": True,
        }

        url = f"/api/v1/groups/create"

        response = client.post(url, json=test_data)
        assert response.status_code == 400

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

    def test_groups_post_many(self):

        for _ in range(20):
            test_data = {
                "name": f"test{secrets.token_hex(4)}",
                "description": "test group",
                "group_type": "notification",
                "is_active": random.choice([True, False]),
            }
            url = f"/api/v1/groups/create"

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
