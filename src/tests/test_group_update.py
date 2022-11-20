# -*- coding: utf-8 -*-
import secrets
import unittest

from fastapi.testclient import TestClient

from dsg_lib.file_functions import open_json
from src.main import app

client = TestClient(app)
directory_to__files: str = "data"

base_url: str = "/api/v1/groups"


class Test(unittest.TestCase):

    # State 422
    def test_groups_get_state_not_set(self):

        g_id: str = secrets.token_hex(10)
        url = f"{base_url}/state?id={g_id}"
        response = client.put(url)
        assert response.status_code == 422

    # Update Activate delay error
    # def test_groups_get_activate_error_delay(self):
    #     group_id = open_json("test_data_group.json")
    #     g_id: str = group_id["id"]
    #     url = f"{base_url}/state?id={g_id}&isActive=true"
    #     response = client.put(url)
    #     assert response.status_code == 422

    # deactivate 404
    def test_groups_get_activate_not_found(self):

        g_id: str = secrets.token_hex(10)
        url = f"{base_url}/state?id={g_id}&isActive=true"
        response = client.put(url)
        assert response.status_code == 404

    # Activate
    def test_groups_get_activate(self):
        group_id = open_json("test_data_group.json")
        g_id: str = group_id["id"]
        url = f"{base_url}/state?id={g_id}&isActive=true"
        response = client.put(url)
        assert response.status_code == 201

    # Update deactivate delay error
    # def test_groups_get_deactivate_error_delay(self):
    #     group_id = open_json("test_data_group.json")
    #     g_id: str = group_id["id"]
    #     url = f"{base_url}/state?id={g_id}&delay=122&isActive=false"
    #     response = client.put(url)
    #     assert response.status_code == 422

    # deactivate 404
    def test_groups_get_deactivate_not_found(self):

        g_id: str = secrets.token_hex(10)
        url = f"{base_url}/state?id={g_id}&delay=1&isActive=false"
        response = client.put(url)
        assert response.status_code == 404

    # state
    def test_groups_get_deactivate(self):
        group_id = open_json("test_data_group.json")
        g_id: str = group_id["id"]
        url = f"{base_url}/state?id={g_id}&isActive=false"
        response = client.put(url)
        assert response.status_code == 201
