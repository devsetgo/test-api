# -*- coding: utf-8 -*-
import unittest

from starlette.testclient import TestClient

from src.core.file_functions import open_json
from src.main import app

client = TestClient(app)

directory_to__files: str = "data"

test_data_users = "test_data_users.json"
test_data_test_user = "test_data_test_user.json"


class Test(unittest.TestCase):
    def test_user_password(self):
        user_id = open_json(test_data_users)
        test_data = {"user_name": user_id["user_name"], "password": user_id["password"]}
        url = f"/api/v1/users/check-pwd/"

        response = client.post(url, data=test_data)
        result = response.json()
        assert response.status_code == 200
        assert result["result"] == True

    def test_users_count(self):

        response = client.get(f"api/v1/users/list/count")
        assert response.status_code == 200

    def test_users_count_complete_delay(self):

        response = client.get(f"api/v1/users/list/count?delay=1&active=true")
        assert response.status_code == 200

    def test_users_list_params(self):

        response = client.get(f"api/v1/users/list?delay=1&qty=100&offset=1&active=true")
        assert response.status_code == 200

    def test_users_list_offset(self):

        response = client.get(f"api/v1/users/list?qty=2")

        test_offset_1 = response.json()
        test_user_1 = test_offset_1["users"][1]
        response = client.get(f"api/v1/users/list?qty=2&offset=1")
        test_offset_2 = response.json()
        test_user_2 = test_offset_2["users"][0]
        assert response.status_code == 200
        assert test_user_1["user_id"] == test_user_2["user_id"]

    def test_users_list_param_none(self):

        response = client.get(f"/api/v1/users/list")
        assert response.status_code == 200

    def test_users_list_options(self):

        response = client.get(f"/api/v1/users/list?delay=1&qty=2&active=true")
        assert response.status_code == 200

    def test_users_list_param_all(self):
        data = open_json(test_data_test_user)
        a = data["first_name"]
        b = data["last_name"]
        c = data["title"]
        d = data["company"]
        e = data["city"]
        f = data["country"]
        g = data["postal"]
        response = client.get(
            f"/api/v1/users/list?active=true&firstname={a}&lastname={b}&title={c}&company={d}&city={e}&country={f}&postal={g}"
        )
        assert response.status_code == 200

    def test_users_error_delay(self):

        response = client.get(f"/api/v1/users/list?delay=122")
        assert response.status_code == 422

    def test_users_id(self):
        user_id = open_json(test_data_users)
        uid = user_id["user_id"]

        response = client.get(f"/api/v1/users/{uid}")
        state = response.status_code
        assert state is 200
        assert response.json() is not None

    def test_users_id_delay(self):
        user_id = open_json(test_data_users)

        response = client.get(f"/api/v1/users/{user_id['user_id']}?delay=1")
        assert response.status_code == 200

    def test_users_put_status_deactivate(self):
        user_id = open_json(test_data_users)
        test_data = {"id": user_id["user_id"], "isActive": False}
        response = client.put(f"/api/v1/users/status?delay=1", json=test_data)
        assert response.status_code == 200

    def test_users_put_status_activate(self):
        user_id = open_json(test_data_users)
        test_data = {"id": user_id["user_id"], "isActive": True}
        response = client.put(f"/api/v1/users/status", json=test_data)
        assert response.status_code == 200
