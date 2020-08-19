# -*- coding: utf-8 -*-
import unittest
import secrets
from starlette.testclient import TestClient

from app.com_lib.file_functions import save_json, open_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"

# api/v1/groups/list?delay=1&qty=10&offset=1&active=true&groupType=approval
class Test(unittest.TestCase):
    def test_groups_post_user_error(self):
        group_id = open_json("test_data_group.json")
        test_data = {
            "group_id": group_id["id"],
            "user": "abc1234",
        }

        url = f"/api/v1/groups/user/create"

        response = client.post(url, json=test_data)
        assert response.status_code == 422

    def test_groups_post_user(self):
        group_id = open_json("test_data_group.json")
        test_data = {
            "group_id": group_id["id"],
            "user": "abc123",
        }
        save_json("test_data_test_group_user.json", test_data)
        url = f"/api/v1/groups/user/create?delay=1"

        response = client.post(url, json=test_data)
        assert response.status_code == 201
        data = response.json()

        # save_json("test_data_group_user.json", data)
        # duplicate
        response = client.post(url, json=test_data)
        assert response.status_code == 400

    def test_groups_post_two_user(self):
        count = 1
        group_id = open_json("test_data_group.json")

        for _ in range(2):
            test_data = {
                "group_id": group_id["id"],
                "user": f"abc12{count}",
            }
            url = f"/api/v1/groups/user/create"
            count += 1
            response = client.post(url, json=test_data)
            assert response.status_code == 201

    def test_groups_post_two_user_error(self):

        test_data = {
            "group_id": "203b7773-543f-4e2b-9f5b-dcd17c18b50f",
            "user": "abc123",
        }
        url = f"/api/v1/groups/user/create"
        response = client.post(url, json=test_data)
        response = client.post(url, json=test_data)
        assert response.status_code == 400

    def test_groups_post_user(self):
        group_id = open_json("test_data_group.json")
        test_data = {
            "group_id": group_id["id"],
            "user": "abc123",
        }
        # save_json("test_data_test_group_user.json", test_data)
        url = f"/api/v1/groups/user/create?delay=1"

        response = client.post(url, json=test_data)
        assert response.status_code == 400
