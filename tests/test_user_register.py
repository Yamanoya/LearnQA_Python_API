import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

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
    def test_create_user_with_existing_email(self, email, password, username, firstname, lastname, error):
        data = {
            'password': password,
            'username': username,
            'firstName': firstname,
            'lastName': lastname,
            'email': email,
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        assert response.status_code == 400, f'Unexpceted status code {response.status_code}'
        assert response.content.decode("utf-8") == error

