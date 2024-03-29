import allure
import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.feature("Authorization")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        res1 = MyRequests.post('/user/login', data)

        self.auth_sid = self.get_cookie(res1, "auth_sid")
        self.token = self.get_headers(res1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(res1, "user_id")

    @allure.description("This test successfully authorize user by email and password")
    @allure.issue("TMS-456")
    def test_auth_user(self):

        res2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
        )

        Assertions.assert_json_value_by_name(
            res2,
            "user_id",
            self.user_id_from_auth_method,
            error_message="User id from auth method is not equal to user id from check method"
        )
    @allure.description("This test checks auth status w/o sending auth cookie or token")
    @allure.issue("TMS-457")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            res2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token}
            )
        else:
            res2 = MyRequests.get(
                "/user/auth",
                headers={"auth_sid": self.auth_sid}
            )

        Assertions.assert_json_value_by_name(
            res2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
