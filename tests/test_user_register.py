import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    @pytest.mark.parametrize(
        'email, password, username, firstname, lastname',
        [
            ("vinkotov@example.com", "123", "learnqa", "learnqa", "learnqa"),
            ("vinkotovexample.com", "123", "learnqa", "learnqa", "learnqa"),
            ("vinkotov@example.com", "123", "", "learnqa", "learnqa"),
            ("vinkotov@example.com", "123", "learnqa", "", "learnqa"),
            ("vinkotov@example.com", "123", "learnqa", "learnqa", ""),
            ("vinkotov@example.com", "123", "l", "learnqa", "learnqa"),
            ("vinkotov@example.com", "123", f"{'learnqa' * 50}", "learnqa", "learnqa"),
        ],
        ids=['no_changes',
             'email_without_@',
             'without_username',
             'without_firstname',
             'without_lastname',
             'one_character_username',
             'character_more_250'
             ]
    )
    def test_create_user_with_existing_email(self, email, password, username, firstname, lastname):
        data = {
            'password': password,
            'username': username,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
        }
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        assert response.status_code == 400, f'Unexpceted status code {response.status_code}'
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: firstName, lastName", \
            f"Unexpected response content {response.content}"
