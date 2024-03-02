import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):

        # REGISTER USER
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

        # EDIT USER
        new_name = "Changed Name"

        res3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(res3, 200)

        # GET USER
        res4 = requests.get(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            res4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_unauthorized(self):

        register_data = self.prepare_registration_data()

        res1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_status_code(res1, 200)
        Assertions.assert_json_has_key(res1, "id")

        user_id = self.get_json_value(res1, "id")

        new_name = "Changed Name"
        res2 = requests.put(
            f'https://playground.learnqa.ru/api/user/{user_id}',
            data={'firstName': new_name}
        )

        Assertions.assert_status_code(res2, 400)
        assert res2.text == "Auth token not supplied"

    def test_edit_just_created_user_by_another_user(self):
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

        # EDIT FIRST USER BY SECOND USER
        new_name = "Changed Name"

        res4 = requests.put(
            f"https://playground.learnqa.ru/api/user/{first_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_status_code(res4, 200)

        # GET FIRST USER
        res5 = requests.get(
            f"https://playground.learnqa.ru/api/user/{first_user_id}",
        )
        Assertions.assert_json_value_by_name(
            res5,
            "firstName",
            first_user_data["firstName"],
            "User's name was changed by another user"
        )

    def test_edit_email_without_symbol(self):

        # REGISTER USER
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

        # EDIT USER
        email = f"{register_data['email'].replace("@", "")}"

        res3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": email}
        )

        Assertions.assert_status_code(res3, 400)
        assert res3.text == 'Invalid email format'

    def test_edit_on_short_firstname(self):

        # REGISTER USER
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

        # EDIT USER
        firstName = f'{register_data['firstName'][:1]}'

        res3 = requests.put(
            f"https://playground.learnqa.ru/api/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": firstName}
        )

        Assertions.assert_status_code(res3, 400)
        Assertions.assert_json_value_by_name(
            res3,
            "error",
            "Too short value for field firstName",
            "Too short value for field firstName"
        )
