import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime

class TestUserRegister(BaseCase):

    def test_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):

        data = self.prepare_registration_data(email="vinkotov@example.com")
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{data['email']}' already exists"

    @pytest.mark.parametrize(
        'email, password, username, firstname, lastname, error',
        [
            ("vinkotov@example.com", "123", "learnqa", "learnqa", "learnqa", "Users with email 'vinkotov@example.com' already exists"),
            ("vinkotovexample.com", "123", "learnqa", "learnqa", "learnqa", "Invalid email format"),
            ("vinkotov@example.com", "123", "", "learnqa", "learnqa", "The value of 'username' field is too short"),
            ("vinkotov@example.com", "123", "learnqa", "", "learnqa", "The value of 'firstname' field is too short"),
            ("vinkotov@example.com", "123", "learnqa", "learnqa", "", "The value of 'lastname' field is too short"),
            ("vinkotov@example.com", "123", "l", "learnqa", "learnqa", "The value of 'username' field is too short"),
            ("vinkotov@example.com", "123", f"{'learnqa' * 50}", "learnqa", "learnqa", "The value of 'username' field is too long"),
        ],
        ids=['no_changes',
             'email_without_@',
             'without_username',
             'without_firstname',
             'without_lastname',
             'one_character_username',
             'character_more_250',
             ]
    )
    def test_ex_fifteen(self, email, password, username, firstname, lastname, error):
        data = {
            'password': password,
            'username': username,
            'firstName': firstname,
            'lastName': lastname,
            'email': email,
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == error

