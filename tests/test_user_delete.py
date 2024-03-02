import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):

    def test_delete_user_by_id_2(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        res1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(res1, "auth_sid")
        token = self.get_headers(res1, "x-csrf-token")
        user_id = self.get_json_value(res1, "user_id")

        res2 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_status_code(res2, 400)
        assert res2.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'


    def test_succeess_delete_user(self):

        register_data = self.prepare_registration_data()

        res1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(res1, 200)
        Assertions.assert_json_has_key(res1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(res1, "id")

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password,
        }

        res2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(res2, "auth_sid")
        token = self.get_headers(res2, "x-csrf-token")

        res3 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_status_code(res3, 200)

        res4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        assert res4.text == 'User not found'

    def test_delete_user_when_auth_another_user(self):

        # REGISTER FIRST USER
        first_user_data = self.prepare_registration_data()
        res1 = requests.post("https://playground.learnqa.ru/api/user/", data=first_user_data)

        Assertions.assert_status_code(res1, 200)
        Assertions.assert_json_has_key(res1, "id")

        first_user_id = self.get_json_value(res1, "id")

        # REGISTER SECOND USER
        second_user_data = self.prepare_registration_data()
        res2 = requests.post("https://playground.learnqa.ru/api/user/", data=second_user_data)

        Assertions.assert_status_code(res2, 200)
        Assertions.assert_json_has_key(res2, "id")

        second_user_id = self.get_json_value(res2, "id")

        # LOGIN SECOND USER
        login_data = {
            'email': second_user_data['email'],
            'password': second_user_data['password'],
        }
        res3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(res3, "auth_sid")
        token = self.get_headers(res3, "x-csrf-token")

        res4 = requests.delete(
            f"https://playground.learnqa.ru/api/user/{first_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_status_code(res4, 200)


