import random

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        expected_fields = ["email", "firstName", "lastName"]
        response = requests.get("https://playground.learnqa.ru/api/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_keys(response, expected_fields)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        res1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_headers(res1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(res1, "user_id")

        res2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(res2, expected_fields)

    def test_user_auth_but_get_data_another_user(self):
        expected_fields = ["email", "firstName", "lastName"]
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        res1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_headers(res1, "x-csrf-token")
        user_id = 2
        headers = {
            'Cookie': f'auth_sid={auth_sid}; token={token}'
        }

        res2 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
                headers=headers,
        )

        Assertions.assert_json_has_key(res2, "username")
        Assertions.assert_json_has_not_keys(res2, expected_fields)