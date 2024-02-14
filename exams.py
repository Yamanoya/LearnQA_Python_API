import requests

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
