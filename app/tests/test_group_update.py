# -*- coding: utf-8 -*-
import secrets
import unittest

from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"

base_url: str = "/api/v1/groups"

class Test(unittest.TestCase):

    # Update Activate delay error
    def test_groups_get_activate_error_delay(self):
        group_id = open_json("test_data_group.json")
        g_id: str=group_id['id']
        url = f"{base_url}/activate?id={g_id}&delay=122"
        response = client.put(url)
        assert response.status_code == 422

    # deactivate 404
    def test_groups_get_activate_not_found(self):
        group_id = open_json("test_data_group.json")
        g_id: str = secrets.token_hex(10) #group_id['id']
        url = f"{base_url}/activate?id={g_id}&delay=1"
        response = client.put(url)
        assert response.status_code == 404

    # Activate 
    def test_groups_get_activate(self):
        group_id = open_json("test_data_group.json")
        g_id: str = group_id['id']
        url = f"{base_url}/activate?id={g_id}"
        response = client.put(url)
        assert response.status_code == 201

    # Update deactivate delay error
    def test_groups_get_deactivate_error_delay(self):
        group_id = open_json("test_data_group.json")
        g_id: str=group_id['id']
        url = f"{base_url}/deactivate?id={g_id}&delay=122"
        response = client.put(url)
        assert response.status_code == 422

    # deactivate 404
    def test_groups_get_deactivate_not_found(self):
        group_id = open_json("test_data_group.json")
        g_id: str = secrets.token_hex(10) #group_id['id']
        url = f"{base_url}/deactivate?id={g_id}&delay=1"
        response = client.put(url)
        assert response.status_code == 404

    # deactivate 
    def test_groups_get_deactivate(self):
        group_id = open_json("test_data_group.json")
        g_id: str = group_id['id']
        url = f"{base_url}/deactivate?id={g_id}"
        response = client.put(url)
        assert response.status_code == 201