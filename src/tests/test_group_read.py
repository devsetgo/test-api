# -*- coding: utf-8 -*-
import unittest

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)
directory_to__files: str = "data"

# api/v1/groups/list?delay=1&qty=10&offset=1&active=true&groupType=approval
class Test(unittest.TestCase):
    def test_groups_get_list_error_ignore_input(self):
        url = f"/api/v1/groups/list?bob=123"

        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list_error_qty(self):
        url = f"/api/v1/groups/list?qty=501"

        response = client.get(url)
        assert response.status_code == 422

    def test_groups_get_list_error_type(self):
        url = f"/api/v1/groups/list?groupType=bob"

        response = client.get(url)
        assert response.status_code == 422

    def test_groups_get_list_all_options(self):

        url = f"/api/v1/groups/list?qty=10&offset=1&active=true&groupType=approval"

        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list(self):

        url = f"/api/v1/groups/list"

        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list_name(self):

        url = f"/api/v1/groups/list?groupName=test"

        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list_count(self):

        url = f"/api/v1/groups/list/count"
        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list_count_error_delay(self):

        url = f"/api/v1/groups/list/count"
        response = client.get(url)
        assert response.status_code == 200

    def test_groups_get_list_count_all_options(self):

        group_type: list = ["approval", "notification"]
        active_state: list = ["true", "false"]
        for g in group_type:
            for a in active_state:
                url = f"/api/v1/groups/list/count?active={a}&groupType={g}"

                response = client.get(url)
                assert response.status_code == 200

    def test_groups_get_list_count_invalid_group(self):

        url = f"/api/v1/groups/list/count?groupType=bob"

        response = client.get(url)
        assert response.status_code == 422

    def test_groups_get_list_count_invalid_group(self):

        url = f"/api/v1/groups/list/?groupType=bob"

        response = client.get(url)
        assert response.status_code == 422
