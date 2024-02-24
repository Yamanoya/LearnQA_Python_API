import pytest
import requests

class TestExample:
    def test_exam_ten_short_phrase(self):
        phrase = input()
        assert len(phrase) < 15

    def test_exam_eleven_cookie(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'
        response = requests.get(url=url).cookies
        assert 'HomeWork' in response
        assert response['HomeWork'] == 'hw_value'

    def test_exam_twelve_headers(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        response = requests.get(url=url).headers
        assert 'x-secret-homework-header' in response
        assert response['x-secret-homework-header'] == 'Some secret value'

    @pytest.mark.parametrize('user_agent, expected_device, expected_browser, expected_platform', [
        (
                'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                'Android', 'No', 'Mobile'
        ),
        (
                'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
                'iOS', 'Chrome', 'Mobile'
        ),
        (
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Unknown', 'Unknown', 'Googlebot'
        ),
        (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
                'No', 'Chrome', 'Web'
        ),
        (
                'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
                'iPhone', 'No', 'Mobile'
        )
    ])
    def test_exam_thirteen_user_agent_check(self, user_agent, expected_device, expected_browser, expected_platform):
        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'
        headers = {'User-Agent': user_agent}
        response = requests.get(url=url, headers=headers).json()

        assert response[
                   'device'] == expected_device, (f"Неправильное значение для параметра 'device'. Ожидаемое значение:"
                                                  f" {expected_device}, Фактическое значение: {response['device']}")
        assert response[
                   'browser'] == expected_browser, (f"Неправильное значение для параметра 'browser'. Ожидаемое значение:"
                                                    f" {expected_browser}, Фактическое значение: {response['browser']}")
        assert response[
                   'platform'] == expected_platform, (f"Неправильное значение для параметра 'platform'. Ожидаемое значение: "
                                                      f"{expected_platform}, Фактическое значение: {response['platform']}")
