# -*- coding: utf-8 -*-
import unittest
import uuid

from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json
from app.main import app


client = TestClient(app)
directory_to__files: str = "data"

base_url: str = "/api/v1/groups/user/delete"


class Test(unittest.TestCase):
    def test_groups_delete_user_error(self):

        test_data = {"id": ""}
        url = f"{base_url}"
        response = client.delete(url, json=test_data)
        assert response.status_code == 422

    def test_groups_delete_user_error_entity(self):

        test_data = {"bob": str(uuid.uuid4())}
        url = f"{base_url}"
        response = client.delete(url, json=test_data)
        assert response.status_code == 422

    def test_groups_delete_user_not_found(self):

        test_data = {"id": str(uuid.uuid4())}
        url = f"{base_url}"
        response = client.delete(url, json=test_data)
        assert response.status_code == 404

    def test_groups_delete_user_super_delay(self):

        test_data = {"id": str(uuid.uuid4())}
        url = f"{base_url}?delay=122"
        response = client.delete(url, json=test_data)
        assert response.status_code == 422

    def test_groups_delete_user(self):

        group_id = open_json("test_data_group_user.json")
        test_data = {"id": group_id["id"]}
        url = f"{base_url}?delay=1"
        response = client.delete(url, json=test_data)
        assert response.status_code == 200
