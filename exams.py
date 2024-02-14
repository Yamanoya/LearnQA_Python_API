import json

import requests
import time

base_path = "https://playground.learnqa.ru/api/"


def exams_six_long_redirect():
    response = requests.get(url=base_path + "long_redirect", allow_redirects=True)
    count_redirects = 0

    for urls in response.history:
        count_redirects += 1
        print(f"Редирект {count_redirects}:", urls.url)

    endpoint_url = response.url
    print('Конечный url:', endpoint_url)

    print('Общее кол-во редиректов:', count_redirects)


exams_six_long_redirect()


def exams_seven_requests_and_methods():
    url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

    # запрос get без параметра
    response_without_method = requests.get(url=url)
    print(response_without_method.text)

    # запрос не из списка. HEAD
    response_invalid_method = requests.head(url=url)
    print(response_invalid_method.text)

    # запрос с правильным значением method post
    response_valid_method = requests.post(url=url, data={"method": "POST"})
    print(response_valid_method.text)

    # цикл с запросами
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    for method in methods:
        response_get = requests.get(url, params={'method': method})
        print(response_get.text)

    for method in methods:
        response_post = requests.post(url, data={'method': method})
        print(response_post.text)

    for method in methods:
        response_put = requests.put(url, data={'method': method})
        print(response_put.text)

    for method in methods:
        response_delete = requests.delete(url, data={'method': method})
        print(response_delete.text)


exams_seven_requests_and_methods()


def exams_eight_tokens():
    url = 'https://playground.learnqa.ru/ajax/api/longtime_job'

    response = requests.get(url=url)
    token = response.json()['token']
    seconds = response.json()['seconds']
    new_response = requests.get(url=url, params={"token": token})
    _ = new_response.json()['status'] == 'Job is NOT ready'
    time.sleep(seconds)
    end_response = requests.get(url=url, params={"token": token})
    _ = end_response.json()['status'] == 'Job is ready'
    result = end_response.json()['result']
    if result:
        print("Результат выполнения задачи:", result)


exams_eight_tokens()


def exams_nine_find_password():
    url_secret_password = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
    url_check_auth_cookie = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'

    passwords = [
        'password', 'password', '123456', '123456', '123456', '123456', '123456', '123456', '123456', '123456',
        '123456', '123456', 'password', 'password', 'password', 'password', 'password', 'password', '123456789',
        '12345678', '12345678', '12345678', '12345', '12345678', '12345', '12345678', '123456789', 'qwerty',
        'qwerty', 'abc123', 'qwerty', '12345678', 'qwerty', '12345678', 'qwerty', '12345678', 'password',
        'abc123', 'qwerty', 'abc123', 'qwerty', '12345', 'football', '12345', '12345', '1234567',
        'monkey', 'monkey', '123456789', '123456789', '123456789', 'qwerty', '123456789', '111111', '12345678',
        '1234567', 'letmein', '111111', '1234', 'football', '1234567890', 'letmein', '1234567', '12345',
        'letmein', 'dragon', '1234567', 'baseball', '1234', '1234567', '1234567', 'sunshine', 'iloveyou',
        'trustno1', '111111', 'iloveyou', 'dragon', '1234567', 'princess', 'football', 'qwerty', '111111',
        'dragon', 'baseball', 'adobe123[a]', 'football', 'baseball', '1234', 'iloveyou', 'iloveyou', '123123',
        'baseball', 'iloveyou', '123123', '1234567', 'welcome', 'login', 'admin', 'princess', 'abc123',
        '111111', 'trustno1', 'admin', 'monkey', '1234567890', 'welcome', 'welcome', 'admin', 'qwerty123',
        'iloveyou', '1234567', '1234567890', 'letmein', 'abc123', 'solo', 'monkey', 'welcome', '1q2w3e4r',
        'master', 'sunshine', 'letmein', 'abc123', '111111', 'abc123', 'login', '666666', 'admin',
        'sunshine', 'master', 'photoshop[a]', '111111', '1qaz2wsx', 'admin', 'abc123', 'abc123', 'qwertyuiop',
        'ashley', '123123', '1234', 'mustang', 'dragon', '121212', 'starwars', 'football', '654321',
        'bailey', 'welcome', 'monkey', 'access', 'master', 'flower', '123123', '123123', '555555',
        'passw0rd', 'shadow', 'shadow', 'shadow', 'monkey', 'passw0rd', 'dragon', 'monkey', 'lovely',
        'shadow', 'ashley', 'sunshine', 'master', 'letmein', 'dragon', 'passw0rd', '654321', '7777777',
        '123123', 'football', '12345', 'michael', 'login', 'sunshine', 'master', '!@#$%^&*', 'welcome',
        '654321', 'jesus', 'password1', 'superman', 'princess', 'master', 'hello', 'charlie', '888888',
        'superman', 'michael', 'princess', '696969', 'qwertyuiop', 'hottie', 'freedom', 'aa123456', 'princess',
        'qazwsx', 'ninja', 'azerty', '123123', 'solo', 'loveme', 'whatever', 'donald', 'dragon',
        'michael', 'mustang', 'trustno1', 'batman', 'passw0rd', 'zaq1zaq1', 'qazwsx', 'password1', 'password1',
        'Football', 'password1', '000000', 'trustno1', 'starwars', 'password1', 'trustno1', 'qwerty123', '123qwe'
    ]
    for password in passwords:
        response = requests.post(url=url_secret_password, data={'login': 'super_admin', "password": password})
        auth_cookie = response.cookies['auth_cookie']

        if auth_cookie:
            response = requests.post(url=url_check_auth_cookie, cookies={"auth_cookie": auth_cookie})
            if response.text == "You are authorized":
                print("Верный пароль:", password)
                print("Ответ сервера:", response.text)
                break
        else:
            print("Не удалось получить авторизационную cookie для пароля:", password)


exams_nine_find_password()
