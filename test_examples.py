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
