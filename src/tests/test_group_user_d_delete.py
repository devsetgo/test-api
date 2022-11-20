# -*- coding: utf-8 -*-
import unittest
import uuid

from fastapi.testclient import TestClient

from dsg_lib.file_functions import open_json
from src.main import app

client = TestClient(app)
directory_to__files: str = "data"


class Test(unittest.TestCase):
    def test_groups_delete_user_error(self):

        test_data = {"id": ""}
        url: str = "/api/v1/groups/user/delete"
        response = client.delete(url=url, json=test_data)
        assert response.status_code == 422

    def test_groups_delete_user_error_entity(self):

        test_data = {"bob": str(uuid.uuid4())}
        url: str = "/api/v1/groups/user/delete"
        response = client.delete(url=url, json=test_data)
        assert response.status_code == 422

    def test_groups_delete_user_not_found(self):
        group_id = open_json("test_data_group_user.json")
        test_data = {"id": str(uuid.uuid4()), "group_id": group_id["group_id"]}
        url: str = "/api/v1/groups/user/delete"
        response = client.delete(url=url, json=test_data)
        assert response.status_code == 404

    # def test_groups_delete_user_super_delay(self):

    #     test_data = {"id": str(uuid.uuid4())}
    #     url: str = "/api/v1/groups/user/delete"
    #     response = client.delete(url=url, json=test_data)
    #     assert response.status_code == 422

    def test_groups_delete_user(self):

        group_id = open_json("test_data_group_user.json")
        test_data = {"id": group_id["id"], "group_id": group_id["group_id"]}
        url: str = "/api/v1/groups/user/delete"
        response = client.delete(url=url, open_json=test_data)
        # response = client.delete(url, json=test_data)
        assert response.status_code == 200
