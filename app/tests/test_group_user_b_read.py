# -*- coding: utf-8 -*-
import secrets
import unittest

from starlette.testclient import TestClient

from app.com_lib.file_functions import open_json
from app.main import app

client = TestClient(app)
directory_to__files: str = "data"

# api/v1/groups/list?delay=1&qty=10&offset=1&active=true&groupType=approval
class Test(unittest.TestCase):
    # get group
    def test_groups_get_group_delay(self):
        group_id = open_json("test_data_group.json")
        url = f"/api/v1/groups/group?groupId={group_id['id']}&delay=1"
        response = client.get(url)
        assert response.status_code == 200

    # get group
    def test_groups_get_group(self):
        group_id = open_json("test_data_group.json")
        url = f"/api/v1/groups/group?groupId={group_id['id']}"

        response = client.get(url)
        assert response.status_code == 200

    # get delay error
    def test_groups_get_group_delay_error(self):
        group_id = open_json("test_data_group.json")
        url = f"/api/v1/groups/group?groupId={group_id['id']}&delay=122"

        response = client.get(url)
        assert response.status_code == 422

    # get id not found
    def test_groups_get_group_not_found(self):
        # group_id = open_json("test_data_group.json")
        url = f"/api/v1/groups/group?groupId=bob"

        response = client.get(url)
        assert response.status_code == 404

    def test_groups_get_group_name_not_found(self):
        # group_id = open_json("test_data_group.json")
        url = f"/api/v1/groups/group?groupName={secrets.token_hex(2)}"

        response = client.get(url)
        assert response.status_code == 404

    def test_groups_get_group_name(self):

        get_groups = client.get("api/v1/groups/list?active=true")

        groups = get_groups.json()
        name = groups["groups"][0]["name"]
        url = f"/api/v1/groups/group?groupName={name}"
        response = client.get(url)
        assert response.status_code == 200
