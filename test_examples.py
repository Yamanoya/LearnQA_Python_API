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